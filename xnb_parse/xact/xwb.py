"""
parse XWB files
"""

from __future__ import print_function

import os
import datetime
from collections import namedtuple
from struct import Struct

from xnb_parse.file_formats.wav import (PyWavWriter, WAVE_FORMAT_WMAUDIO2, WAVE_FORMAT_WMAUDIO3, WAVE_FORMAT_PCM,
                                        WAVE_FORMAT_ADPCM, WAVE_FORMAT_XMA2)
from xnb_parse.type_reader import ReaderError
from xnb_parse.binstream import BinaryStream


WB_L_SIGNATURE = b'WBND'
WB_B_SIGNATURE = b'DNBW'
WB_TYPE_BUFFER = 0x00000000
WB_TYPE_STREAMING = 0x00000001
WB_TYPE_MASK = 0x00000001
WB_FLAGS_ENTRY_NAMES = 0x00010000
WB_FLAGS_COMPACT = 0x00020000
WB_FLAGS_SYNC_DISABLED = 0x00040000
WB_FLAGS_SEEK_TABLES = 0x00080000
WB_FLAGS_MASK = 0x000F0000
WB_ENTRY_FLAGS_READ_AHEAD = 0x00000001
WB_ENTRY_FLAGS_LOOP_CACHE = 0x00000002
WB_ENTRY_FLAGS_REMOVE_LOOP_TAIL = 0x00000004
WB_ENTRY_FLAGS_IGNORE_LOOP = 0x00000008
WB_ENTRY_FLAGS_MASK = 0x0000000F
WB_ENTRY_DURATION_MASK = 0xFFFFFFF0
WB_FORMAT_TAG_PCM = 0
WB_FORMAT_TAG_XMA = 1
WB_FORMAT_TAG_ADPCM = 2
WB_FORMAT_TAG_WMA = 3
WB_FORMAT_TAG_MASK = 0x00000003
WB_FORMAT_CHANNELS = 0x0000001C
WB_FORMAT_SAMPLES_PER_SEC = 0x007FFFE0
WB_FORMAT_BLOCK_ALIGN = 0x7F800000
WB_FORMAT_BITS_PER_SAMPLE = 0x80000000
WMA_AVG_BYTES_PER_SEC = [
    12000,
    24000,
    4000,
    6000,
    8000,
    20000,
    2500
]
WMA_BLOCK_ALIGN = [
    929,
    1487,
    1280,
    2230,
    8917,
    8192,
    4459,
    5945,
    2304,
    1536,
    1485,
    1008,
    2731,
    4096,
    6827,
    5462,
    1280
]
ADPCM_BLOCK_ALIGN_OFFSET = 22
ADPCM_COEF = [
    (256, 0),
    (512, -256),
    (0, 0),
    (192, 64),
    (240, 0),
    (460, -208),
    (392, -232)
]

XWBRegion = namedtuple('XWBRegion', ['offset', 'length'])
XWBEntry = namedtuple('XWBEntry', ['flags_duration', 'format', 'play_offset', 'play_length', 'loop_start',
                                   'loop_total'])
Entry = namedtuple('Entry', ['name', 'header', 'data', 'dpds', 'seek'])


_FILETIME_NULL = datetime.datetime(1601, 1, 1, 0, 0, 0)


def filetime_to_datetime(ftl, fth):
    timestamp = ftl | fth << 32
    return _FILETIME_NULL + datetime.timedelta(microseconds=timestamp / 10.0)


_WB_HEADER = '4s I I'
_WB_REGION = 'II'
_WB_DATA = 'I I 64s I I I I II'
_WB_ENTRY = 'I I II II'
_REGIONS = ['BANKDATA', 'ENTRYMETADATA', 'SEEKTABLES', 'ENTRYNAMES', 'ENTRYWAVEDATA']
_WAVEFORMATEX = Struct('<H H I I H H H')
_ADPCM_WAVEFORMAT = Struct('<H H')
_ADPCM_WAVEFORMAT_COEF = Struct('<h h')
_XMA_WAVEFORMAT = Struct('<H I I I I I I I B B H')


class XWB(object):
    def __init__(self, data=None, filename=None, audio_engine=None):
        self.audio_engine = audio_engine

        # open in little endian initially
        stream = BinaryStream(data=data, filename=filename)
        del data

        # check sig to find actual endianess
        h_sig = stream.peek(len(WB_L_SIGNATURE))
        if h_sig == WB_L_SIGNATURE:
            big_endian = False
        elif h_sig == WB_B_SIGNATURE:
            big_endian = True
        else:
            raise ValueError("bad sig: {!r}".format(h_sig))

        # switch stream to correct endianess
        stream.set_endian(big_endian)
        (h_sig, self.h_version, self.h_header_version) = stream.unpack(_WB_HEADER)
        regions = {k: XWBRegion._make(stream.unpack(_WB_REGION)) for k in _REGIONS}

        # check if we have a valid BANKDATA region and parse it
        bankdata_size = stream.calc_size(_WB_DATA)
        if regions['BANKDATA'].length != bankdata_size:
            raise ReaderError("Invalid BANKDATA size: {} != {}".format(regions['BANKDATA'].length, bankdata_size))
        stream.seek(regions['BANKDATA'].offset)
        (self.flags, h_entry_count, h_bank_name_raw, h_entry_metadata_element_size, h_entry_name_element_size,
         self.alignment, h_compact_format, buildtime_raw_low, buildtime_raw_high) = stream.unpack(_WB_DATA)
        self.bank_name = h_bank_name_raw.rstrip(b'\x00').decode('iso8859-1')
        del h_bank_name_raw
        self.buildtime = filetime_to_datetime(buildtime_raw_low, buildtime_raw_high)

        if self.flags & ~(WB_TYPE_MASK | WB_FLAGS_MASK):
            raise ReaderError("Unknown flags in WAVEBANK")

        # check what type of ENTRYMETADATA we have and parse it
        if self.has_compact:
            raise ReaderError("Compact format not supported")
        bankentry_size = stream.calc_size(_WB_ENTRY)
        if bankentry_size != h_entry_metadata_element_size:
            raise ReaderError("Unknown EntryMetaDataElementSize: {} != {}".format(bankentry_size,
                                                                                  h_entry_metadata_element_size))
        if regions['ENTRYMETADATA'].length != bankentry_size * h_entry_count:
            raise ReaderError("Invalid ENTRYMETADATA size: {} != {}".format(regions['ENTRYMETADATA'].length,
                                                                            bankentry_size * h_entry_count))
        stream.seek(regions['ENTRYMETADATA'].offset)
        entry_metadata = [XWBEntry._make(stream.unpack(_WB_ENTRY))
                          for _ in range(h_entry_count)]

        # read ENTRYNAMES if present
        entry_names = []
        if self.has_entry_names and regions['ENTRYNAMES'].offset and regions['ENTRYNAMES'].length:
            if regions['ENTRYNAMES'].length != h_entry_name_element_size * h_entry_count:
                raise ReaderError("Invalid ENTRYNAMES region size: {} != {}".format(
                    regions['ENTRYNAMES'].length, h_entry_name_element_size * h_entry_count))
            stream.seek(regions['ENTRYNAMES'].offset)
            entry_names = [stream.read(h_entry_name_element_size).rstrip(b'\x00').decode('iso8859-1')
                           for _ in range(h_entry_count)]

        # read SEEKTABLES if present
        entry_seektables = []
        if self.has_seek_tables and regions['SEEKTABLES'].offset and regions['SEEKTABLES'].length:
            stream.seek(regions['SEEKTABLES'].offset)
            seek_offsets = []
            for _ in range(h_entry_count):
                seek_offsets.append(stream.read_int32())
            seek_data_offset = stream.tell()
            for cur_offset in seek_offsets:
                if cur_offset >= 0:
                    stream.seek(seek_data_offset + cur_offset)
                    packet_count = stream.read_uint32()
                    cur_seek_data = BinaryStream()
                    for _ in range(packet_count):
                        cur_seek_data.write_uint32(stream.read_uint32())
                    entry_seektables.append(cur_seek_data.getvalue())
                else:
                    entry_seektables.append(None)

        self.entries = []
        for i, cur_meta in enumerate(entry_metadata):
            c_entry_flags = cur_meta.flags_duration & WB_ENTRY_FLAGS_MASK
            c_duration = (cur_meta.flags_duration & WB_ENTRY_DURATION_MASK) >> 4
            c_format_tag = cur_meta.format & WB_FORMAT_TAG_MASK
            c_channels = (cur_meta.format & WB_FORMAT_CHANNELS) >> 2
            c_samples_per_sec = (cur_meta.format & WB_FORMAT_SAMPLES_PER_SEC) >> 5
            c_block_align = (cur_meta.format & WB_FORMAT_BLOCK_ALIGN) >> 23
            c_bits_per_sample = (cur_meta.format & WB_FORMAT_BITS_PER_SAMPLE) >> 31
            entry_name = None
            if entry_names:
                entry_name = entry_names[i]
            entry_dpds = None
            entry_seek = None
            extra_header = bytes()
            # build format specific header and seek data
            if c_format_tag == WB_FORMAT_TAG_PCM:
                c_format_tag = WAVE_FORMAT_PCM
                if c_bits_per_sample == 1:
                    c_bits_per_sample = 16
                else:
                    c_bits_per_sample = 8
                c_avg_bytes_per_sec = c_samples_per_sec * c_block_align
            elif c_format_tag == WB_FORMAT_TAG_ADPCM:
                c_format_tag = WAVE_FORMAT_ADPCM
                c_bits_per_sample = 4
                c_block_align = (c_block_align + ADPCM_BLOCK_ALIGN_OFFSET) * c_channels
                cx_samples_per_block = ((c_block_align - (7 * c_channels)) * 8) // (c_bits_per_sample * c_channels) + 2
                c_avg_bytes_per_sec = (c_samples_per_sec // cx_samples_per_block) * c_block_align
                cx_num_coef = len(ADPCM_COEF)
                extra_header = _ADPCM_WAVEFORMAT.pack(cx_samples_per_block, cx_num_coef)
                for coef in ADPCM_COEF:
                    extra_header += _ADPCM_WAVEFORMAT_COEF.pack(coef[0], coef[1])
            elif c_format_tag == WB_FORMAT_TAG_WMA:
                if c_bits_per_sample == 1:
                    c_format_tag = WAVE_FORMAT_WMAUDIO3
                else:
                    c_format_tag = WAVE_FORMAT_WMAUDIO2
                c_bits_per_sample = 16
                c_avg_bytes_per_sec = WMA_AVG_BYTES_PER_SEC[c_block_align >> 5]
                c_block_align = WMA_BLOCK_ALIGN[c_block_align & 0x1f]
                if entry_seektables:
                    entry_dpds = entry_seektables[i]
                else:
                    raise ReaderError("No SEEKTABLES found for xWMA format")
            elif c_format_tag == WB_FORMAT_TAG_XMA:
                # lots of placeholders in here but seems to decode ok
                c_format_tag = WAVE_FORMAT_XMA2
                c_bits_per_sample = 16
                c_avg_bytes_per_sec = 0
                cx_num_streams = 1
                if c_channels == 2:
                    cx_channel_mask = 3
                else:
                    cx_channel_mask = 0
                cx_samples_encoded = 0
                cx_bytes_per_block = 0
                cx_play_begin = 0
                cx_play_length = 0
                cx_loop_begin = 0
                cx_loop_length = 0
                cx_loop_count = 0
                cx_encoder_version = 4
                cx_block_count = 1
                extra_header = _XMA_WAVEFORMAT.pack(cx_num_streams, cx_channel_mask, cx_samples_encoded,
                                                    cx_bytes_per_block, cx_play_begin, cx_play_length, cx_loop_begin,
                                                    cx_loop_length, cx_loop_count, cx_encoder_version, cx_block_count)
                if entry_seektables:
                    entry_seek = entry_seektables[i]
                else:
                    raise ReaderError("No SEEKTABLES found for XMA2 format")
            else:
                raise ReaderError("Unhandled entry format: {}".format(c_format_tag))
            cx_size = len(extra_header)
            entry_header = _WAVEFORMATEX.pack(c_format_tag, c_channels, c_samples_per_sec, c_avg_bytes_per_sec,
                                              c_block_align, c_bits_per_sample, cx_size)
            entry_header += extra_header
            # read entry wave data
            stream.seek(regions['ENTRYWAVEDATA'].offset + cur_meta.play_offset)
            # manually swap PCM data if needed
            entry_data = stream.read(cur_meta.play_length)
            if big_endian and c_format_tag == WAVE_FORMAT_PCM and c_bits_per_sample == 16:
                entry_data = bytearray(entry_data)
                entry_data[1::2], entry_data[0::2] = entry_data[0::2], entry_data[1::2]
            self.entries.append(Entry(entry_name, entry_header, entry_data, entry_dpds, entry_seek))

    @property
    def is_buffer(self):
        return self.flags & WB_TYPE_MASK == WB_TYPE_BUFFER

    @property
    def is_streaming(self):
        return self.flags & WB_TYPE_MASK == WB_TYPE_STREAMING

    @property
    def has_entry_names(self):
        return bool(self.flags & WB_FLAGS_ENTRY_NAMES)

    @property
    def has_compact(self):
        return bool(self.flags & WB_FLAGS_COMPACT)

    @property
    def has_sync_disabled(self):
        return bool(self.flags & WB_FLAGS_SYNC_DISABLED)

    @property
    def has_seek_tables(self):
        return bool(self.flags & WB_FLAGS_SEEK_TABLES)

    def export(self, out_dir):
        if self.bank_name:
            out_dir = os.path.join(out_dir, self.bank_name)
        if not os.path.isdir(out_dir):
            os.makedirs(out_dir)
        for i, entry in enumerate(self.entries):
            if entry.name:
                out_filename = os.path.join(out_dir, entry.name)
            else:
                out_filename = os.path.join(out_dir, str(i))
            PyWavWriter(header=entry.header, data=entry.data, dpds=entry.dpds, seek=entry.seek).write(out_filename)

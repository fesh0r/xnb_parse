# coding=utf-8
"""
parse XWB files
"""

import os
import datetime
from collections import namedtuple
from struct import Struct

from xnb_parse.file_formats.wav import WAVE_FORMAT_WMAUDIO2, WAVE_FORMAT_WMAUDIO3, PyWavWriter
from xnb_parse.type_reader import ReaderError
from xnb_parse.binstream import BinaryReader, BinaryWriter


XWB_L_SIGNATURE = b'WBND'
XWB_B_SIGNATURE = b'DNBW'
WAVEBANK_TYPE_BUFFER = 0x00000000
WAVEBANK_TYPE_STREAMING = 0x00000001
WAVEBANK_TYPE_MASK = 0x00000001
WAVEBANK_FLAGS_ENTRYNAMES = 0x00010000
WAVEBANK_FLAGS_COMPACT = 0x00020000
WAVEBANK_FLAGS_SYNC_DISABLED = 0x00040000
WAVEBANK_FLAGS_SEEKTABLES = 0x00080000
WAVEBANKENTRY_FLAGS_READAHEAD = 0x00000001
WAVEBANKENTRY_FLAGS_LOOPCACHE = 0x00000002
WAVEBANKENTRY_FLAGS_REMOVELOOPTAIL = 0x00000004
WAVEBANKENTRY_FLAGS_IGNORELOOP = 0x00000008
WAVEBANKMINIFORMAT_TAG_PCM = 0
WAVEBANKMINIFORMAT_TAG_XMA = 1
WAVEBANKMINIFORMAT_TAG_ADPCM = 2
WAVEBANKMINIFORMAT_TAG_WMA = 3

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

# pylint: disable-msg=C0103
XWBRegion = namedtuple('XWBRegion', ['offset', 'length'])
XWBEntry = namedtuple('XWBEntry', ['flags_duration', 'format', 'play_offset', 'play_length', 'loop_start',
                                   'loop_total'])
Entry = namedtuple('Entry', ['name', 'header', 'data', 'dpds', 'seek'])
# pylint: enable-msg=C0103


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


class XWB(object):
    #noinspection PyUnusedLocal
    # pylint: disable-msg=W0612
    def __init__(self, data):
        # check sig to find file endianess
        h_sig = data[:4]
        if h_sig == XWB_L_SIGNATURE:
            big_endian = False
        elif h_sig == XWB_B_SIGNATURE:
            big_endian = True
        else:
            raise ValueError("bad sig: {!r}".format(h_sig))
        stream = BinaryReader(data, big_endian=big_endian)
        (h_sig, h_version, h_header_version) = stream.unpack(_WB_HEADER)
        self.h_version = h_version
        self.h_header_version = h_header_version
        # pylint: disable-msg=W0212
        regions = {k: XWBRegion._make(stream.unpack(_WB_REGION)) for k in _REGIONS}
        # pylint: enable-msg=W0212

        # check if we have a valid BANKDATA region and parse it
        bankdata_size = stream.calc_size(_WB_DATA)
        if regions['BANKDATA'].length != bankdata_size:
            raise ReaderError("Invalid BANKDATA size: {} != {}".format(regions['BANKDATA'].length, bankdata_size))
        stream.seek(regions['BANKDATA'].offset)
        (h_flags, h_entry_count, h_bank_name_raw, h_entry_metadata_element_size, h_entry_name_element_size,
         h_alignment, h_compact_format, h_buildtime_raw_low, h_buildtime_raw_high) = stream.unpack(_WB_DATA)
        h_bank_name = h_bank_name_raw.rstrip(b'\x00').decode('utf-8')
        h_buildtime = filetime_to_datetime(h_buildtime_raw_low, h_buildtime_raw_high)
        self.h_flags = h_flags
        self.h_bank_name = h_bank_name
        self.h_buildtime = h_buildtime

        # check what type of ENTRYMETADATA we have and parse it
        if h_flags & WAVEBANK_FLAGS_COMPACT:
            raise ReaderError("Compact format not supported")
        bankentry_size = stream.calc_size(_WB_ENTRY)
        if bankentry_size != h_entry_metadata_element_size:
            raise ReaderError("Unknown EntryMetaDataElementSize: {} != {}".format(bankentry_size,
                                                                                  h_entry_metadata_element_size))
        if regions['ENTRYMETADATA'].length != bankentry_size * h_entry_count:
            raise ReaderError("Invalid ENTRYMETADATA size: {} != {}".format(regions['ENTRYMETADATA'].length,
                                                                            bankentry_size * h_entry_count))
        stream.seek(regions['ENTRYMETADATA'].offset)
        # pylint: disable-msg=W0212
        entry_metadata = [XWBEntry._make(stream.unpack(_WB_ENTRY)) for _ in range(h_entry_count)]
        # pylint: enable-msg=W0212

        # read ENTRYNAMES if present
        entry_names = None
        if h_flags & WAVEBANK_FLAGS_ENTRYNAMES:
            if regions['ENTRYNAMES'].length != h_entry_name_element_size * h_entry_count:
                raise ReaderError("Invalid ENTRYNAMES region size: {} != {}".format(
                    regions['ENTRYNAMES'].length, h_entry_name_element_size * h_entry_count))
            stream.seek(regions['ENTRYNAMES'].offset)
            entry_names = [stream.read_bytes(h_entry_name_element_size).rstrip(b'\x00').decode('utf-8')
                           for _ in range(h_entry_count)]

        # read SEEKTABLES if present
        entry_seektables = None
        if regions['SEEKTABLES'].length:
            entry_seektables = []
            stream.seek(regions['SEEKTABLES'].offset)
            seek_offsets = []
            for i in range(h_entry_count):
                seek_offsets.append(stream.read_uint32())
            seek_data_offset = stream.tell()
            for cur_offset in seek_offsets:
                stream.seek(seek_data_offset + cur_offset)
                packet_count = stream.read_uint32()
                cur_seek_data = BinaryWriter()
                for _ in range(packet_count):
                    cur_seek_data.write_uint32(stream.read_uint32())
                entry_seektables.append(cur_seek_data.serial())

        self.entries = []
        for i, cur_meta in enumerate(entry_metadata):
            c_entry_flags = cur_meta.flags_duration & 0x0f
            c_duration = cur_meta.flags_duration >> 4
            c_format_tag = cur_meta.format & 0x03
            c_channels = cur_meta.format >> 2 & 0x07
            c_samples_per_sec = cur_meta.format >> 5 & 0x3ffff
            c_block_align = cur_meta.format >> 23 & 0xff
            c_bits_per_sample = cur_meta.format >> 31
            if entry_names is not None:
                entry_name = entry_names[i]
            else:
                entry_name = None
            entry_dpds = None
            entry_seek = None
            # build format specific header and seek data
            if c_format_tag == WAVEBANKMINIFORMAT_TAG_WMA:
                if c_bits_per_sample == 1:
                    c_format_tag = WAVE_FORMAT_WMAUDIO3
                else:
                    c_format_tag = WAVE_FORMAT_WMAUDIO2
                c_bits_per_sample = 16
                c_avg_bytes_per_sec = WMA_AVG_BYTES_PER_SEC[c_block_align >> 5]
                c_block_align = WMA_BLOCK_ALIGN[c_block_align & 0x1f]
                entry_header = _WAVEFORMATEX.pack(c_format_tag, c_channels, c_samples_per_sec, c_avg_bytes_per_sec,
                                                  c_block_align, c_bits_per_sample, 0)
                if entry_seektables is None:
                    raise ReaderError("No SEEKTABLES found for xWMA format")
                entry_dpds = entry_seektables[i]
            else:
                raise ReaderError("Unhandled entry format: {}".format(c_format_tag))

            # read entry wave data
            stream.seek(regions['ENTRYWAVEDATA'].offset + cur_meta.play_offset)
            entry_data = stream.read_bytes(cur_meta.play_length)
            self.entries.append(Entry(entry_name, entry_header, entry_data, entry_dpds, entry_seek))

    def export(self, out_dir):
        if not os.path.isdir(out_dir):
            os.makedirs(out_dir)
        for i, entry in enumerate(self.entries):
            out_filename = os.path.join(out_dir, str(i))
            PyWavWriter(header=entry.header, data=entry.data, dpds=entry.dpds, seek=entry.seek).write(out_filename)

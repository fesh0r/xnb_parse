"""
parse XSB files
"""

from __future__ import print_function
from collections import OrderedDict

from xnb_parse.type_reader import ReaderError
from xnb_parse.xact.xwb import filetime_to_datetime
from xnb_parse.binstream import BinaryStream


XSB_L_SIGNATURE = b'SDBK'
XSB_B_SIGNATURE = b'KBDS'

_SB_HEADER = '4s H H H II B HHHHBH I iiiiiiiiii 64s'
_SB_LIMIT = 'B H H B'


def fix_offset(offset):
    if offset <= 0:
        offset = None
    return offset


class XSB(object):
    def __init__(self, data=None, filename=None, audio_engine=None):
        self.audio_engine = audio_engine

        # open in little endian initially
        stream = BinaryStream(data=data, filename=filename)
        del data

        # check sig to find actual endianess
        h_sig = stream.peek(len(XSB_L_SIGNATURE))
        if h_sig == XSB_L_SIGNATURE:
            big_endian = False
        elif h_sig == XSB_B_SIGNATURE:
            big_endian = True
        else:
            raise ValueError("bad sig: {!r}".format(h_sig))

        # switch stream to correct endianess
        stream.set_endian(big_endian)
        (h_sig, self.version, self.header_version, self.crc, buildtime_raw_low, buildtime_raw_high,
         self.platform, h_simple_cue_count, h_complex_cue_count, h_unknown_count, h_cue_name_hash_count,
         h_wavebank_count, h_sound_count, h_cue_names_length, simple_cue_offset_raw, complex_cue_offset_raw,
         cue_name_offset_raw, unknown_offset_raw, variation_offset_raw, transition_offset_raw, wavebank_offset_raw,
         cue_name_hash_offset_raw, cue_name_table_offset_raw, sound_offset_raw, h_name_raw) = stream.unpack(_SB_HEADER)
        h_simple_cue_offset = fix_offset(simple_cue_offset_raw)
        h_complex_cue_offset = fix_offset(complex_cue_offset_raw)
        h_cue_name_offset = fix_offset(cue_name_offset_raw)
        h_unknown_offset = fix_offset(unknown_offset_raw)
        h_variation_offset = fix_offset(variation_offset_raw)
        h_transition_offset = fix_offset(transition_offset_raw)
        h_wavebank_offset = fix_offset(wavebank_offset_raw)
        h_cue_name_hash_offset = fix_offset(cue_name_hash_offset_raw)
        h_cue_name_table_offset = fix_offset(cue_name_table_offset_raw)
        h_sound_offset = fix_offset(sound_offset_raw)
        self.name = h_name_raw.rstrip(b'\x00').decode('iso8859-1')
        del h_name_raw
        self.buildtime = filetime_to_datetime(buildtime_raw_low, buildtime_raw_high)

        self.wavebanks = None
        if h_wavebank_count and h_wavebank_offset:
            stream.seek(h_wavebank_offset)
            self.wavebanks = [stream.read(64).rstrip(b'\x00').decode('iso8859-1') for _ in range(h_wavebank_count)]
        else:
            raise ReaderError("No wavebanks found in soundbank")

        cue_name_hash = None
        if h_cue_name_hash_count and h_cue_name_hash_offset:
            stream.seek(h_cue_name_hash_offset)
            cue_name_hash = [stream.read_int16() for _ in range(h_cue_name_hash_count)]
        cue_name_table = None
        if h_cue_names_length and h_cue_name_table_offset:
            stream.seek(h_cue_name_table_offset)
            cue_name_table = [(stream.read_int32(), stream.read_int16())
                              for _ in range(h_simple_cue_count + h_complex_cue_count)]
        cue_names = None
        if cue_name_table:
            cue_names = []
            for (name_offset, _) in cue_name_table:
                stream.seek(name_offset)
                cue_names.append(stream.read_cstring())

        self.cues = []
        if cue_names:
            self.cues_name = OrderedDict()
        else:
            self.cues_name = None
        if h_simple_cue_count and h_simple_cue_offset:
            stream.seek(h_simple_cue_offset)
            for i in range(h_simple_cue_count):
                cue_name = None
                if cue_names:
                    cue_name = cue_names[i]
                cue = Cue(self, cue_name, stream)
                self.cues.append(cue)
                if cue_name:
                    self.cues_name[cue_name] = cue
        if h_complex_cue_count and h_complex_cue_offset:
            stream.seek(h_complex_cue_offset)
            for i in range(h_complex_cue_count):
                cue_name = None
                if cue_names:
                    cue_name = cue_names[h_simple_cue_count + i]
                cue = Cue(self, cue_name, stream, is_complex=True)
                self.cues.append(cue)
                if cue_name:
                    self.cues_name[cue_name] = cue
        pass


class Cue(object):
    def __init__(self, sound_bank, name, stream, is_complex=False):
        self.sound_bank = sound_bank
        self.name = name
        self.is_complex = is_complex
        self.flags = stream.read_byte()
        self.sound_offset = None
        self.unknown_offset = None
        self.variation_offset = None
        self.transition_offset = None
        if self.is_complex:
            if self.flags & 4:
                self.sound_offset = fix_offset(stream.read_int32())
                self.unknown_offset = fix_offset(stream.read_int32())
            else:
                self.variation_offset = fix_offset(stream.read_int32())
                self.transition_offset = fix_offset(stream.read_int32())
            (self.limit, self.fade_in, self.fade_out,
             limit_fade_raw) = stream.unpack(_SB_LIMIT)
            self.fade_type = limit_fade_raw & 0x03
            self.limit_type = limit_fade_raw >> 3
        else:
            self.sound_offset = fix_offset(stream.read_int32())

        next_cue_offset = stream.tell()

        if self.sound_offset:
            stream.seek(self.sound_offset)


        stream.seek(next_cue_offset)

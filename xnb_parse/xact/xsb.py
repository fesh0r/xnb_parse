"""
parse XSB files
"""

from __future__ import print_function

from xnb_parse.type_reader import ReaderError
from xnb_parse.xact.xwb import filetime_to_datetime
from xnb_parse.binstream import BinaryStream


XSB_L_SIGNATURE = b'SDBK'
XSB_B_SIGNATURE = b'KBDS'

_SB_HEADER = '4s H H H II B HHHHBH I iiiiiiiiii 64s'

class XSB(object):
    def __init__(self, data=None, filename=None):
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
        (h_sig, h_version, h_header_version, h_crc, h_buildtime_raw_low, h_buildtime_raw_high, h_platform,
         h_simple_cue_count, h_complex_cue_count, h_unknown_count, h_cue_name_hash_count, h_wavebank_count,
         h_sound_count, h_cue_names_length, h_simple_cue_offset, h_complex_cue_offset, h_cue_name_offset,
         h_unknown_offset, h_variation_offset, h_transition_offset, h_wavebank_offset, h_cue_name_hash_offset,
         h_cue_name_table_offset, h_sound_offset, h_name_raw) = stream.unpack(_SB_HEADER)
        h_name = h_name_raw.rstrip(b'\x00').decode('iso8859-1')
        h_buildtime = filetime_to_datetime(h_buildtime_raw_low, h_buildtime_raw_high)
        self.h_version = h_version
        self.h_header_version = h_header_version
        self.h_crc = h_crc
        self.h_name = h_name
        self.h_buildtime = h_buildtime
        self.h_platform = h_platform

        self.wavebanks = None
        if h_wavebank_count and h_wavebank_offset >= 0:
            stream.seek(h_wavebank_offset)
            self.wavebanks = [stream.read(64).rstrip(b'\x00').decode('iso8859-1') for _ in range(h_wavebank_count)]
        else:
            raise ReaderError("No wavebanks found in soundbank")

        self.cue_name_hash = None
        if h_cue_name_hash_count and h_cue_name_hash_offset >= 0:
            stream.seek(h_cue_name_hash_offset)
            self.cue_name_hash = [stream.read_int16() for _ in range(h_cue_name_hash_count)]
        self.cue_name_table = None
        if h_cue_names_length and h_cue_name_table_offset >= 0:
            stream.seek(h_cue_name_table_offset)
            self.cue_name_table = [(stream.read_int32(), stream.read_int16())
                                   for _ in range(h_simple_cue_count + h_complex_cue_count)]
        self.cue_name = None
        if self.cue_name_table:
            for (name_offset, _) in self.cue_name_table:
                stream.seek(name_offset)
                self.cue_name.append(stream.read_cstring())

        current_name_index = 0
        self.cues = []
        if h_simple_cue_count and h_simple_cue_offset >= 0:
            stream.seek(h_simple_cue_offset)
#            for _ in range(h_simple_cue_count):

        pass

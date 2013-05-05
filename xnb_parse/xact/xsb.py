"""
parse XSB files
"""

from __future__ import print_function

import os
from collections import OrderedDict

from xnb_parse.type_reader import ReaderError
from xnb_parse.xact.xwb import filetime_to_datetime
from xnb_parse.binstream import BinaryStream


SB_L_SIGNATURE = b'SDBK'
SB_B_SIGNATURE = b'KBDS'
SB_CUE_FLAGS_COMPLEX = 0x01
SB_CUE_FLAGS_TRANSITION = 0x02
SB_CUE_FLAGS_SOUND = 0x04
SB_CUE_FLAGS_MASK = 0x07
SB_SOUND_FLAGS_COMPLEX = 0x01
SB_SOUND_FLAGS_RPC_SOUND = 0x02
SB_SOUND_FLAGS_RPC_TRACK = 0x04
SB_SOUND_FLAGS_RPC_EFFECT = 0x08
SB_SOUND_FLAGS_DSP = 0x10
SB_SOUND_FLAGS_MASK = 0x1F
SB_EVENT_TYPE = 0x0000001F
SB_EVENT_TIMESTAMP = 0x001FFFE0
SB_EVENT_MASK = 0x001FFFFF


def fix_offset(offset):
    if offset <= 0:
        offset = None
    return offset


_SB_HEADER = '4s H H H II B HHHHBH I iiiiiiiiii 64s'
_SB_LIMIT = 'B H H B'
_SB_SOUND = 'B H B h B H'
_SB_CLIP = 'B i HH'
_SB_EVENT = 'I H B'


class XSB(object):
    def __init__(self, data=None, filename=None, audio_engine=None):
        self.audio_engine = audio_engine

        # open in little endian initially
        stream = BinaryStream(data=data, filename=filename)
        del data

        # check sig to find actual endianess
        h_sig = stream.peek(len(SB_L_SIGNATURE))
        if h_sig == SB_L_SIGNATURE:
            big_endian = False
        elif h_sig == SB_B_SIGNATURE:
            big_endian = True
        else:
            raise ValueError("bad sig: {!r}".format(h_sig))

        # switch stream to correct endianess
        stream.set_endian(big_endian)
        (h_sig, self.version, self.header_version, self.crc, buildtime_raw_low, buildtime_raw_high,
         self.platform, h_simple_cue_count, h_complex_cue_count, h_unknown_count, h_cue_name_hash_count,
         h_wave_bank_count, h_sound_count, h_cue_names_length, simple_cue_offset_raw, complex_cue_offset_raw,
         cue_name_offset_raw, unknown_offset_raw, variation_offset_raw, transition_offset_raw, wave_bank_offset_raw,
         cue_name_hash_offset_raw, cue_name_table_offset_raw, sound_offset_raw, h_name_raw) = stream.unpack(_SB_HEADER)
        h_simple_cue_offset = fix_offset(simple_cue_offset_raw)
        h_complex_cue_offset = fix_offset(complex_cue_offset_raw)
        h_cue_name_offset = fix_offset(cue_name_offset_raw)
        h_unknown_offset = fix_offset(unknown_offset_raw)
        h_variation_offset = fix_offset(variation_offset_raw)
        h_transition_offset = fix_offset(transition_offset_raw)
        h_wave_bank_offset = fix_offset(wave_bank_offset_raw)
        h_cue_name_hash_offset = fix_offset(cue_name_hash_offset_raw)
        h_cue_name_table_offset = fix_offset(cue_name_table_offset_raw)
        h_sound_offset = fix_offset(sound_offset_raw)
        self.name = h_name_raw.rstrip(b'\x00').decode('iso8859-1')
        del h_name_raw
        self.buildtime = filetime_to_datetime(buildtime_raw_low, buildtime_raw_high)

        self.wave_banks = []
        if h_wave_bank_count and h_wave_bank_offset:
            stream.seek(h_wave_bank_offset)
            self.wave_banks = [stream.read(64).rstrip(b'\x00').decode('iso8859-1') for _ in range(h_wave_bank_count)]
        else:
            raise ReaderError("No wave banks found in sound bank")

        cue_name_hash = []
        if h_cue_name_hash_count and h_cue_name_hash_offset:
            stream.seek(h_cue_name_hash_offset)
            cue_name_hash = [stream.read_int16() for _ in range(h_cue_name_hash_count)]
        cue_name_hash_entry = []
        if h_cue_names_length and h_cue_name_table_offset:
            stream.seek(h_cue_name_table_offset)
            cue_name_hash_entry = [(stream.read_int32(), stream.read_int16())
                                   for _ in range(h_simple_cue_count + h_complex_cue_count)]
        cue_names = []
        for (name_offset, _) in cue_name_hash_entry:
            stream.seek(name_offset)
            cue_names.append(stream.read_cstring())

        self.cues = []
        self.cues_name = OrderedDict()
        if h_simple_cue_count and h_simple_cue_offset:
            stream.seek(h_simple_cue_offset)
            for i in range(h_simple_cue_count):
                cue_name = None
                if cue_names:
                    cue_name = cue_names[i]
                cue = Cue(cue_name, stream)
                self.cues.append(cue)
                if cue_name:
                    self.cues_name[cue_name] = cue
        if h_complex_cue_count and h_complex_cue_offset:
            stream.seek(h_complex_cue_offset)
            for i in range(h_complex_cue_count):
                cue_name = None
                if cue_names:
                    cue_name = cue_names[h_simple_cue_count + i]
                cue = Cue(cue_name, stream, is_complex=True)
                self.cues.append(cue)
                if cue_name:
                    self.cues_name[cue_name] = cue

    def export(self, out_dir):
        if self.name:
            out_dir = os.path.join(out_dir, self.name)
        if not os.path.isdir(out_dir):
            os.makedirs(out_dir)


class Cue(object):
    def __init__(self, name, stream, is_complex=False):
        self.name = name
        self.flags = stream.read_byte()
        if self.flags & ~SB_CUE_FLAGS_MASK:
            raise ReaderError("Unknown flags in SB_CUE")
        sound_offset = None
        unknown_offset = None
        variation_offset = None
        transition_offset = None
        if self.is_complex:
            if not is_complex:
                raise ReaderError("SB_CUE_FLAGS_COMPLEX not set for complex cue")
            if self.has_sound:
                sound_offset = fix_offset(stream.read_int32())
            else:
                variation_offset = fix_offset(stream.read_int32())
            if self.has_transition:
                transition_offset = fix_offset(stream.read_int32())
            else:
                unknown_offset = fix_offset(stream.read_int32())
                if unknown_offset:
                    raise ReaderError("unknown_offset set in complex cue")
            (self.limit, self.fade_in, self.fade_out,
             limit_fade_raw) = stream.unpack(_SB_LIMIT)
            self.fade_type = limit_fade_raw & 0x03
            self.limit_type = limit_fade_raw >> 3
        else:
            if is_complex:
                raise ReaderError("SB_CUE_FLAGS_COMPLEX is set for simple cue")
            if self.has_sound:
                sound_offset = fix_offset(stream.read_int32())
            else:
                unknown_offset = fix_offset(stream.read_int32())
                raise ReaderError("SB_CUE_FLAGS_SOUND not set for simple cue")
        next_cue_offset = stream.tell()
        if sound_offset:
            stream.seek(sound_offset)
            self.sound = Sound(stream)
        stream.seek(next_cue_offset)

    @property
    def is_complex(self):
        return bool(self.flags & SB_CUE_FLAGS_COMPLEX)

    @property
    def has_sound(self):
        return bool(self.flags & SB_CUE_FLAGS_SOUND)

    @property
    def has_transition(self):
        return bool(self.flags & SB_CUE_FLAGS_TRANSITION)


class Sound(object):
    def __init__(self, stream):
        start_pos = stream.tell()
        (self.flags, self.category, self.volume, self.pitch, self.priority, entry_len) = stream.unpack(_SB_SOUND)
        if self.flags & ~SB_SOUND_FLAGS_MASK:
            raise ReaderError("Unknown flags in SB_SOUND")
        clip_count = 0
        if self.is_complex:
            clip_count = stream.read_byte()
        else:
            self.track = stream.read_uint16()
            self.wavebank = stream.read_byte()
        if self.has_rpc_sound or self.has_rpc_track or self.has_rpc_effect:
            rpc_pos = stream.tell()
            rpc_extra = stream.read_uint16()
            # TODO: parse RPC data
            stream.seek(rpc_pos + rpc_extra)
        if self.has_dsp:
            dsp_pos = stream.tell()
            dsp_extra = stream.read_uint16()
            # TODO: parse DSP data
            stream.seek(dsp_pos + dsp_extra)
        self.clips = []
        if self.is_complex:
            self.clips = [Clip(stream) for _ in range(clip_count)]
        if stream.tell() > entry_len + start_pos:
            raise ReaderError("SB_SOUND length mismatch")

    @property
    def is_complex(self):
        return bool(self.flags & SB_CUE_FLAGS_COMPLEX)

    @property
    def has_rpc_sound(self):
        return bool(self.flags & SB_SOUND_FLAGS_RPC_SOUND)

    @property
    def has_rpc_track(self):
        return bool(self.flags & SB_SOUND_FLAGS_RPC_TRACK)

    @property
    def has_rpc_effect(self):
        return bool(self.flags & SB_SOUND_FLAGS_RPC_EFFECT)

    @property
    def has_dsp(self):
        return bool(self.flags & SB_SOUND_FLAGS_DSP)


class Clip(object):
    def __init__(self, stream):
        (self.volume, clip_offset_raw, self.filter_flags, self.filter_freq) = stream.unpack(_SB_CLIP)
        clip_offset = fix_offset(clip_offset_raw)
        next_clip_offset = stream.tell()
        self.events = []
        if clip_offset:
            stream.seek(clip_offset)
            event_count = stream.read_byte()
            self.events = [ClipEvent(stream) for _ in range(event_count)]
        stream.seek(next_clip_offset)


class Event(object):
    has_sound = False


class Event1(Event):
    has_sound = True

    def __init__(self, stream):
        pass


_EVENTS = {
    1: Event1,
}


class ClipEvent(object):
    def __init__(self, stream):
        (self.flags, self.random_offset, unknown) = stream.unpack(_SB_EVENT)
        # if self.flags & ~SB_EVENT_MASK:
        #     raise ReaderError("Unknown flags in SB_EVENT")
        self.event = _EVENTS[self.event_type](stream)
        # if unknown:
        #     raise ReaderError("Unknown field set in SB_EVENT")

    @property
    def event_type(self):
        return self.flags & SB_EVENT_TYPE

    @property
    def timestamp(self):
        return (self.flags & SB_EVENT_TIMESTAMP) >> 5

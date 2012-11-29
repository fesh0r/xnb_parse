"""
FEZ music type readers
"""

from __future__ import print_function

from xnb_parse.type_reader import TypeReaderPlugin, BaseTypeReader, EnumTypeReader
from xnb_parse.type_readers.xna_primitive import Int32Reader
from xnb_parse.type_readers.xna_system import ListReader, ArrayReader
from xnb_parse.xna_types.fez.fez_music import ShardNotes, AssembleChords, TrackedSong, Loop


class TrackedSongReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'FezEngine.Structure.TrackedSong'
    reader_name = 'FezEngine.Readers.TrackedSongReader'

    def read(self):
        loops = self.stream.read_object(ListReader, [LoopReader])
        name = self.stream.read_string()
        tempo = self.stream.read_int32()
        time_signature = self.stream.read_int32()
        notes = self.stream.read_object(ArrayReader, [ShardNotesReader])
        assemble_chord = self.stream.read_object(AssembleChordsReader)
        random_ordering = self.stream.read_boolean()
        custom_ordering = self.stream.read_object(ArrayReader, [Int32Reader])
        return TrackedSong(loops, name, tempo, time_signature, notes, assemble_chord, random_ordering, custom_ordering)


class LoopReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'FezEngine.Structure.Loop'
    reader_name = 'FezEngine.Readers.LoopReader'

    def read(self):
        duration = self.stream.read_int32()
        loop_times_from = self.stream.read_int32()
        loop_times_to = self.stream.read_int32()
        name = self.stream.read_string()
        trigger_from = self.stream.read_int32()
        trigger_to = self.stream.read_int32()
        delay = self.stream.read_int32()
        night = self.stream.read_boolean()
        day = self.stream.read_boolean()
        dusk = self.stream.read_boolean()
        dawn = self.stream.read_boolean()
        fractional_time = self.stream.read_boolean()
        one_at_a_time = self.stream.read_boolean()
        cut_off_tail = self.stream.read_boolean()
        return Loop(duration, loop_times_from, loop_times_to, name, trigger_from, trigger_to, delay, night, day, dusk,
                    dawn, fractional_time, one_at_a_time, cut_off_tail)


class ShardNotesReader(EnumTypeReader, TypeReaderPlugin):
    target_type = 'FezEngine.Structure.ShardNotes'
    reader_name = 'FezEngine.Readers.ShardNotesReader'
    enum_type = ShardNotes


class AssembleChordsReader(EnumTypeReader, TypeReaderPlugin):
    target_type = 'FezEngine.Structure.AssembleChords'
    reader_name = 'FezEngine.Readers.AssembleChordsReader'
    enum_type = AssembleChords

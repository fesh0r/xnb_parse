"""
FEZ music type readers
"""

from xnb_parse.type_reader import BaseTypeReader, ValueTypeReader
from xnb_parse.type_reader_manager import TypeReaderPlugin
from xnb_parse.type_readers.xna_system import ListReader, ArrayReader, EnumReader
from xnb_parse.type_readers.xna_primitive import Int32Reader


class TrackedSongReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'FezEngine.Structure.TrackedSong'
    reader_name = 'FezEngine.Readers.TrackedSongReader'

    def read(self):
        loops = self.stream.read_object(ListReader, [LoopReader])
        name = self.stream.read('str')
        tempo = self.stream.read('s4')
        time_signature = self.stream.read('s4')
        notes = self.stream.read_object(ArrayReader, [ShardNotesReader])
        assemble_chord = self.stream.read_object(EnumReader, [AssembleChordsReader])
        random_ordering = self.stream.read('?')
        custom_ordering = self.stream.read_object(ArrayReader, [Int32Reader])
        return loops, name, tempo, time_signature, notes, assemble_chord, random_ordering, custom_ordering


class LoopReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'FezEngine.Structure.Loop'
    reader_name = 'FezEngine.Readers.LoopReader'

    def read(self):
        duration = self.stream.read('s4')
        loop_times_from = self.stream.read('s4')
        loop_times_to = self.stream.read('s4')
        name = self.stream.read('str')
        trigger_from = self.stream.read('s4')
        trigger_to = self.stream.read('s4')
        delay = self.stream.read('s4')
        night = self.stream.read('?')
        day = self.stream.read('?')
        dusk = self.stream.read('?')
        dawn = self.stream.read('?')
        fractional_time = self.stream.read('?')
        one_at_a_time = self.stream.read('?')
        cut_off_tail = self.stream.read('?')
        return (duration, loop_times_from, loop_times_to, name, trigger_from, trigger_to, delay, night, day, dusk,
                dawn, fractional_time, one_at_a_time, cut_off_tail)


class ShardNotesReader(ValueTypeReader, TypeReaderPlugin):
    target_type = 'FezEngine.Structure.ShardNotes'
    reader_name = 'FezEngine.Readers.ShardNotesReader'

    def read(self):
        return self.stream.read('u4')


class AssembleChordsReader(ValueTypeReader, TypeReaderPlugin):
    target_type = 'FezEngine.Structure.AssembleChords'
    reader_name = 'FezEngine.Readers.AssembleChordsReader'

    def read(self):
        return self.stream.read('u4')

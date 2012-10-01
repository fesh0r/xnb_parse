"""
FEZ graphics type readers
"""

from xnb_parse.type_reader import BaseTypeReader, generic_reader_type
from xnb_parse.type_reader_manager import TypeReaderPlugin
from xnb_parse.type_readers.xna_system import ListReader, ArrayReader, TimeSpanReader
from xnb_parse.type_readers.xna_math import ColorReader
from xnb_parse.type_readers.xna_primitive import StringReader

from xnb_parse.type_readers.fez.fez_basic import NpcActionReader


class ArtObjectReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'FezEngine.Structure.ArtObject'
    reader_name = 'FezEngine.Readers.ArtObjectReader'


class NpcMetadataReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'FezEngine.Structure.NpcMetadata'
    reader_name = 'FezEngine.Readers.NpcMetadataReader'

    def read(self):
        walk_speed = self.stream.read('f')
        avoids_gomez = self.stream.read('?')
        sound_path = self.stream.read_object(StringReader.target_type)
        sound_actions = self.stream.read_object(generic_reader_type(ListReader, [NpcActionReader]))
        return walk_speed, avoids_gomez, sound_path, sound_actions


class AnimatedTextureReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'FezEngine.Structure.AnimatedTexture'
    reader_name = 'FezEngine.Readers.AnimatedTextureReader'

    def read(self):
        width = self.stream.read('s4')
        height = self.stream.read('s4')
        actual_width = self.stream.read('s4')
        actual_height = self.stream.read('s4')
        frames = self.stream.read_object(generic_reader_type(ListReader, [FrameReader]))
        return width, height, actual_width, actual_height, frames


class FrameReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'FezEngine.Content.FrameContent'
    reader_name = 'FezEngine.Readers.FrameReader'

    def read(self):
        duration = self.stream.read_object(TimeSpanReader.target_type)
        data = self.stream.read_object(generic_reader_type(ArrayReader, [ColorReader]))
        return duration, data

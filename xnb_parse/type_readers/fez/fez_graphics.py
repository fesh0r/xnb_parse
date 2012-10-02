"""
FEZ graphics type readers
"""

from xnb_parse.type_reader import BaseTypeReader, ValueTypeReader, GenericTypeReader, generic_reader_type
from xnb_parse.type_reader_manager import TypeReaderPlugin
from xnb_parse.type_readers.xna_system import ListReader, ArrayReader, TimeSpanReader, EnumReader, ReflectiveReader
from xnb_parse.type_readers.xna_math import ColorReader, Vector2Reader, Vector3Reader, MatrixReader
from xnb_parse.type_readers.xna_graphics import PrimitiveTypeReader
from xnb_parse.type_readers.xna_primitive import StringReader, UInt16Reader
from xnb_parse.type_readers.fez.fez_basic import NpcActionReader, ActorTypeReader, SetReader, FaceOrientationReader


class ArtObjectReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'FezEngine.Structure.ArtObject'
    reader_name = 'FezEngine.Readers.ArtObjectReader'

    def __init__(self, stream=None, version=None):
        BaseTypeReader.__init__(self, stream=stream, version=version)
        TypeReaderPlugin.__init__(self)
        self.vector3_reader = self.stream.get_type_reader(Vector3Reader)

    def init_reader(self):
        BaseTypeReader.init_reader(self)
        self.vector3_reader.init_reader()

    def read(self):
        name = self.stream.read('str')
        cubemap_path = self.stream.read('str')
        size = self.vector3_reader.read()
        geometry = self.stream.read_object(ShaderInstancedIndexedPrimitivesReader,
                                           [VertexPositionNormalTextureInstanceReader, MatrixReader])
        actor_type = self.stream.read_object(EnumReader, [ActorTypeReader])
        no_silhouette = self.stream.read('?')
        laser_outlets = self.stream.read_object(ReflectiveReader, [generic_reader_type(SetReader,
                                                                                       [FaceOrientationReader])])
        return name, cubemap_path, size, geometry, actor_type, no_silhouette, laser_outlets


class ShaderInstancedIndexedPrimitivesReader(GenericTypeReader, TypeReaderPlugin):
    generic_target_type = 'FezEngine.Structure.Geometry.ShaderInstancedIndexedPrimitives`2'
    generic_reader_name = 'FezEngine.Readers.ShaderInstancedIndexedPrimitivesReader`2'

    def read(self):
        primitive_type = self.stream.read_object(EnumReader, [PrimitiveTypeReader])
        vertices = self.stream.read_object(ArrayReader, [VertexPositionNormalTextureInstanceReader])
        indices = self.stream.read_object(ArrayReader, [UInt16Reader])
        return primitive_type, vertices, indices


class VertexPositionNormalTextureInstanceReader(ValueTypeReader, TypeReaderPlugin):
    target_type = 'FezEngine.Structure.Geometry.VertexPositionNormalTextureInstance'
    reader_name = 'FezEngine.Readers.VertexPositionNormalTextureInstanceReader'

    def __init__(self, stream=None, version=None):
        ValueTypeReader.__init__(self, stream=stream, version=version)
        TypeReaderPlugin.__init__(self)
        self.vector2_reader = self.stream.get_type_reader(Vector2Reader)
        self.vector3_reader = self.stream.get_type_reader(Vector3Reader)

    def init_reader(self):
        BaseTypeReader.init_reader(self)
        self.vector2_reader.init_reader()
        self.vector3_reader.init_reader()

    def read(self):
        position = self.vector3_reader.read()
        normal = self.stream.read('s1')
        texture_coord = self.vector2_reader.read()
        return position, normal, texture_coord


class NpcMetadataReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'FezEngine.Structure.NpcMetadata'
    reader_name = 'FezEngine.Readers.NpcMetadataReader'

    def read(self):
        walk_speed = self.stream.read('f')
        avoids_gomez = self.stream.read('?')
        sound_path = self.stream.read_object(StringReader)
        sound_actions = self.stream.read_object(ListReader, [NpcActionReader])
        return walk_speed, avoids_gomez, sound_path, sound_actions


class AnimatedTextureReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'FezEngine.Structure.AnimatedTexture'
    reader_name = 'FezEngine.Readers.AnimatedTextureReader'

    def read(self):
        width = self.stream.read('s4')
        height = self.stream.read('s4')
        actual_width = self.stream.read('s4')
        actual_height = self.stream.read('s4')
        frames = self.stream.read_object(ListReader, [FrameReader])
        return width, height, actual_width, actual_height, frames


class FrameReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'FezEngine.Content.FrameContent'
    reader_name = 'FezEngine.Readers.FrameReader'

    def read(self):
        duration = self.stream.read_object(TimeSpanReader)
        data = self.stream.read_object(ArrayReader, [ColorReader])
        return duration, data

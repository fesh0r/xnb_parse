"""
FEZ graphics type readers
"""

from __future__ import print_function

from xnb_parse.type_reader import (TypeReaderPlugin, BaseTypeReader, ValueTypeReader, GenericTypeReader,
                                   generic_reader_type)
from xnb_parse.type_readers.xna_graphics import PrimitiveTypeReader, Texture2DReader
from xnb_parse.type_readers.xna_math import MatrixReader, RectangleReader
from xnb_parse.type_readers.xna_primitive import StringReader, UInt16Reader
from xnb_parse.type_readers.xna_system import ListReader, ArrayReader, TimeSpanReader, ReflectiveReader
from xnb_parse.type_readers.fez.fez_basic import NpcActionReader, ActorTypeReader, SetReader, FaceOrientationReader
from xnb_parse.xna_types.xna_math import Vector3, Vector2
from xnb_parse.xna_types.fez.fez_graphics import (AnimatedTexture, Frame, ArtObject, ShaderInstancedIndexedPrimitives,
                                                  VertexPositionNormalTextureInstance, NpcMetadata, AnimatedTexturePC,
                                                  FramePC, ArtObjectPC)

# avoiding circular import
PLATFORM_WINDOWS = b'w'


class ArtObjectReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'FezEngine.Structure.ArtObject'
    reader_name = 'FezEngine.Readers.ArtObjectReader'

    def read(self):
        if self.file_platform == PLATFORM_WINDOWS:
            name = self.stream.read_string()
            cubemap = self.stream.read_object(Texture2DReader)
            size = self.stream.read_vector3()
            geometry = self.stream.read_object(ShaderInstancedIndexedPrimitivesReader,
                                               [VertexPositionNormalTextureInstanceReader, MatrixReader])
            actor_type = self.stream.read_object(ActorTypeReader)
            no_silhouette = self.stream.read_boolean()
            return ArtObjectPC(name, cubemap, size, geometry, actor_type, no_silhouette)
        else:
            name = self.stream.read_string()
            cubemap_path = self.stream.read_string()
            size = self.stream.read_vector3()
            geometry = self.stream.read_object(ShaderInstancedIndexedPrimitivesReader,
                                               [VertexPositionNormalTextureInstanceReader, MatrixReader])
            actor_type = self.stream.read_object(ActorTypeReader)
            no_silhouette = self.stream.read_boolean()
            laser_outlets = self.stream.read_object(ReflectiveReader, [generic_reader_type(SetReader,
                                                                                           [FaceOrientationReader])])
            return ArtObject(name, cubemap_path, size, geometry, actor_type, no_silhouette, laser_outlets)


class ShaderInstancedIndexedPrimitivesReader(GenericTypeReader, TypeReaderPlugin):
    generic_target_type = 'FezEngine.Structure.Geometry.ShaderInstancedIndexedPrimitives`2'
    generic_reader_name = 'FezEngine.Readers.ShaderInstancedIndexedPrimitivesReader`2'

    def read(self):
        primitive_type = self.stream.read_object(PrimitiveTypeReader)
        vertices = self.stream.read_object(ArrayReader, [self.readers[0]])
        indices = self.stream.read_object(ArrayReader, [UInt16Reader])
        return ShaderInstancedIndexedPrimitives(primitive_type, vertices, indices)


class VertexPositionNormalTextureInstanceReader(ValueTypeReader, TypeReaderPlugin):
    target_type = 'FezEngine.Structure.Geometry.VertexPositionNormalTextureInstance'
    reader_name = 'FezEngine.Readers.VertexPositionNormalTextureInstanceReader'

    def read(self):
        values = self.stream.unpack('3f B 2f')
        position = Vector3._make(values[0:3])
        normal = values[3]
        texture_coord = Vector2._make(values[4:6])
        return VertexPositionNormalTextureInstance(position, normal, texture_coord)


class NpcMetadataReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'FezEngine.Structure.NpcMetadata'
    reader_name = 'FezEngine.Readers.NpcMetadataReader'

    def read(self):
        walk_speed = self.stream.read_single()
        avoids_gomez = self.stream.read_boolean()
        sound_path = self.stream.read_object(StringReader)
        sound_actions = self.stream.read_object(ListReader, [NpcActionReader])
        return NpcMetadata(walk_speed, avoids_gomez, sound_path, sound_actions)


class AnimatedTextureReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'FezEngine.Structure.AnimatedTexture'
    reader_name = 'FezEngine.Readers.AnimatedTextureReader'

    def read(self):
        if self.file_platform == PLATFORM_WINDOWS:
            width = self.stream.read_int32()
            height = self.stream.read_int32()
            actual_width = self.stream.read_int32()
            actual_height = self.stream.read_int32()
            elements = self.stream.read_uint32()
            data = self.stream.read(elements)
            frames = self.stream.read_object(ListReader, [FrameReader])
            return AnimatedTexturePC(width, height, actual_width, actual_height, data, frames)
        else:
            width = self.stream.read_int32()
            height = self.stream.read_int32()
            actual_width = self.stream.read_int32()
            actual_height = self.stream.read_int32()
            frames = self.stream.read_object(ListReader, [FrameReader])
            return AnimatedTexture(width, height, actual_width, actual_height, frames)


class FrameReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'FezEngine.Content.FrameContent'
    reader_name = 'FezEngine.Readers.FrameReader'

    def read(self):
        if self.file_platform == PLATFORM_WINDOWS:
            duration = self.stream.read_object(TimeSpanReader)
            rectangle = self.stream.read_object(RectangleReader)
            return FramePC(duration, rectangle)
        else:
            duration = self.stream.read_object(TimeSpanReader)
            _ = self.stream.read_7bit_encoded_int()
            elements = self.stream.read_uint32()
            data = self.stream.read(elements * 4)
            return Frame(duration, data)

# coding=utf-8
"""
FEZ graphics type readers
"""

from __future__ import absolute_import, division, unicode_literals

from xnb_parse.type_reader import BaseTypeReader, ValueTypeReader, GenericTypeReader, generic_reader_type
from xnb_parse.type_reader_manager import TypeReaderPlugin
from xnb_parse.type_readers.xna_system import ListReader, ArrayReader, TimeSpanReader, ReflectiveReader
from xnb_parse.type_readers.xna_math import ColorReader, MatrixReader
from xnb_parse.type_readers.xna_graphics import PrimitiveTypeReader
from xnb_parse.type_readers.xna_primitive import StringReader, UInt16Reader
from xnb_parse.type_readers.fez.fez_basic import NpcActionReader, ActorTypeReader, SetReader, FaceOrientationReader
from xnb_parse.xna_types.fez.fez_graphics import (AnimatedTexture, Frame, ArtObject, ShaderInstancedIndexedPrimitives,
                                                  VertexPositionNormalTextureInstance, NpcMetadata)


class ArtObjectReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'FezEngine.Structure.ArtObject'
    reader_name = 'FezEngine.Readers.ArtObjectReader'

    def read(self):
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
        position = self.stream.read_vector3()
        normal = self.stream.read_byte()
        texture_coord = self.stream.read_vector2()
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
        duration = self.stream.read_object(TimeSpanReader)
        data = self.stream.read_object(ArrayReader, [ColorReader])
        return Frame(duration, data)

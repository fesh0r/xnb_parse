"""
graphics type readers
"""

from __future__ import print_function

from xnb_parse.type_reader import TypeReaderPlugin, BaseTypeReader, ReaderError, EnumTypeReader
from xnb_parse.type_readers.xna_math import Vector3Reader, RectangleReader
from xnb_parse.type_readers.xna_primitive import CharReader, StringReader, ObjectReader
from xnb_parse.type_readers.xna_system import ListReader, DictionaryReader
from xnb_parse.xna_types.xna_graphics import (Texture2D, Texture3D, TextureCube, CUBE_SIDES, IndexBuffer, Effect,
                                              get_surface_format, PrimitiveType, SpriteFont, BasicEffect,
                                              PrimitiveType4)


class TextureReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.Graphics.Texture'
    reader_name = 'Microsoft.Xna.Framework.Content.TextureReader'

    def read(self):
        raise ReaderError("TextureReader should never be invoked directly")


class Texture2DReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.Graphics.Texture2D'
    reader_name = 'Microsoft.Xna.Framework.Content.Texture2DReader'

    def read(self):
        surface_format_raw = self.stream.read_int32()
        surface_format = get_surface_format(self.stream.file_version, surface_format_raw)
        width = self.stream.read_int32()
        height = self.stream.read_int32()
        mip_count = self.stream.read_int32()
        mip_levels = []
        for _ in range(mip_count):
            size = self.stream.read_int32()
            data = self.stream.read(size)
            mip_levels.append(data)
        return Texture2D(surface_format, width, height, mip_levels, self.stream.needs_swap)


class Texture3DReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.Graphics.Texture3D'
    reader_name = 'Microsoft.Xna.Framework.Content.Texture3DReader'

    def read(self):
        surface_format_raw = self.stream.read_int32()
        surface_format = get_surface_format(self.stream.file_version, surface_format_raw)
        width = self.stream.read_int32()
        height = self.stream.read_int32()
        depth = self.stream.read_int32()
        mip_count = self.stream.read_int32()
        mip_levels = []
        for _ in range(mip_count):
            size = self.stream.read_int32()
            data = self.stream.read(size)
            mip_levels.append(data)
        return Texture3D(surface_format, width, height, depth, mip_levels, self.stream.needs_swap)


class TextureCubeReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.Graphics.TextureCube'
    reader_name = 'Microsoft.Xna.Framework.Content.TextureCubeReader'

    def read(self):
        surface_format_raw = self.stream.read_int32()
        surface_format = get_surface_format(self.stream.file_version, surface_format_raw)
        texture_size = self.stream.read_int32()
        mip_count = self.stream.read_int32()
        sides = {}
        for side in CUBE_SIDES:
            mip_levels = []
            for _ in range(mip_count):
                size = self.stream.read_int32()
                data = self.stream.read(size)
                mip_levels.append(data)
            sides[side] = mip_levels
        return TextureCube(surface_format, texture_size, sides, self.stream.needs_swap)


class IndexBufferReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.Graphics.IndexBuffer'
    reader_name = 'Microsoft.Xna.Framework.Content.IndexBufferReader'

    def read(self):
        index_16 = self.stream.read_boolean()
        size = self.stream.read_int32()
        data = self.stream.read(size)
        return IndexBuffer(index_16, data)


class VertexBufferReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.Graphics.VertexBuffer'
    reader_name = 'Microsoft.Xna.Framework.Content.VertexBufferReader'

    def read(self):
        size = self.stream.read_int32()
        data = self.stream.read(size)
        return data


class VertexDeclarationReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.Graphics.VertexDeclaration'
    reader_name = 'Microsoft.Xna.Framework.Content.VertexDeclarationReader'

    def read(self):
        element_count = self.stream.read_int32()
        elements = []
        for _ in range(element_count):
            v_stream = self.stream.read_int16()
            v_offset = self.stream.read_int16()
            v_format = self.stream.read_byte()
            v_method = self.stream.read_byte()
            v_usage = self.stream.read_byte()
            v_usage_index = self.stream.read_byte()
            element = v_stream, v_offset, v_format, v_method, v_usage, v_usage_index
            elements.append(element)
        return elements


class EffectReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.Graphics.Effect'
    reader_name = 'Microsoft.Xna.Framework.Content.EffectReader'

    def read(self):
        size = self.stream.read_int32()
        data = self.stream.read(size)
        return Effect(data)


class EffectMaterialReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.Graphics.EffectMaterial'
    reader_name = 'Microsoft.Xna.Framework.Content.EffectMaterialReader'

    def read(self):
        effect = self.stream.read_external_reference(EffectReader)
        parameters = self.stream.read_object(DictionaryReader, [StringReader, ObjectReader])
        return effect, parameters


class BasicEffectReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.Graphics.BasicEffect'
    reader_name = 'Microsoft.Xna.Framework.Content.BasicEffectReader'

    def read(self):
        texture = self.stream.read_external_reference(TextureReader)
        colour_d = self.stream.read_vector3()
        colour_e = self.stream.read_vector3()
        colour_s = self.stream.read_vector3()
        spec = self.stream.read_single()
        alpha = self.stream.read_single()
        colour_v = self.stream.read_boolean()
        return BasicEffect(texture, colour_d, colour_e, colour_s, spec, alpha, colour_v)


class SpriteFontReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.Graphics.SpriteFont'
    reader_name = 'Microsoft.Xna.Framework.Content.SpriteFontReader'

    def read(self):
        texture = self.stream.read_object(Texture2DReader)
        glyphs = self.stream.read_object(ListReader, [RectangleReader])
        cropping = self.stream.read_object(ListReader, [RectangleReader])
        char_map = self.stream.read_object(ListReader, [CharReader])
        v_space = self.stream.read_int32()
        h_space = self.stream.read_single()
        kerning = self.stream.read_object(ListReader, [Vector3Reader])
        default_char = None
        has_default_char = self.stream.read_boolean()
        if has_default_char:
            default_char = self.stream.read_char()
        return SpriteFont(texture, glyphs, cropping, char_map, v_space, h_space, kerning, default_char)


class ModelReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.Graphics.Model'
    reader_name = 'Microsoft.Xna.Framework.Content.ModelReader'


class PrimitiveTypeReader(EnumTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.Graphics.PrimitiveType'
    reader_name = 'Microsoft.Xna.Framework.Content.PrimitiveTypeReader'
    enum_type = PrimitiveType
    enum_type4 = PrimitiveType4

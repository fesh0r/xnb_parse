"""
graphics type readers
"""

from xnb_parse.type_reader import BaseTypeReader, ValueTypeReader, ReaderError, generic_reader_name
from xnb_parse.type_reader_manager import TypeReaderPlugin
from xnb_parse.xna_types.xna_graphics import Texture2D, Texture3D, TextureCube, CUBE_SIDES, IndexBuffer, Effect
from xnb_parse.type_readers.xna_system import NullableReader, ListReader, DictionaryReader
from xnb_parse.type_readers.xna_math import Vector3Reader, RectangleReader
from xnb_parse.type_readers.xna_primitive import CharReader, StringReader, ObjectReader


class TextureReader(BaseTypeReader, TypeReaderPlugin):
    target_type = u'Microsoft.Xna.Framework.Graphics.Texture'
    reader_name = u'Microsoft.Xna.Framework.Content.TextureReader'

    def read(self):
        raise ReaderError("TextureReader should never be invoked directly")


class Texture2DReader(BaseTypeReader, TypeReaderPlugin):
    target_type = u'Microsoft.Xna.Framework.Graphics.Texture2D'
    reader_name = u'Microsoft.Xna.Framework.Content.Texture2DReader'

    def read(self):
        texture_format = self.stream.read_int32()
        width = self.stream.read_int32()
        height = self.stream.read_int32()
        mip_count = self.stream.read_int32()
        mip_levels = []
        for _ in range(mip_count):
            data_size = self.stream.read_int32()
            data = self.stream.read_bytes(data_size)
            mip_levels.append(data)
        return Texture2D(texture_format, width, height, mip_levels)


class Texture3DReader(BaseTypeReader, TypeReaderPlugin):
    target_type = u'Microsoft.Xna.Framework.Graphics.Texture3D'
    reader_name = u'Microsoft.Xna.Framework.Content.Texture3DReader'

    def read(self):
        texture_format = self.stream.read_int32()
        width = self.stream.read_int32()
        height = self.stream.read_int32()
        depth = self.stream.read_int32()
        mip_count = self.stream.read_int32()
        mip_levels = []
        for _ in range(mip_count):
            data_size = self.stream.read_int32()
            data = self.stream.read_bytes(data_size)
            mip_levels.append(data)
        return Texture3D(texture_format, width, height, depth, mip_levels)


class TextureCubeReader(BaseTypeReader, TypeReaderPlugin):
    target_type = u'Microsoft.Xna.Framework.Graphics.TextureCube'
    reader_name = u'Microsoft.Xna.Framework.Content.TextureCubeReader'

    def read(self):
        texture_format = self.stream.read_int32()
        texture_size = self.stream.read_int32()
        mip_count = self.stream.read_int32()
        sides = {}
        for side in CUBE_SIDES:
            mip_levels = []
            for _ in range(mip_count):
                data_size = self.stream.read_int32()
                data = self.stream.read_bytes(data_size)
                mip_levels.append(data)
            sides[side] = mip_levels
        return TextureCube(texture_format, texture_size, sides)


class IndexBufferReader(BaseTypeReader, TypeReaderPlugin):
    target_type = u'Microsoft.Xna.Framework.Graphics.IndexBuffer'
    reader_name = u'Microsoft.Xna.Framework.Content.IndexBufferReader'

    def read(self):
        index_16 = self.stream.read_boolean()
        index_size = self.stream.read_int32()
        index_data = self.stream.read_bytes(index_size)
        return IndexBuffer(index_16, index_data)


class VertexBufferReader(BaseTypeReader, TypeReaderPlugin):
    target_type = u'Microsoft.Xna.Framework.Graphics.VertexBuffer'
    reader_name = u'Microsoft.Xna.Framework.Content.VertexBufferReader'

    def read(self):
        vertex_size = self.stream.read_int32()
        vertex_data = self.stream.read_bytes(vertex_size)
        return vertex_data


class VertexDeclarationReader(BaseTypeReader, TypeReaderPlugin):
    target_type = u'Microsoft.Xna.Framework.Graphics.VertexDeclaration'
    reader_name = u'Microsoft.Xna.Framework.Content.VertexDeclarationReader'

    def read(self):
        element_count = self.stream.read_int32()
        elements = []
        for _ in range(element_count):
            element_stream = self.stream.read_int16()
            element_offset = self.stream.read_int16()
            element_format = self.stream.read_byte()
            element_method = self.stream.read_byte()
            element_usage = self.stream.read_byte()
            element_usage_index = self.stream.read_byte()
            element = element_stream, element_offset, element_format, element_method, element_usage, element_usage_index
            elements.append(element)
        return elements


class EffectReader(BaseTypeReader, TypeReaderPlugin):
    target_type = u'Microsoft.Xna.Framework.Graphics.Effect'
    reader_name = u'Microsoft.Xna.Framework.Content.EffectReader'

    def read(self):
        effect_size = self.stream.read_int32()
        effect_data = self.stream.read_bytes(effect_size)
        return Effect(effect_data)


class EffectMaterialReader(BaseTypeReader, TypeReaderPlugin):
    target_type = u'Microsoft.Xna.Framework.Graphics.EffectMaterial'
    reader_name = u'Microsoft.Xna.Framework.Content.EffectMaterialReader'

    def read(self):
        effect = self.stream.read_external_reference(EffectReader)
        parameters = self.stream.read_object(DictionaryReader, [StringReader, ObjectReader])
        return effect, parameters


class BasicEffectReader(BaseTypeReader, TypeReaderPlugin):
    target_type = u'Microsoft.Xna.Framework.Graphics.BasicEffect'
    reader_name = u'Microsoft.Xna.Framework.Content.BasicEffectReader'

    def read(self):
        texture = self.stream.read_external_reference(TextureReader)
        colour_d = self.stream.read_vector3()
        colour_e = self.stream.read_vector3()
        colour_s = self.stream.read_vector3()
        spec = self.stream.read_single()
        alpha = self.stream.read_single()
        colour_v = self.stream.read_boolean()
        return texture, colour_d, colour_e, colour_s, spec, alpha, colour_v


class SpriteFontReader(BaseTypeReader, TypeReaderPlugin):
    target_type = u'Microsoft.Xna.Framework.Graphics.SpriteFont'
    reader_name = u'Microsoft.Xna.Framework.Content.SpriteFontReader'

    def __init__(self, stream=None, version=None):
        BaseTypeReader.__init__(self, stream=stream, version=version)
        TypeReaderPlugin.__init__(self)
        self.nullable_char_reader = self.stream.get_type_reader(generic_reader_name(NullableReader, [CharReader]))

    def init_reader(self):
        BaseTypeReader.init_reader(self)
        self.nullable_char_reader.init_reader()
        self.nullable_char_reader.readers[0].init_reader()

    def read(self):
        texture = self.stream.read_object(Texture2DReader)
        glyphs = self.stream.read_object(ListReader, [RectangleReader])
        cropping = self.stream.read_object(ListReader, [RectangleReader])
        char_map = self.stream.read_object(ListReader, [CharReader])
        v_space = self.stream.read_int32()
        h_space = self.stream.read_single()
        kerning = self.stream.read_object(ListReader, [Vector3Reader])
        default_char = self.nullable_char_reader.read()
        return texture, glyphs, cropping, char_map, v_space, h_space, kerning, default_char


class ModelReader(BaseTypeReader, TypeReaderPlugin):
    target_type = u'Microsoft.Xna.Framework.Graphics.Model'
    reader_name = u'Microsoft.Xna.Framework.Content.ModelReader'


class PrimitiveTypeReader(ValueTypeReader, TypeReaderPlugin):
    target_type = u'Microsoft.Xna.Framework.Graphics.PrimitiveType'
    reader_name = u'Microsoft.Xna.Framework.Content.PrimitiveTypeReader'

    def read(self):
        return self.stream.read_int32()

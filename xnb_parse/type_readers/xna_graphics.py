"""
graphics type readers
"""

from xnb_parse.type_reader import BaseTypeReader, ValueTypeReader, ReaderError, generic_reader_name
from xnb_parse.type_reader_manager import TypeReaderPlugin
from xnb_parse.xna_types.xna_graphics import Texture2D, Texture3D, TextureCube, CUBE_SIDES, IndexBuffer, Effect
from xnb_parse.type_readers.xna_system import ExternalReferenceReader, NullableReader, ListReader
from xnb_parse.type_readers.xna_math import Vector3Reader, RectangleReader
from xnb_parse.type_readers.xna_primitive import CharReader


class TextureReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.Graphics.Texture'
    reader_name = 'Microsoft.Xna.Framework.Content.TextureReader'

    def read(self):
        raise ReaderError("TextureReader should never be invoked directly")


class Texture2DReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.Graphics.Texture2D'
    reader_name = 'Microsoft.Xna.Framework.Content.Texture2DReader'

    def read(self):
        texture_format = self.stream.read('s4')
        width = self.stream.read('u4')
        height = self.stream.read('u4')
        mip_count = self.stream.read('u4')
        mip_levels = []
        for _ in range(mip_count):
            data_size = self.stream.read('u4')
            data = self.stream.pull(data_size)
            mip_levels.append(data)
        return Texture2D(texture_format, width, height, mip_levels)


class Texture3DReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.Graphics.Texture3D'
    reader_name = 'Microsoft.Xna.Framework.Content.Texture3DReader'

    def read(self):
        texture_format = self.stream.read('s4')
        width = self.stream.read('u4')
        height = self.stream.read('u4')
        depth = self.stream.read('u4')
        mip_count = self.stream.read('u4')
        mip_levels = []
        for _ in range(mip_count):
            data_size = self.stream.read('u4')
            data = self.stream.pull(data_size)
            mip_levels.append(data)
        return Texture3D(texture_format, width, height, depth, mip_levels)


class TextureCubeReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.Graphics.TextureCube'
    reader_name = 'Microsoft.Xna.Framework.Content.TextureCubeReader'

    def read(self):
        texture_format = self.stream.read('s4')
        texture_size = self.stream.read('u4')
        mip_count = self.stream.read('u4')
        sides = {}
        for side in CUBE_SIDES:
            mip_levels = []
            for _ in range(mip_count):
                data_size = self.stream.read('u4')
                data = self.stream.pull(data_size)
                mip_levels.append(data)
            sides[side] = mip_levels
        return TextureCube(texture_format, texture_size, sides)


class IndexBufferReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.Graphics.IndexBuffer'
    reader_name = 'Microsoft.Xna.Framework.Content.IndexBufferReader'

    def read(self):
        index_16 = self.stream.read('?')
        index_size = self.stream.read('u4')
        index_data = self.stream.pull(index_size)
        return IndexBuffer(index_16, index_data)


class VertexBufferReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.Graphics.VertexBuffer'
    reader_name = 'Microsoft.Xna.Framework.Content.VertexBufferReader'

    def __init__(self, stream=None, version=None):
        BaseTypeReader.__init__(self, stream=stream, version=version)
        TypeReaderPlugin.__init__(self)
        self.vertexdec_reader = self.stream.get_type_reader(VertexDeclarationReader)

    def init_reader(self):
        BaseTypeReader.init_reader(self)
        self.vertexdec_reader.init_reader()

    def read(self):
        vertex_dec = self.vertexdec_reader.read()
        vertex_count = self.stream.read('u4')
        vertex_data = self.stream.pull(vertex_dec[0] * vertex_count)
        return vertex_dec, vertex_data


class VertexDeclarationReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.Graphics.VertexDeclaration'
    reader_name = 'Microsoft.Xna.Framework.Content.VertexDeclarationReader'

    def read(self):
        stride = self.stream.read('u4')
        element_count = self.stream.read('s4')
        elements = []
        for _ in range(element_count):
            offset = self.stream.read('u4')
            format_ = self.stream.read('s4')
            usage = self.stream.read('s4')
            usage_index = self.stream.read('u4')
            element = offset, format_, usage, usage_index
            elements.append(element)
        return stride, elements


class EffectReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.Graphics.Effect'
    reader_name = 'Microsoft.Xna.Framework.Content.EffectReader'

    def read(self):
        effect_size = self.stream.read('u4')
        effect_data = self.stream.pull(effect_size)
        return Effect(effect_data)


class EffectMaterialReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.Graphics.EffectMaterial'
    reader_name = 'Microsoft.Xna.Framework.Content.EffectMaterialReader'

    def __init__(self, stream=None, version=None):
        BaseTypeReader.__init__(self, stream=stream, version=version)
        TypeReaderPlugin.__init__(self)
        self.externalref_reader = self.stream.get_type_reader(ExternalReferenceReader)

    def init_reader(self):
        BaseTypeReader.init_reader(self)
        self.externalref_reader.init_reader()

    def read(self):
        effect = self.externalref_reader.read()
        parameters = self.stream.read_object()
        return effect, parameters


class BasicEffectReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.Graphics.BasicEffect'
    reader_name = 'Microsoft.Xna.Framework.Content.BasicEffectReader'

    def __init__(self, stream=None, version=None):
        BaseTypeReader.__init__(self, stream=stream, version=version)
        TypeReaderPlugin.__init__(self)
        self.externalref_reader = self.stream.get_type_reader(ExternalReferenceReader)
        self.vector3_reader = self.stream.get_type_reader(Vector3Reader)

    def init_reader(self):
        BaseTypeReader.init_reader(self)
        self.externalref_reader.init_reader()
        self.vector3_reader.init_reader()

    def read(self):
        texture = self.externalref_reader.read()
        colour_d = self.vector3_reader.read()
        colour_e = self.vector3_reader.read()
        colour_s = self.vector3_reader.read()
        spec = self.stream.read('f')
        alpha = self.stream.read('f')
        colour_v = self.stream.read('?')
        return texture, colour_d, colour_e, colour_s, spec, alpha, colour_v


class AlphaTestEffectReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.Graphics.AlphaTestEffect'
    reader_name = 'Microsoft.Xna.Framework.Content.AlphaTestEffectReader'

    def __init__(self, stream=None, version=None):
        BaseTypeReader.__init__(self, stream=stream, version=version)
        TypeReaderPlugin.__init__(self)
        self.externalref_reader = self.stream.get_type_reader(ExternalReferenceReader)
        self.vector3_reader = self.stream.get_type_reader(Vector3Reader)

    def init_reader(self):
        BaseTypeReader.init_reader(self)
        self.externalref_reader.init_reader()
        self.vector3_reader.init_reader()

    def read(self):
        texture = self.externalref_reader.read()
        compare = self.stream.read('s4')
        ref_alpha = self.stream.read('u4')
        colour_d = self.vector3_reader.read()
        alpha = self.stream.read('f')
        colour_v = self.stream.read('?')
        return texture, compare, ref_alpha, colour_d, alpha, colour_v


class DualTextureEffectReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.Graphics.DualTextureEffect'
    reader_name = 'Microsoft.Xna.Framework.Content.DualTextureEffectReader'

    def __init__(self, stream=None, version=None):
        BaseTypeReader.__init__(self, stream=stream, version=version)
        TypeReaderPlugin.__init__(self)
        self.externalref_reader = self.stream.get_type_reader(ExternalReferenceReader)
        self.vector3_reader = self.stream.get_type_reader(Vector3Reader)

    def init_reader(self):
        BaseTypeReader.init_reader(self)
        self.externalref_reader.init_reader()
        self.vector3_reader.init_reader()

    def read(self):
        texture1 = self.externalref_reader.read()
        texture2 = self.externalref_reader.read()
        colour_d = self.vector3_reader.read()
        alpha = self.stream.read('f')
        colour_v = self.stream.read('?')
        return texture1, texture2, colour_d, alpha, colour_v


class EnvironmentMapEffect(BaseTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.Graphics.EnvironmentMapEffect'
    reader_name = 'Microsoft.Xna.Framework.Content.EnvironmentMapEffectReader'

    def __init__(self, stream=None, version=None):
        BaseTypeReader.__init__(self, stream=stream, version=version)
        TypeReaderPlugin.__init__(self)
        self.externalref_reader = self.stream.get_type_reader(ExternalReferenceReader)
        self.vector3_reader = self.stream.get_type_reader(Vector3Reader)

    def init_reader(self):
        BaseTypeReader.init_reader(self)
        self.externalref_reader.init_reader()
        self.vector3_reader.init_reader()

    def read(self):
        texture = self.externalref_reader.read()
        env_texture = self.externalref_reader.read()
        env_amount = self.stream.read('f')
        env_spec = self.vector3_reader.read()
        fresnel = self.stream.read('f')
        colour_d = self.vector3_reader.read()
        colour_e = self.vector3_reader.read()
        alpha = self.stream.read('f')
        return texture, env_texture, env_amount, env_spec, fresnel, colour_d, colour_e, alpha


class SkinnedEffect(BaseTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.Graphics.SkinnedEffect'
    reader_name = 'Microsoft.Xna.Framework.Content.SkinnedEffectReader'

    def __init__(self, stream=None, version=None):
        BaseTypeReader.__init__(self, stream=stream, version=version)
        TypeReaderPlugin.__init__(self)
        self.externalref_reader = self.stream.get_type_reader(ExternalReferenceReader)
        self.vector3_reader = self.stream.get_type_reader(Vector3Reader)

    def init_reader(self):
        BaseTypeReader.init_reader(self)
        self.externalref_reader.init_reader()
        self.vector3_reader.init_reader()

    def read(self):
        texture = self.externalref_reader.read()
        weights = self.stream.read('u4')
        colour_d = self.vector3_reader.read()
        colour_e = self.vector3_reader.read()
        colour_s = self.vector3_reader.read()
        spec_pow = self.stream.read('f')
        alpha = self.stream.read('f')
        return texture, weights, colour_d, colour_e, colour_s, spec_pow, alpha


class SpriteFontReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.Graphics.SpriteFont'
    reader_name = 'Microsoft.Xna.Framework.Content.SpriteFontReader'

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
        v_space = self.stream.read('s4')
        h_space = self.stream.read('f')
        kerning = self.stream.read_object(ListReader, [Vector3Reader])
        default_char = self.nullable_char_reader.read()
        return texture, glyphs, cropping, char_map, v_space, h_space, kerning, default_char


class ModelReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.Graphics.Model'
    reader_name = 'Microsoft.Xna.Framework.Content.ModelReader'


class PrimitiveTypeReader(ValueTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.Graphics.PrimitiveType'
    reader_name = 'Microsoft.Xna.Framework.Content.PrimitiveTypeReader'

    def read(self):
        return self.stream.read('u4')

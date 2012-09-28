"""
graphics type readers
"""

from xnb_parse.type_reader import BaseTypeReader, ReaderError
from xnb_parse.type_reader_manager import TypeReaderPlugin
from xnb_parse.xna_types.xna_graphics import Texture2D, Texture3D, TextureCube, CUBE_SIDES, IndexBuffer, Effect
from xnb_parse.type_readers.xna_system import ExternalReferenceReader
from xnb_parse.type_readers.xna_math import Vector3Reader


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


class VertexDeclarationReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.Graphics.VertexDeclaration'
    reader_name = 'Microsoft.Xna.Framework.Content.VertexDeclarationReader'


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


class BasicEffectReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.Graphics.BasicEffect'
    reader_name = 'Microsoft.Xna.Framework.Content.BasicEffectReader'

    def read(self):
        texture = ExternalReferenceReader.read_from(self.stream)
        colour_d = Vector3Reader.read_from(self.stream)
        colour_e = Vector3Reader.read_from(self.stream)
        colour_s = Vector3Reader.read_from(self.stream)
        spec = self.stream.read('f')
        alpha = self.stream.read('f')
        colour_v = self.stream.read('?')


class AlphaTestEffectReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.Graphics.AlphaTestEffect'
    reader_name = 'Microsoft.Xna.Framework.Content.AlphaTestEffectReader'

    def read(self):
        texture = ExternalReferenceReader.read_from(self.stream)
        compare = self.stream.read('s4')
        ref_alpha = self.stream.read('u4')
        colour_d = Vector3Reader.read_from(self.stream)
        alpha = self.stream.read('f')
        colour_v = self.stream.read('?')


class DualTextureEffectReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.Graphics.DualTextureEffect'
    reader_name = 'Microsoft.Xna.Framework.Content.DualTextureEffectReader'

    def read(self):
        texture1 = ExternalReferenceReader.read_from(self.stream)
        texture2 = ExternalReferenceReader.read_from(self.stream)
        colour_d = Vector3Reader.read_from(self.stream)
        alpha = self.stream.read('f')
        colour_v = self.stream.read('?')


class EnvironmentMapEffect(BaseTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.Graphics.EnvironmentMapEffect'
    reader_name = 'Microsoft.Xna.Framework.Content.EnvironmentMapEffectReader'


class SkinnedEffect(BaseTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.Graphics.SkinnedEffect'
    reader_name = 'Microsoft.Xna.Framework.Content.SkinnedEffectReader'


class SpriteFontReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.Graphics.SpriteFont'
    reader_name = 'Microsoft.Xna.Framework.Content.SpriteFontReader'

    def read(self):
        texture = self.stream.read_object('Microsoft.Xna.Framework.Graphics.Texture2D')
        glyphs = self.stream.read_object()
        cropping = self.stream.read_object()
        char_map = self.stream.read_object()
        v_space = self.stream.read('s4')
        h_space = self.stream.read('f')
        default_char = self.stream.read('c')


class Model(BaseTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.Graphics.Model'
    reader_name = 'Microsoft.Xna.Framework.Content.ModelReader'

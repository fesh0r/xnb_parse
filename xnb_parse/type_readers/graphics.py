"""
graphics type readers
"""

from xnb_parse.type_reader import BaseTypeReader, ReaderError
from xnb_parse.type_reader_manager import TypeReaderPlugin
from xnb_parse.xnb_types.graphics import Texture2D, Texture3D


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

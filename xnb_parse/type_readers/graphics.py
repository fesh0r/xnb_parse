"""
graphics types
"""

from xnb_parse.type_reader import BaseTypeReader, ReaderError
from xnb_parse.type_reader_manager import TypeReaderPlugin


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


class Texture2D(object):
    def __init__(self, texture_format, width, height, mip_levels):
        self.texture_format = texture_format
        self.width = width
        self.height = height
        self.mip_levels = mip_levels

    def __str__(self):
        return 'Texture2D f%d d%dx%d m%d s%d' % (self.texture_format, self.width, self.height, len(self.mip_levels),
                                                 len(self.mip_levels[0]))


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


class Texture3D(object):
    def __init__(self, texture_format, width, height, depth, mip_levels):
        self.texture_format = texture_format
        self.width = width
        self.height = height
        self.depth = depth
        self.mip_levels = mip_levels

    def __str__(self):
        return 'Texture3D f%d d%dx%dx%d m%d s%d' % (self.texture_format, self.width, self.height, self.depth,
                                                    len(self.mip_levels), len(self.mip_levels[0]))

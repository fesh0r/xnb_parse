"""
graphics types
"""


CUBE_SIDES = ['+x', '-x', '+y', '-y', '+z', '-z']


class Texture2D(object):
    def __init__(self, texture_format, width, height, mip_levels):
        self.texture_format = texture_format
        self.width = width
        self.height = height
        self.mip_levels = mip_levels

    def __str__(self):
        return "Texture2D f:%d d:%dx%d m:%d s:%d" % (self.texture_format, self.width, self.height, len(self.mip_levels),
                                                     len(self.mip_levels[0]))


class Texture3D(object):
    def __init__(self, texture_format, width, height, depth, mip_levels):
        self.texture_format = texture_format
        self.width = width
        self.height = height
        self.depth = depth
        self.mip_levels = mip_levels

    def __str__(self):
        return "Texture3D f:%d d:%dx%dx%d m:%d s:%d" % (self.texture_format, self.width, self.height, self.depth,
                                                        len(self.mip_levels), len(self.mip_levels[0]))


class TextureCube(object):
    def __init__(self, texture_format, texture_size, sides):
        self.texture_format = texture_format
        self.texture_size = texture_size
        self.sides = sides

    def __str__(self):
        return "TextureCube f:%d d:%d m:%d s:%d" % (self.texture_format, self.texture_size, len(self.sides['+x']),
                                                    len(self.sides['+x'][0]))


class IndexBuffer(object):
    def __init__(self, index_16, index_data):
        self.index_16 = index_16
        self.index_data = index_data

    def __str__(self):
        return "IndexBuffer t:%d s:%d" % (16 if self.index_16 else 32, len(self.index_data))


class Effect(object):
    def __init__(self, effect_data):
        self.effect_data = effect_data

    def __str__(self):
        return "Effect s:%d" % len(self.effect_data)

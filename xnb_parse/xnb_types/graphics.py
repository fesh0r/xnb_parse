"""
graphics types
"""


class Texture2D(object):
    def __init__(self, texture_format, width, height, mip_levels):
        self.texture_format = texture_format
        self.width = width
        self.height = height
        self.mip_levels = mip_levels

    def __str__(self):
        return 'Texture2D f%d d%dx%d m%d s%d' % (self.texture_format, self.width, self.height, len(self.mip_levels),
                                                 len(self.mip_levels[0]))


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

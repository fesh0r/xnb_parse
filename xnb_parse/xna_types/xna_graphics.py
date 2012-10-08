"""
graphics types
"""

import os

from xnb_parse.xnb_reader import VERSION_40, XNBReader
from xnb_parse.type_reader import ReaderError
from xnb_parse.xna_types.xna_primitive import Enum
from xnb_parse.file_formats import png


def decode_color(data, width, height):
    stride = width * 4
    if len(data) != stride * height:
        raise ReaderError("Texture data length incorrect for Color: %d != %d", (len(data), stride * height))
    return chunk_data(data, stride)


def chunk_data(data, size):
    return (data[pos:pos + size] for pos in xrange(0, len(data), size))


CUBE_SIDES = ['+x', '-x', '+y', '-y', '+z', '-z']
FORMAT_COLOR = 1
SURFACE_FORMAT = {
    1: ('Color', decode_color),
    2: ('Bgr32', None),
    3: ('Bgra1010102', None),
    4: ('Rgba32', None),
    5: ('Rgb32', None),
    6: ('Rgba1010102', None),
    7: ('Rg32', None),
    8: ('Rgba64', None),
    9: ('Bgr565', None),
    10: ('Bgra5551', None),
    11: ('Bgr555', None),
    12: ('Bgra4444', None),
    13: ('Bgr444', None),
    14: ('Bgra2338', None),
    15: ('Alpha8', None),
    16: ('Bgr233', None),
    17: ('Bgr24', None),
    18: ('NormalizedByte2', None),
    19: ('NormalizedByte4', None),
    20: ('NormalizedShort2', None),
    21: ('NormalizedShort4', None),
    22: ('Single', None),
    23: ('Vector2', None),
    24: ('Vector4', None),
    25: ('HalfSingle', None),
    26: ('HalfVector2', None),
    27: ('HalfVector4', None),
    28: ('Dxt1', None),
    29: ('Dxt2', None),
    30: ('Dxt3', None),
    31: ('Dxt4', None),
    32: ('Dxt5', None),
    33: ('Luminance8', None),
    34: ('Luminance16', None),
    35: ('LuminanceAlpha8', None),
    36: ('LuminanceAlpha16', None),
    37: ('Palette8', None),
    38: ('PaletteAlpha16', None),
    39: ('NormalizedLuminance16', None),
    40: ('NormalizedLuminance32', None),
    41: ('NormalizedAlpha1010102', None),
    42: ('NormalizedByte2Computed', None),
    43: ('VideoYuYv', None),
    44: ('VideoUyVy', None),
    45: ('VideoGrGb', None),
    46: ('VideoRgBg', None),
    47: ('Multi2Bgra32', None),
    48: ('Depth24Stencil8', None),
    49: ('Depth24Stencil8Single', None),
    50: ('Depth24Stencil4', None),
    51: ('Depth24', None),
    52: ('Depth32', None),
    54: ('Depth16', None),
    56: ('Depth15Stencil1', None),
}
FORMAT4_COLOR = 0
SURFACE_FORMAT4 = {
    0: ('Color', decode_color),
    1: ('Bgr565', None),
    2: ('Bgra5551', None),
    3: ('Bgra4444', None),
    4: ('Dxt1', None),
    5: ('Dxt3', None),
    6: ('Dxt5', None),
    7: ('NormalizedByte2', None),
    8: ('NormalizedByte4', None),
    9: ('Rgba1010102', None),
    10: ('Rg32', None),
    11: ('Rgba64', None),
    12: ('Alpha8', None),
    13: ('Single', None),
    14: ('Vector2', None),
    15: ('Vector4', None),
    16: ('HalfSingle', None),
    17: ('HalfVector2', None),
    18: ('HalfVector4', None),
    19: ('HdrBlendable', None),
}


class SurfaceFormat(Enum):
    enum_values = dict((k, v[0]) for (k, v) in SURFACE_FORMAT.iteritems())

    @property
    def reader(self):
        return SURFACE_FORMAT[self.value][1]


class SurfaceFormat4(Enum):
    enum_values = dict((k, v[0]) for (k, v) in SURFACE_FORMAT4.iteritems())

    @property
    def reader(self):
        return SURFACE_FORMAT4[self.value][1]


def get_texture_format(xna_version, texture_format):
    try:
        if xna_version >= VERSION_40:
            return SurfaceFormat4(texture_format)
        else:
            return SurfaceFormat(texture_format)
    except KeyError:
        raise ReaderError("Invalid texture format for V%s: %d" % (XNBReader.versions[xna_version], texture_format))


class Texture2D(object):
    def __init__(self, texture_format, width, height, mip_levels):
        self.texture_format = texture_format
        self.width = width
        self.height = height
        self.mip_levels = mip_levels

    def __str__(self):
        return "Texture2D f:%s d:%dx%d m:%d s:%d" % (self.texture_format.name, self.width, self.height,
                                                     len(self.mip_levels), len(self.mip_levels[0]))

    def export(self, filename):
        if self.texture_format.reader:
            out_png = png.Writer(width=self.width, height=self.height)
            out_dir = os.path.dirname(filename)
            if not os.path.isdir(out_dir):
                os.makedirs(out_dir)
            with open(filename + '.png', 'wb') as out_handle:
                rows = self.texture_format.reader(self.mip_levels[0], self.width, self.height)
                out_png.write_packed(out_handle, rows)


class Texture3D(object):
    def __init__(self, texture_format, width, height, depth, mip_levels):
        self.texture_format = texture_format
        self.width = width
        self.height = height
        self.depth = depth
        self.mip_levels = mip_levels

    def __str__(self):
        return "Texture3D f:%s d:%dx%dx%d m:%d s:%d" % (self.texture_format.name, self.width, self.height, self.depth,
                                                        len(self.mip_levels), len(self.mip_levels[0]))


class TextureCube(object):
    def __init__(self, texture_format, texture_size, sides):
        self.texture_format = texture_format
        self.texture_size = texture_size
        self.sides = sides

    def __str__(self):
        return "TextureCube f:%s d:%d m:%d s:%d" % (self.texture_format.name, self.texture_size, len(self.sides['+x']),
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

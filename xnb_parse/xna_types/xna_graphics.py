"""
graphics types
"""

from __future__ import print_function

import os

from xnb_parse.type_reader import ReaderError
from xnb_parse.xna_types.xna_primitive import Enum
from xnb_parse.file_formats.png import write_png
from xnb_parse.file_formats.xml_utils import ET
from xnb_parse.file_formats.img_decode import decode_bgra, decode_rgba, decode_a, decode_dxt1, decode_dxt3, decode_dxt5


VERSION_31 = 4
VERSION_40 = 5
CUBE_SIDES = ['+x', '-x', '+y', '-y', '+z', '-z']
FORMAT_COLOR = 1
SURFACE_FORMAT = {
    1: ('Color', decode_bgra),
    2: ('Bgr32', None),
    3: ('Bgra1010102', None),
    4: ('Rgba32', decode_rgba),
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
    15: ('Alpha8', decode_a),
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
    28: ('Dxt1', decode_dxt1),
    29: ('Dxt2', None),
    30: ('Dxt3', decode_dxt3),
    31: ('Dxt4', None),
    32: ('Dxt5', decode_dxt5),
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
    0: ('Color', decode_rgba),
    1: ('Bgr565', None),
    2: ('Bgra5551', None),
    3: ('Bgra4444', None),
    4: ('Dxt1', decode_dxt1),
    5: ('Dxt3', decode_dxt3),
    6: ('Dxt5', decode_dxt5),
    7: ('NormalizedByte2', None),
    8: ('NormalizedByte4', None),
    9: ('Rgba1010102', None),
    10: ('Rg32', None),
    11: ('Rgba64', None),
    12: ('Alpha8', decode_a),
    13: ('Single', None),
    14: ('Vector2', None),
    15: ('Vector4', None),
    16: ('HalfSingle', None),
    17: ('HalfVector2', None),
    18: ('HalfVector4', None),
    19: ('HdrBlendable', None),
}


class SurfaceFormat(Enum):
    __slots__ = ()
    enum_values = {k: v[0] for k, v in SURFACE_FORMAT.items()}

    @property
    def reader(self):
        return SURFACE_FORMAT[self.value][1]


class SurfaceFormat4(Enum):
    __slots__ = ()
    enum_values = {k: v[0] for k, v in SURFACE_FORMAT4.items()}

    @property
    def reader(self):
        return SURFACE_FORMAT4[self.value][1]


def get_surface_format(xna_version, surface_format):
    try:
        if xna_version >= VERSION_40:
            return SurfaceFormat4(surface_format)
        else:
            return SurfaceFormat(surface_format)
    except KeyError:
        raise ReaderError("Invalid surface format for V{}: {}".format(xna_version, surface_format))


class Texture2D(object):
    def __init__(self, surface_format, width, height, mip_levels, needs_swap=False):
        self.surface_format = surface_format
        self.width = width
        self.height = height
        self.mip_levels = mip_levels
        self.needs_swap = needs_swap

    def __str__(self):
        return "Texture2D f:{} d:{}x{} m:{} s:{}".format(self.surface_format, self.width, self.height,
                                                         len(self.mip_levels), len(self.mip_levels[0]))

    def export(self, filename):
        if not self.surface_format.reader:
            raise ReaderError("No decoder found: '{}'".format(self.surface_format))
        dirname = os.path.dirname(filename)
        if not os.path.isdir(dirname):
            os.makedirs(dirname)

        # hack for ArtObject/TrileSet alpha channel
        alpha = 'yes'
        if 'art objects' in filename or 'trile sets' in filename:
            alpha = 'no'
            rows = self.surface_format.reader(self.mip_levels[0], self.width, self.height, self.needs_swap,
                                              alpha='only')
            write_png(filename + '_alpha', self.width, self.height, rows)
        rows = self.surface_format.reader(self.mip_levels[0], self.width, self.height, self.needs_swap, alpha=alpha)
        write_png(filename, self.width, self.height, rows)

    def full_data(self, alpha='yes'):
        if not self.surface_format.reader:
            raise ReaderError("No decoder found: '{}'".format(self.surface_format))

        rows = self.surface_format.reader(self.mip_levels[0], self.width, self.height, self.needs_swap, alpha=alpha)
        data = bytearray()
        for row in rows:
            data.extend(row)
        return bytes(data)


class Texture3D(object):
    def __init__(self, surface_format, width, height, depth, mip_levels, needs_swap=False):
        self.surface_format = surface_format
        self.width = width
        self.height = height
        self.depth = depth
        self.mip_levels = mip_levels
        self.needs_swap = needs_swap

    def __str__(self):
        return "Texture3D f:{} d:{}x{}x{} m:{} s:{}".format(self.surface_format, self.width, self.height, self.depth,
                                                            len(self.mip_levels), len(self.mip_levels[0]))


class TextureCube(object):
    def __init__(self, surface_format, texture_size, sides, needs_swap=False):
        self.surface_format = surface_format
        self.texture_size = texture_size
        self.sides = sides
        self.needs_swap = needs_swap

    def __str__(self):
        return "TextureCube f:{} d:{} m:{} s:{}".format(self.surface_format, self.texture_size, len(self.sides['+x']),
                                                        len(self.sides['+x'][0]))


class IndexBuffer(object):
    def __init__(self, index_16, index_data):
        self.index_16 = index_16
        self.index_data = index_data

    def __str__(self):
        return "IndexBuffer t:{} s:{}".format(16 if self.index_16 else 32, len(self.index_data))


class Effect(object):
    def __init__(self, effect_data):
        self.effect_data = effect_data

    def __str__(self):
        return "Effect s:{}".format(len(self.effect_data))

    def export(self, filename):
        out_dir = os.path.dirname(filename)
        if not os.path.isdir(out_dir):
            os.makedirs(out_dir)
        with open(filename + '.fxo', 'wb') as out_handle:
            out_handle.write(self.effect_data)


class BasicEffect(object):
    def __init__(self, texture, colour_d, colour_e, colour_s, spec, alpha, colour_v):
        self.texture = texture
        self.colour_d = colour_d
        self.colour_e = colour_e
        self.colour_s = colour_s
        self.spec = spec
        self.alpha = alpha
        self.colour_v = colour_v

    def __str__(self):
        return "BasicEffectReader '{}'".format(self.texture)

    def xml(self, parent):
        if parent is None:
            root = ET.Element('BasicEffect')
        else:
            root = ET.SubElement(parent, 'BasicEffect')
        root.set('spec', str(self.spec))
        root.set('alpha', str(self.alpha))
        root.set('colorV', str(self.colour_v))
        self.texture.xml(ET.SubElement(root, 'Texture'))
        self.colour_d.xml(ET.SubElement(root, 'ColorD'))
        self.colour_e.xml(ET.SubElement(root, 'ColorE'))
        self.colour_s.xml(ET.SubElement(root, 'ColorS'))
        return root


class SpriteFont(object):
    def __init__(self, texture, glyphs, cropping, char_map, v_space, h_space, kerning, default_char):
        self.texture = texture
        self.glyphs = glyphs
        self.cropping = cropping
        self.char_map = char_map
        self.v_space = v_space
        self.h_space = h_space
        self.kerning = kerning
        self.default_char = default_char

    def __str__(self):
        return 'SpriteFont c:{} f:{} d:{}x{}'.format(len(self.glyphs), self.texture.surface_format, self.texture.width,
                                                     self.texture.height)

    def xml(self, parent=None):
        if parent is None:
            root = ET.Element('SpriteFont')
        else:
            root = ET.SubElement(parent, 'SpriteFont')
        root.set('width', str(self.texture.width))
        root.set('height', str(self.texture.height))
        root.set('hSpace', str(self.h_space))
        root.set('vSpace', str(self.v_space))
        if self.default_char is not None:
            root.set('defaultChar', self.default_char)
        if self.glyphs is not None:
            self.glyphs.xml(root, 'Glyphs')
        if self.cropping is not None:
            self.cropping.xml(root, 'Cropping')
        if self.kerning is not None:
            self.kerning.xml(root, 'Kerning')
        if self.char_map is not None:
            self.char_map.xml(root, 'CharMap', 'Char', 'c')
        return root

    def export(self, filename):
        if self.texture is not None:
            self.texture.export(filename)


class PrimitiveType(Enum):
    __slots__ = ()
    enum_values = {1: 'PointList', 2: 'LineList', 3: 'LineStrip', 4: 'TriangleList', 5: 'TriangleStrip',
                   6: 'TriangleFan'}


class PrimitiveType4(Enum):
    __slots__ = ()
    enum_values = {0: 'TriangleList', 1: 'TriangleStrip', 2: 'LineList', 3: 'LineStrip'}

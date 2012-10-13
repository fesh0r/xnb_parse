"""
Decode DXT/other textures to RGBA
"""

import struct

from xnb_parse.type_reader import ReaderError
#from xnb_parse.xna_types.xna_math import Color, Bgr565


def decode_bgra(data, width, height, needs_swap):
    if needs_swap:
        conv = 'argb_rgba'
    else:
        conv = 'bgra_rgba'
    return decode32(data, width, height, conv)


def decode_rgba(data, width, height, needs_swap):
    if needs_swap:
        conv = 'abgr_rgba'
    else:
        conv = 'rgba_rgba'
    return decode32(data, width, height, conv)


def decode32(data, width, height, conv):
    if conv not in ('rgba_rgba', 'abgr_rgba', 'bgra_rgba', 'argb_rgba'):
        raise ReaderError("Unknown conversion: '%s'" % conv)
    stride = width * 4
    expected_len = stride * height
    if len(data) != expected_len:
        raise ReaderError("Invalid data size: %d != %d", (len(data), expected_len))
    for pos in xrange(0, len(data), stride):
        row = bytearray(data[pos:pos + stride])
        if conv == 'bgra_rgba':
            row[2::4], row[1::4], row[0::4], row[3::4] = row[0::4], row[1::4], row[2::4], row[3::4]
        elif conv == 'argb_rgba':
            row[3::4], row[0::4], row[1::4], row[2::4] = row[0::4], row[1::4], row[2::4], row[3::4]
        elif conv == 'abgr_rgba':
            row[3::4], row[2::4], row[1::4], row[0::4] = row[0::4], row[1::4], row[2::4], row[3::4]
        yield row


def decode_a(data, width, height, needs_swap):
    return decode8(data, width, height, 'a_xxxa')


def decode8(data, width, height, conv):
    if conv not in ('a_xxxa',):
        raise ReaderError("Unknown conversion: '%s'" % conv)
    stride = width
    expected_len = stride * height
    if len(data) != expected_len:
        raise ReaderError("Invalid data size: %d != %d", (len(data), expected_len))
    for pos in xrange(0, len(data), stride):
        row = bytearray([0xff] * width * 4)
        row[3::4] = data[pos:pos + stride]
        yield row


def decode_dxt1(data, width, height, needs_swap):
    return DxtDecoder(width, height, 'DXT1', data, needs_swap).decode()


def decode_dxt3(data, width, height, needs_swap):
    return DxtDecoder(width, height, 'DXT3', data, needs_swap).decode()


def decode_dxt5(data, width, height, needs_swap):
    return DxtDecoder(width, height, 'DXT5', data, needs_swap).decode()


class DxtDecoder(object):
    _FORMATS = {'DXT1': 8, 'DXT3': 16, 'DXT5': 16}

    def __init__(self, width, height, surface_format, data, needs_swap=False):
        if surface_format not in self._FORMATS:
            raise ReaderError("Unknown DXT format: '%s'", surface_format)
        if (width | height) & 3:
            raise ReaderError("Bad dimensions for DXT: %dx%d" % (width, height))
        self.width = width
        self.height = height
        self.surface_format = surface_format
        self.data = data
        self.block_size = self._FORMATS[self.surface_format]
        stride = (self.width >> 2) * self.block_size
        expected_len = stride * (self.height >> 2)
        if len(self.data) != expected_len:
            raise ReaderError("Invalid data size for DXT: %d != %d", (len(data), expected_len))
        self.out_rows = [bytearray([0] * self.width * 4), bytearray([0] * self.width * 4),
                         bytearray([0] * self.width * 4), bytearray([0] * self.width * 4)]
        if needs_swap:
            self.rgb_struct = struct.Struct('>HHHH')
            self.ae_struct = struct.Struct('>HHHH')
        else:
            self.rgb_struct = struct.Struct('<HHHH')
            self.ae_struct = struct.Struct('<HHHH')

    def decode(self):
        source_offset = 0
        for cur_y in xrange(0, self.height, 4):
            for cur_x in xrange(0, self.width, 4):
                if self.surface_format == 'DXT3':
                    self.decode_rgb_block(source_offset + 8, cur_x)
                    self.decode_explicit_alpha_block(source_offset, cur_x)
                elif self.surface_format == 'DXT5':
                    self.decode_rgb_block(source_offset + 8, cur_x)
                    self.decode_interpolated_alpha_block(source_offset, cur_x)
                else:
                    self.decode_rgb_block(source_offset, cur_x, dxt1=True)
                source_offset += self.block_size
            yield self.out_rows[0]
            yield self.out_rows[1]
            yield self.out_rows[2]
            yield self.out_rows[3]

    def decode_rgb_block(self, offset, cur_x, dxt1=False):
        color0_raw, color1_raw, bits0, bits1 = self.rgb_struct.unpack_from(self.data, offset)
        bits = bits0 | bits1 << 16
#        color0 = Color.from_float(Bgr565.from_packed(color0_raw))
#        color1 = Color.from_float(Bgr565.from_packed(color1_raw))
#        colors = [color0.to_bytearray(), color1.to_bytearray()]
#        if color0_raw > color1_raw or not dxt1:
#            colors.append(Color.lerp(color0, color1, 1./3.).to_bytearray())
#            colors.append(Color.lerp(color0, color1, 2./3.).to_bytearray())
#        else:
#            colors.append(Color.lerp(color0, color1, 1./2.).to_bytearray())
#            colors.append(Color(0, 0, 0, 0).to_bytearray())
        r0 = (color0_raw >> 11 & 0x1f) << 3
        g0 = (color0_raw >> 5 & 0x3f) << 2
        b0 = (color0_raw & 0x1f) << 3
        r1 = (color1_raw >> 11 & 0x1f) << 3
        g1 = (color1_raw >> 5 & 0x3f) << 2
        b1 = (color1_raw & 0x1f) << 3
        colors = [[r0, g0, b0, 255], [r1, g1, b1, 255]]
        if color0_raw > color1_raw or not dxt1:
            r2 = int((2 * r0 + r1) / 3)
            g2 = int((2 * g0 + g1) / 3)
            b2 = int((2 * b0 + b1) / 3)
            r3 = int((r0 + 2 * r1) / 3)
            g3 = int((g0 + 2 * g1) / 3)
            b3 = int((b0 + 2 * b1) / 3)
            colors.append([r2, g2, b2, 255])
            colors.append([r3, g3, b3, 255])
        else:
            r2 = int((r0 + r1) / 2)
            g2 = int((g0 + g1) / 2)
            b2 = int((b0 + b1) / 2)
            colors.append([r2, g2, b2, 255])
            colors.append([0, 0, 0, 255])
        for y in range(4):
            for x in range(cur_x << 2, (cur_x + 4) << 2, 4):
                self.out_rows[y][x:x + 4] = colors[bits & 3]
                bits >>= 2

    def decode_explicit_alpha_block(self, offset, cur_x):
        bits0, bits1, bits2, bits3 = self.ae_struct.unpack_from(self.data, offset)
        bits = bits0 | bits1 << 16 | bits2 << 32 | bits3 << 48
        for y in range(4):
            for x in range(cur_x << 2, (cur_x + 4) << 2, 4):
                self.out_rows[y][x + 3] = (bits & 0xf) * 17
                bits >>= 4

    def decode_interpolated_alpha_block(self, offset, cur_x):
        pass

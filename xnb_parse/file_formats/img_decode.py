"""
Decode DXT/other textures to RGBA
"""

from __future__ import print_function

from struct import Struct

from xnb_parse.type_reader import ReaderError


def decode_bgra(data, width, height, needs_swap, alpha='yes'):
    if needs_swap:
        conv = 'argb_rgba'
    else:
        conv = 'bgra_rgba'
    return decode32(data, width, height, conv, alpha=alpha)


def decode_rgba(data, width, height, needs_swap, alpha='yes'):
    if needs_swap:
        conv = 'abgr_rgba'
    else:
        conv = 'rgba_rgba'
    return decode32(data, width, height, conv, alpha=alpha)


def decode32(data, width, height, conv, alpha='yes'):
    if conv not in ('rgba_rgba', 'abgr_rgba', 'bgra_rgba', 'argb_rgba'):
        raise ReaderError("Unknown conversion: '{}'".format(conv))
    if alpha not in ('yes', 'no', 'only'):
        raise ValueError("Invalid alpha parameter: '{}'".format(alpha))
    stride = width * 4
    expected_len = stride * height
    if len(data) != expected_len:
        raise ReaderError("Invalid data size: {} != {}".format(len(data), expected_len))
    full_row_ff = bytearray([0xff] * width)
    for pos in range(0, len(data), stride):
        row = bytearray(data[pos:pos + stride])
        if conv == 'bgra_rgba':
            row[2::4], row[1::4], row[0::4], row[3::4] = row[0::4], row[1::4], row[2::4], row[3::4]
        elif conv == 'argb_rgba':
            row[3::4], row[0::4], row[1::4], row[2::4] = row[0::4], row[1::4], row[2::4], row[3::4]
        elif conv == 'abgr_rgba':
            row[3::4], row[2::4], row[1::4], row[0::4] = row[0::4], row[1::4], row[2::4], row[3::4]
        if alpha == 'no':
            row[3::4] = full_row_ff
        elif alpha == 'only':
            row[0::4] = full_row_ff
            row[1::4] = full_row_ff
            row[2::4] = full_row_ff
        yield row


def decode_a(data, width, height, needs_swap, alpha='yes'):
    return decode8(data, width, height, 'a_xxxa')


def decode8(data, width, height, conv):
    if conv not in ('a_xxxa',):
        raise ReaderError("Unknown conversion: '{}'".format(conv))
    stride = width
    expected_len = stride * height
    if len(data) != expected_len:
        raise ReaderError("Invalid data size: {} != {}".format(len(data), expected_len))
    for pos in range(0, len(data), stride):
        row = bytearray([0xff] * width * 4)
        row[3::4] = data[pos:pos + stride]
        yield row


def decode_dxt1(data, width, height, needs_swap, alpha='yes'):
    return DxtDecoder(width, height, 'DXT1', data, needs_swap).decode(alpha)


def decode_dxt3(data, width, height, needs_swap, alpha='yes'):
    return DxtDecoder(width, height, 'DXT3', data, needs_swap).decode(alpha)


def decode_dxt5(data, width, height, needs_swap, alpha='yes'):
    return DxtDecoder(width, height, 'DXT5', data, needs_swap).decode(alpha)


class DxtDecoder(object):
    _FORMATS = {'DXT1': 8, 'DXT3': 16, 'DXT5': 16}

    def __init__(self, width, height, surface_format, data, needs_swap=False):
        if surface_format not in self._FORMATS:
            raise ReaderError("Unknown DXT format: '{}'".format(surface_format))
        if (width | height) & 3:
            raise ReaderError("Bad dimensions for DXT: {}x{}".format(width, height))
        self.width = width
        self.height = height
        self.surface_format = surface_format
        self.data = data
        self.block_size = self._FORMATS[self.surface_format]
        stride = (self.width >> 2) * self.block_size
        expected_len = stride * (self.height >> 2)
        if len(self.data) != expected_len:
            raise ReaderError("Invalid data size for DXT: {} != {}".format(len(data), expected_len))
        self.out_rows = [bytearray([0] * self.width * 4), bytearray([0] * self.width * 4),
                         bytearray([0] * self.width * 4), bytearray([0] * self.width * 4)]
        if needs_swap:
            self.swap_struct = Struct('>HHHH')
        else:
            self.swap_struct = Struct('<HHHH')

        self.explicit_alphas = []
        for cur_a in range(16):
            self.explicit_alphas.append(cur_a * 17)

    def decode(self, alpha='yes'):
        if alpha not in ('yes', 'no', 'only'):
            raise ValueError("Invalid alpha parameter: '{}'".format(alpha))
        source_offset = 0
        full_row_ff = bytearray([0xff] * self.width)
        for _ in range(0, self.height, 4):
            for cur_x in range(0, self.width, 4):
                if self.surface_format == 'DXT3':
                    self.decode_rgb_block(source_offset + 8, cur_x)
                    self.decode_explicit_alpha_block(source_offset, cur_x)
                elif self.surface_format == 'DXT5':
                    self.decode_rgb_block(source_offset + 8, cur_x)
                    self.decode_interpolated_alpha_block(source_offset, cur_x)
                else:
                    self.decode_rgb_block(source_offset, cur_x, dxt1=True)
                source_offset += self.block_size
            for row in self.out_rows:
                if alpha == 'no':
                    row[3::4] = full_row_ff
                elif alpha == 'only':
                    row[0::4] = full_row_ff
                    row[1::4] = full_row_ff
                    row[2::4] = full_row_ff
            yield self.out_rows[0]
            yield self.out_rows[1]
            yield self.out_rows[2]
            yield self.out_rows[3]

    def decode_rgb_block(self, offset, cur_x, dxt1=False):
        color0_raw, color1_raw, bits0, bits1 = self.swap_struct.unpack_from(self.data, offset)
        bits = bits0 | bits1 << 16
        colors = []
        c_r = color0_raw >> 11 & 0x1f
        color0_r = c_r << 3 | c_r >> 2
        c_g = color0_raw >> 5 & 0x3f
        color0_g = c_g << 2 | c_g >> 4
        c_b = color0_raw & 0x1f
        color0_b = c_b << 3 | c_b >> 2
        colors.append([color0_r, color0_g, color0_b, 255])
        c_r = color1_raw >> 11 & 0x1f
        color1_r = c_r << 3 | c_r >> 2
        c_g = color1_raw >> 5 & 0x3f
        color1_g = c_g << 2 | c_g >> 4
        c_b = color1_raw & 0x1f
        color1_b = c_b << 3 | c_b >> 2
        colors.append([color1_r, color1_g, color1_b, 255])
        if color0_raw > color1_raw or not dxt1:
            c_r = (2 * color0_r + color1_r) // 3
            c_g = (2 * color0_g + color1_g) // 3
            c_b = (2 * color0_b + color1_b) // 3
            colors.append([c_r, c_g, c_b, 255])
            c_r = (color0_r + 2 * color1_r) // 3
            c_g = (color0_g + 2 * color1_g) // 3
            c_b = (color0_b + 2 * color1_b) // 3
            colors.append([c_r, c_g, c_b, 255])
        else:
            c_r = (color0_r + color1_r) // 2
            c_g = (color0_g + color1_g) // 2
            c_b = (color0_b + color1_b) // 2
            colors.append([c_r, c_g, c_b, 255])
            colors.append([0, 0, 0, 0])
        for b_y in range(4):
            for b_x in range(cur_x << 2, (cur_x + 4) << 2, 4):
                self.out_rows[b_y][b_x:b_x + 4] = colors[bits & 3]
                bits >>= 2

    def decode_explicit_alpha_block(self, offset, cur_x):
        bits0, bits1, bits2, bits3 = self.swap_struct.unpack_from(self.data, offset)
        bits = bits0 | bits1 << 16 | bits2 << 32 | bits3 << 48
        for b_y in range(4):
            for b_x in range(cur_x << 2, (cur_x + 4) << 2, 4):
                self.out_rows[b_y][b_x + 3] = self.explicit_alphas[bits & 0xf]
                bits >>= 4

    def decode_interpolated_alpha_block(self, offset, cur_x):
        alpha_raw, bits0, bits1, bits2 = self.swap_struct.unpack_from(self.data, offset)
        bits = bits0 | bits1 << 16 | bits2 << 32
        alphas = []
        alpha0 = alpha_raw & 0xff
        alphas.append(alpha0)
        alpha1 = alpha_raw >> 8
        alphas.append(alpha1)
        if alpha0 > alpha1:
            alphas.append((6 * alpha0 + 1 * alpha1) // 7)
            alphas.append((5 * alpha0 + 2 * alpha1) // 7)
            alphas.append((4 * alpha0 + 3 * alpha1) // 7)
            alphas.append((3 * alpha0 + 4 * alpha1) // 7)
            alphas.append((2 * alpha0 + 5 * alpha1) // 7)
            alphas.append((1 * alpha0 + 6 * alpha1) // 7)
        else:
            alphas.append((4 * alpha0 + 1 * alpha1) // 5)
            alphas.append((3 * alpha0 + 2 * alpha1) // 5)
            alphas.append((2 * alpha0 + 3 * alpha1) // 5)
            alphas.append((1 * alpha0 + 4 * alpha1) // 5)
            alphas.append(0)
            alphas.append(255)
        for b_y in range(4):
            for b_x in range(cur_x << 2, (cur_x + 4) << 2, 4):
                self.out_rows[b_y][b_x + 3] = alphas[bits & 0x7]
                bits >>= 3

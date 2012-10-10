"""
Decode DXT/other textures to RGBA
"""

from xnb_parse.type_reader import ReaderError


def chunk_data(data, size):
    return (bytearray(data[pos:pos + size]) for pos in xrange(0, len(data), size))


def decode_color(data, width, height):
    stride = width * 4
    if len(data) != stride * height:
        raise ReaderError("Surface data length incorrect for Color: %d != %d", (len(data), stride * height))
    return chunk_data(data, stride)


def decode_dxt1(data, width, height):
    raise ReaderError("DXT1 not implemented")


def decode_dxt3(data, width, height):
    raise ReaderError("DXT3 not implemented")


def decode_dxt5(data, width, height):
    raise ReaderError("DXT5 not implemented")

"""
PNG encoder
"""

import struct
import zlib


# The PNG signature.
# http://www.w3.org/TR/PNG/#5PNG-file-signature
_SIGNATURE = struct.pack('8B', 137, 80, 78, 71, 13, 10, 26, 10)


class Writer(object):
    def __init__(self, width=None, height=None):
        if width <= 0 or height <= 0:
            raise ValueError("width and height must be greater than zero")

        # http://www.w3.org/TR/PNG/#7Integers-and-byte-order
        if width > 2 ** 32 - 1 or height > 2 ** 32 - 1:
            raise ValueError("width and height cannot exceed 2**32-1")

        self.width = width
        self.height = height
        self.chunk_limit = 2 ** 20

        self.color_type = 6
        self.planes = 4
        self.stride = self.width * self.planes

    def write_packed(self, outfile, rows):
        # http://www.w3.org/TR/PNG/#5PNG-file-signature
        outfile.write(_SIGNATURE)

        # http://www.w3.org/TR/PNG/#11IHDR
        write_chunk(outfile, 'IHDR', struct.pack("!2I5B", self.width, self.height, 8, self.color_type, 0, 0, 0))

        # http://www.w3.org/TR/PNG/#11IDAT
        compressor = zlib.compressobj()

        data = bytearray()
        for row in rows:
            data.append(0)
            data.extend(rgba_to_bgra(row))
            if len(data) > self.chunk_limit:
                compressed = compressor.compress(str(data))
                if len(compressed):
                    write_chunk(outfile, 'IDAT', compressed)
                data = bytearray()
        if len(data):
            compressed = compressor.compress(str(data))
        else:
            compressed = bytearray()
        flushed = compressor.flush()
        if len(compressed) or len(flushed):
            write_chunk(outfile, 'IDAT', str(compressed + flushed))

        # http://www.w3.org/TR/PNG/#11IEND
        write_chunk(outfile, 'IEND')


def rgba_to_bgra(data):
    fixed_data = bytearray(data)
    fixed_data[0::4], fixed_data[2::4] = fixed_data[2::4], fixed_data[0::4]
#    # kill alpha channel
#    fixed_data[3::4] = [0xff] * (len(data) >> 2)
    return fixed_data


def write_chunk(outfile, tag, data=''):
    # http://www.w3.org/TR/PNG/#5Chunk-layout
    outfile.write(struct.pack("!I", len(data)))
    outfile.write(tag)
    outfile.write(data)
    checksum = zlib.crc32(tag)
    checksum = zlib.crc32(data, checksum)
    checksum &= 2 ** 32 - 1
    outfile.write(struct.pack("!I", checksum))

"""
PNG encoder
"""

from array import array
import struct
import zlib


# The PNG signature.
# http://www.w3.org/TR/PNG/#5PNG-file-signature
_SIGNATURE = struct.pack('8B', 137, 80, 78, 71, 13, 10, 26, 10)


class Writer(object):
    def __init__(self, width=None, height=None, greyscale=False, alpha=False, compression=None, chunk_limit=2 ** 20):
        if width <= 0 or height <= 0:
            raise ValueError("width and height must be greater than zero")

        # http://www.w3.org/TR/PNG/#7Integers-and-byte-order
        if width > 2 ** 32 - 1 or height > 2 ** 32 - 1:
            raise ValueError("width and height cannot exceed 2**32-1")

        self.width = width
        self.height = height
        self.greyscale = bool(greyscale)
        self.alpha = bool(alpha)
        self.compression = compression
        self.chunk_limit = chunk_limit

        self.color_type = 4 * self.alpha + 2 * (not self.greyscale)
        assert self.color_type in (0, 2, 4, 6)

    def write_packed(self, outfile, rows):
        # http://www.w3.org/TR/PNG/#5PNG-file-signature
        outfile.write(_SIGNATURE)

        # http://www.w3.org/TR/PNG/#11IHDR
        write_chunk(outfile, 'IHDR', struct.pack("!2I5B", self.width, self.height, 8, self.color_type, 0, 0, 0))

        # http://www.w3.org/TR/PNG/#11IDAT
        if self.compression is not None:
            compressor = zlib.compressobj(self.compression)
        else:
            compressor = zlib.compressobj()

        data = array('B')
        for row in rows:
            data.append(0)
            data.extend(row)
            if len(data) > self.chunk_limit:
                compressed = compressor.compress(data.tostring())
                if len(compressed):
                    write_chunk(outfile, 'IDAT', compressed)
                data = array('B')
        if len(data):
            compressed = compressor.compress(data.tostring())
        else:
            compressed = ''
        flushed = compressor.flush()
        if len(compressed) or len(flushed):
            write_chunk(outfile, 'IDAT', compressed + flushed)

        # http://www.w3.org/TR/PNG/#11IEND
        write_chunk(outfile, 'IEND')


def write_chunk(outfile, tag, data=''):
    # http://www.w3.org/TR/PNG/#5Chunk-layout
    outfile.write(struct.pack("!I", len(data)))
    outfile.write(tag)
    outfile.write(data)
    checksum = zlib.crc32(tag)
    checksum = zlib.crc32(data, checksum)
    checksum &= 2 ** 32 - 1
    outfile.write(struct.pack("!I", checksum))

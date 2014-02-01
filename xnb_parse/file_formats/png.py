"""
PNG encoder
"""

from __future__ import print_function

import struct
import zlib


class PyPngWriter(object):
    # The PNG signature.
    # http://www.w3.org/TR/PNG/#5PNG-file-signature
    _SIGNATURE = b'\x89PNG\x0d\x0a\x1a\x0a'

    def __init__(self, width=None, height=None):
        if width <= 0 or height <= 0:
            raise ValueError("width and height must be greater than zero")

        # http://www.w3.org/TR/PNG/#7Integers-and-byte-order
        if width > 2 ** 32 - 1 or height > 2 ** 32 - 1:
            raise ValueError("width and height cannot exceed 2**32-1")

        self.width = width
        self.height = height
        self.chunk_limit = 2 ** 20

    def write_bytearray(self, outfile, rows):
        # http://www.w3.org/TR/PNG/#5PNG-file-signature
        outfile.write(PyPngWriter._SIGNATURE)

        # http://www.w3.org/TR/PNG/#11IHDR
        PyPngWriter._write_chunk(outfile, b'IHDR', struct.pack('!II B B BBB', self.width, self.height, 8, 6, 0, 0, 0))

        # http://www.w3.org/TR/PNG/#11IDAT
        compressor = zlib.compressobj()

        data = bytearray()
        for row in rows:
            data.append(0)
            data.extend(row)
            if len(data) > self.chunk_limit:
                compressed = compressor.compress(bytes(data))
                if len(compressed):
                    PyPngWriter._write_chunk(outfile, b'IDAT', compressed)
                data = bytearray()
        if len(data):
            compressed = compressor.compress(bytes(data))
        else:
            compressed = bytes()
        flushed = compressor.flush()
        if len(compressed) or len(flushed):
            PyPngWriter._write_chunk(outfile, b'IDAT', compressed + flushed)

        # http://www.w3.org/TR/PNG/#11IEND
        PyPngWriter._write_chunk(outfile, b'IEND')

    @staticmethod
    def _write_chunk(outfile, tag, data=b''):
        # http://www.w3.org/TR/PNG/#5Chunk-layout
        outfile.write(struct.pack('!I', len(data)))
        outfile.write(tag)
        outfile.write(data)
        checksum = zlib.crc32(tag)
        checksum = zlib.crc32(data, checksum)
        checksum &= 2 ** 32 - 1
        outfile.write(struct.pack('!I', checksum))


def write_png(filename, width, height, rows):
    full_filename = filename + '.png'
    out_png = PyPngWriter(width=width, height=height)
    with open(full_filename, 'wb') as out_handle:
        out_png.write_bytearray(out_handle, rows)

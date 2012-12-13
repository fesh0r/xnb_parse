"""
.NET BinaryStream reader
"""

from __future__ import print_function

import struct
import sys
from io import BytesIO, SEEK_END


_TYPE_FMT = ['Q', 'q', 'I', 'i', 'H', 'h', 'B', 'b', 'f', 'd', '?']


# pylint: disable-msg=W0201
class BinaryStream(BytesIO):
    def __init__(self, data=None, filename=None, big_endian=False):
        if filename is not None:
            with open(filename, 'rb') as file_handle:
                data = file_handle.read()
        BytesIO.__init__(self, data)
        self._types = {k: None for k in _TYPE_FMT}
        self.set_endian(big_endian)

    def set_endian(self, big_endian=False):
        self.big_endian = big_endian
        if self.big_endian:
            self._fmt_end = '>'
        else:
            self._fmt_end = '<'
        self._types = {k: struct.Struct(self._fmt_end + k) for k, v in self._types.items()}

    def peek(self, count):
        cur_pos = self.tell()
        value = self.read(count)
        self.seek(cur_pos)
        return value

    def write_file(self, filename):
        with open(filename, 'wb') as file_handle:
            file_handle.write(self.getvalue())

    def length(self):
        cur_pos = self.tell()
        cur_len = self.seek(0, SEEK_END)
        self.seek(cur_pos)
        return cur_len

    def read_7bit_encoded_int(self):
        value = 0
        shift = 0
        while shift < 32:
            val = self._types['B'].unpack(self.read(1))[0]
            value |= (val & 0x7F) << shift
            if val & 128 == 0:
                return value
            shift += 7
        raise ValueError("Shift out of range")

    def write_7bit_encoded_int(self, value):
        temp = value
        bytes_written = 0
        while temp >= 128:
            self.write(self._types['B'].pack(temp & 0xff | 0x80))
            bytes_written += 1
            temp >>= 7
        self.write(self._types['B'].pack(temp))
        bytes_written += 1
        return bytes_written

    def read_char(self):
        raw_value = self._types['B'].unpack(self.read(1))[0]
        byte_count = 0
        while raw_value & (0x80 >> byte_count):
            byte_count += 1
        raw_value &= (1 << (8 - byte_count)) - 1
        while byte_count > 1:
            raw_value <<= 6
            raw_value |= self._types['B'].unpack(self.read(1))[0] & 0x3f
            byte_count -= 1
        if sys.version < '3':
            #noinspection PyUnresolvedReferences
            return unichr(raw_value)  # pylint: disable-msg=E0602
        else:
            return chr(raw_value)

    def write_char(self, value):
        return self.write(value.encode('utf-8'))

    def read_string(self):
        size = self.read_7bit_encoded_int()
        raw_value = self.read(size)
        return raw_value.decode('utf-8')

    def write_string(self, value):
        raw_value = value.encode('utf-8')
        bytes_written = self.write_7bit_encoded_int(len(raw_value))
        bytes_written += self.write(raw_value)
        return bytes_written

    def read_cstring(self, encoding='utf-8'):
        raw_value = bytearray()
        cur_byte = self.read(1)
        while cur_byte != b'\x00' and cur_byte != b'':
            raw_value += cur_byte
            cur_byte = self.read(1)
        return raw_value.decode(encoding)

    def write_cstring(self, value, encoding='utf-8'):
        raw_value = value.encode(encoding)
        bytes_written = self.write(raw_value)
        bytes_written += self.write_byte(0)
        return bytes_written

    def unpack(self, fmt):
        if fmt not in self._types:
            self._types[fmt] = struct.Struct(self._fmt_end + fmt)
        return self._types[fmt].unpack(self.read(self._types[fmt].size))

    def pack(self, fmt, *values):
        if fmt not in self._types:
            self._types[fmt] = struct.Struct(self._fmt_end + fmt)
        return self.write(self._types[fmt].pack(*values))

    def calc_size(self, fmt):
        if fmt not in self._types:
            self._types[fmt] = struct.Struct(self._fmt_end + fmt)
        return self._types[fmt].size

    def read_byte(self):
        return self._types['B'].unpack(self.read(1))[0]

    def write_byte(self, value):
        return self.write(self._types['B'].pack(value))

    def read_sbyte(self):
        return self._types['b'].unpack(self.read(1))[0]

    def write_sbyte(self, value):
        return self.write(self._types['b'].pack(value))

    def read_int16(self):
        return self._types['h'].unpack(self.read(2))[0]

    def write_int16(self, value):
        return self.write(self._types['h'].pack(value))

    def read_uint16(self):
        return self._types['H'].unpack(self.read(2))[0]

    def write_uint16(self, value):
        return self.write(self._types['H'].pack(value))

    def read_int32(self):
        return self._types['i'].unpack(self.read(4))[0]

    def write_int32(self, value):
        return self.write(self._types['i'].pack(value))

    def read_uint32(self):
        return self._types['I'].unpack(self.read(4))[0]

    def write_uint32(self, value):
        return self.write(self._types['I'].pack(value))

    def read_int64(self):
        return self._types['q'].unpack(self.read(8))[0]

    def write_int64(self, value):
        return self.write(self._types['q'].pack(value))

    def read_uint64(self):
        return self._types['Q'].unpack(self.read(8))[0]

    def write_uint64(self, value):
        return self.write(self._types['Q'].pack(value))

    def read_boolean(self):
        return self._types['?'].unpack(self.read(1))[0]

    def write_boolean(self, value):
        return self.write(self._types['?'].pack(value))

    def read_single(self):
        return self._types['f'].unpack(self.read(4))[0]

    def write_single(self, value):
        return self.write(self._types['f'].pack(value))

    def read_double(self):
        return self._types['d'].unpack(self.read(8))[0]

    def write_double(self, value):
        return self.write(self._types['d'].pack(value))

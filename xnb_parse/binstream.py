# coding=utf-8
"""
.NET BinaryStream reader
"""

from __future__ import print_function

import struct
import sys
from io import BytesIO, SEEK_END


_TYPE_FMT = {
    'u8': 'Q',
    's8': 'q',
    'u4': 'I',
    's4': 'i',
    'u2': 'H',
    's2': 'h',
    'u1': 'B',
    's1': 'b',
    'c1': 'c',
    'f': 'f',
    'd': 'd',
    '?': '?'
}


# pylint: disable-msg=W0201
class BinaryStream(BytesIO):
    def __init__(self, data=None, filename=None, big_endian=False):
        if filename is not None:
            with open(filename, 'rb') as file_handle:
                data = file_handle.read()
        BytesIO.__init__(self, data)
        self.set_endian(big_endian)

    def set_endian(self, big_endian=False):
        self.big_endian = big_endian
        if self.big_endian:
            self._fmt_end = '>'
        else:
            self._fmt_end = '<'
        self._types = {k: struct.Struct(self._fmt_end + v) for k, v in _TYPE_FMT.items()}

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
            val = self.read_byte()
            value |= (val & 0x7F) << shift
            if val & 128 == 0:
                break
            shift += 7
        if shift >= 32:
            raise ValueError("Shift out of range")
        return value

    def write_7bit_encoded_int(self, value):
        temp = value
        bytes_written = 0
        while temp >= 128:
            self.write_byte(temp & 0xff | 0x80)
            bytes_written += 1
            temp >>= 7
        self.write_byte(temp)
        bytes_written += 1
        return bytes_written

    def read_char(self):
        raw_value = self.read_byte()
        byte_count = 0
        while raw_value & (0x80 >> byte_count):
            byte_count += 1
        raw_value &= (1 << (8 - byte_count)) - 1
        while byte_count > 1:
            raw_value <<= 6
            raw_value |= self.read_byte() & 0x3f
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

    def unpack(self, fmt):
        local_struct = struct.Struct(self._fmt_end + fmt)
        raw_value = self.read(local_struct.size)
        return local_struct.unpack(raw_value)

    def pack(self, fmt, *values):
        local_struct = struct.Struct(self._fmt_end + fmt)
        return self.write(local_struct.pack(*values))

    def calc_size(self, fmt):
        return struct.calcsize(self._fmt_end + fmt)

    def _read_struct(self, struct_):
        value, = struct_.unpack(self.read(struct_.size))
        return value

    def _write_struct(self, value, struct_):
        return self.write(struct_.pack(value))

    def read_byte(self):
        return self._read_struct(self._types['u1'])

    def write_byte(self, value):
        return self._write_struct(value, self._types['u1'])

    def read_sbyte(self):
        return self._read_struct(self._types['s1'])

    def write_sbyte(self, value):
        return self._write_struct(value, self._types['s1'])

    def read_cbyte(self):
        return self._read_struct(self._types['c1'])

    def write_cbyte(self, value):
        return self._write_struct(value, self._types['c1'])

    def read_int16(self):
        return self._read_struct(self._types['s2'])

    def write_int16(self, value):
        return self._write_struct(value, self._types['s2'])

    def read_uint16(self):
        return self._read_struct(self._types['u2'])

    def write_uint16(self, value):
        return self._write_struct(value, self._types['u2'])

    def read_int32(self):
        return self._read_struct(self._types['s4'])

    def write_int32(self, value):
        return self._write_struct(value, self._types['s4'])

    def read_uint32(self):
        return self._read_struct(self._types['u4'])

    def write_uint32(self, value):
        return self._write_struct(value, self._types['u4'])

    def read_int64(self):
        return self._read_struct(self._types['s8'])

    def write_int64(self, value):
        return self._write_struct(value, self._types['s8'])

    def read_uint64(self):
        return self._read_struct(self._types['u8'])

    def write_uint64(self, value):
        return self._write_struct(value, self._types['u8'])

    def read_boolean(self):
        return self._read_struct(self._types['?'])

    def write_boolean(self, value):
        return self._write_struct(value, self._types['?'])

    def read_single(self):
        return self._read_struct(self._types['f'])

    def write_single(self, value):
        return self._write_struct(value, self._types['f'])

    def read_double(self):
        return self._read_struct(self._types['d'])

    def write_double(self, value):
        return self._write_struct(value, self._types['d'])

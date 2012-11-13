# coding=utf-8
"""
.NET BinaryStream reader
"""

import struct
from io import BytesIO


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


class BinaryStream(object):
    def __init__(self, big_endian=False):
        self.big_endian = big_endian
        if self.big_endian:
            self._fmt_end = '>'
        else:
            self._fmt_end = '<'
        self._types = {k: struct.Struct(self._fmt_end + v) for k, v in _TYPE_FMT.items()}

    def calc_size(self, fmt):
        return struct.calcsize(self._fmt_end + fmt)

    def size(self, type_):
        return self._types[type_].size


class BinaryWriter(BinaryStream):
    def __init__(self, big_endian=False):
        BinaryStream.__init__(self, big_endian)
        self.stream = BytesIO()

    def _write_struct(self, value, struct_):
        self.stream.write(struct_.pack(value))

    def pack(self, fmt, *values):
        local_struct = struct.Struct(self._fmt_end + fmt)
        self.stream.write(local_struct.pack(*values))

    def serial(self):
        return self.stream.getvalue()

    def write_bytes(self, value):
        self.stream.write(value)

    def write_byte(self, value):
        return self._write_struct(value, self._types['u1'])

    def write_sbyte(self, value):
        return self._write_struct(value, self._types['s1'])

    def write_cbyte(self, value):
        return self._write_struct(value, self._types['c1'])

    def write_int16(self, value):
        return self._write_struct(value, self._types['s2'])

    def write_uint16(self, value):
        return self._write_struct(value, self._types['u2'])

    def write_int32(self, value):
        return self._write_struct(value, self._types['s4'])

    def write_uint32(self, value):
        return self._write_struct(value, self._types['u4'])

    def write_int64(self, value):
        return self._write_struct(value, self._types['s8'])

    def write_uint64(self, value):
        return self._write_struct(value, self._types['u8'])

    def write_boolean(self, value):
        return self._write_struct(value, self._types['?'])

    def write_single(self, value):
        return self._write_struct(value, self._types['f'])

    def write_double(self, value):
        return self._write_struct(value, self._types['d'])

    def write_7bit_encoded_int(self, value):
        temp = value
        while temp >= 128:
            self.write_byte(temp & 0xff | 0x80)
            temp >>= 7
        self.write_byte(temp)

    def write_char(self, value):
        raw_value = value.encode('utf-8')
        self.stream.write(raw_value)

    def write_string(self, value):
        raw_value = value.encode('utf-8')
        self.write_7bit_encoded_int(len(raw_value))
        self.stream.write(raw_value)


class BinaryReader(BinaryStream):
    def __init__(self, data, big_endian=False):
        BinaryStream.__init__(self, big_endian)
        self.data = data
        self._index = 0

    def _read_struct(self, struct_):
        value, = struct_.unpack_from(self.data, self._index)
        self._index += struct_.size
        return value

    def seek(self, offset):
        self._index = offset

    def tell(self):
        return self._index

    def remainder(self):
        rest = self.data[self._index:]
        self._index = len(self.data)
        return rest

    def remaining(self):
        return len(self.data) - self._index

    def unpack(self, fmt):
        local_struct = struct.Struct(self._fmt_end + fmt)
        values = local_struct.unpack_from(self.data, self._index)
        self._index += local_struct.size
        return values

    def read_bytes(self, count):
        value = self.data[self._index:self._index + count]
        self._index += count
        return value

    def read_byte(self):
        return self._read_struct(self._types['u1'])

    def read_sbyte(self):
        return self._read_struct(self._types['s1'])

    def read_cbyte(self):
        return self._read_struct(self._types['c1'])

    def read_int16(self):
        return self._read_struct(self._types['s2'])

    def read_uint16(self):
        return self._read_struct(self._types['u2'])

    def read_int32(self):
        return self._read_struct(self._types['s4'])

    def read_uint32(self):
        return self._read_struct(self._types['u4'])

    def read_int64(self):
        return self._read_struct(self._types['s8'])

    def read_uint64(self):
        return self._read_struct(self._types['u8'])

    def read_boolean(self):
        return self._read_struct(self._types['?'])

    def read_single(self):
        return self._read_struct(self._types['f'])

    def read_double(self):
        return self._read_struct(self._types['d'])

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
        value = chr(raw_value)
        return value

    def read_string(self):
        size = self.read_7bit_encoded_int()
        raw_value = self.read_bytes(size)
        value = raw_value.decode('utf-8')
        return value

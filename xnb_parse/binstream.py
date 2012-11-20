"""
.NET BinaryStream reader
"""

import struct
from io import BytesIO, SEEK_END


_TYPE_FMT = ['Q', 'q', 'I', 'i', 'H', 'h', 'B', 'b', 'c', 'f', 'd', '?']


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
        return self.unpack('B')[0]

    def write_byte(self, value):
        return self.pack('B', value)

    def read_sbyte(self):
        return self.unpack('b')[0]

    def write_sbyte(self, value):
        return self.pack('b', value)

    def read_cbyte(self):
        return self.unpack('c')[0]

    def write_cbyte(self, value):
        return self.pack('c', value)

    def read_int16(self):
        return self.unpack('h')[0]

    def write_int16(self, value):
        return self.pack('h', value)

    def read_uint16(self):
        return self.unpack('H')[0]

    def write_uint16(self, value):
        return self.pack('H', value)

    def read_int32(self):
        return self.unpack('i')[0]

    def write_int32(self, value):
        return self.pack('i', value)

    def read_uint32(self):
        return self.unpack('I')[0]

    def write_uint32(self, value):
        return self.pack('I', value)

    def read_int64(self):
        return self.unpack('q')[0]

    def write_int64(self, value):
        return self.pack('q', value)

    def read_uint64(self):
        return self.unpack('Q')[0]

    def write_uint64(self, value):
        return self.pack('Q', value)

    def read_boolean(self):
        return self.unpack('?')[0]

    def write_boolean(self, value):
        return self.pack('?', value)

    def read_single(self):
        return self.unpack('f')[0]

    def write_single(self, value):
        return self.pack('f', value)

    def read_double(self):
        return self.unpack('d')[0]

    def write_double(self, value):
        return self.pack('d', value)

# coding=utf-8
"""
.NET BinaryStream reader
"""

from __future__ import absolute_import, division, unicode_literals

from struct import Struct, calcsize
from io import BytesIO
from array import array


class BinaryStream(object):
    _type_fmt = {
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

    def __init__(self, big_endian=False):
        self.big_endian = big_endian
        if self.big_endian:
            self._fmt_end = '>'
        else:
            self._fmt_end = '<'
        self._types = {}
        for name, type_ in self._type_fmt.items():
            self._types[name] = Struct(str(self._fmt_end + type_))

    def calc_size(self, fmt):
        return calcsize(str(self._fmt_end + fmt))

    def size(self, type_):
        return self._types[type_].size


class BinaryWriter(BinaryStream):
    def __init__(self, big_endian=False):
        BinaryStream.__init__(self, big_endian)
        self.stream = BytesIO()

    def clear(self):
        self.stream = BytesIO()

    def write(self, value, type_):
        try:
            self.write_struct(value, self._types[type_])
        except KeyError:
            if type_ == 'c':
                self.write_char(value)
            elif type_ == 'str':
                self.write_string(value)
            elif type_ == '7b':
                self.write_7bit_encoded_int(value)
            else:
                raise

    def write_struct(self, value, struct_):
        self.stream.write(struct_.pack(value))

    def pack(self, fmt, *values):
        local_struct = Struct(str(self._fmt_end + fmt))
        self.stream.write(local_struct.pack(*values))

    def extend(self, value):
        self.stream.write(value)

    def serial(self):
        index = self.stream.tell()
        self.stream.seek(0)
        out = self.stream.read()
        self.stream.seek(index)
        return out

    def write_byte(self, value):
        return self.write_struct(value, self._types['u1'])

    def write_sbyte(self, value):
        return self.write_struct(value, self._types['s1'])

    def write_cbyte(self, value):
        return self.write_struct(value, self._types['c1'])

    def write_int16(self, value):
        return self.write_struct(value, self._types['s2'])

    def write_uint16(self, value):
        return self.write_struct(value, self._types['u2'])

    def write_int32(self, value):
        return self.write_struct(value, self._types['s4'])

    def write_uint32(self, value):
        return self.write_struct(value, self._types['u4'])

    def write_int64(self, value):
        return self.write_struct(value, self._types['s8'])

    def write_uint64(self, value):
        return self.write_struct(value, self._types['u8'])

    def write_boolean(self, value):
        return self.write_struct(value, self._types['?'])

    def write_single(self, value):
        return self.write_struct(value, self._types['f'])

    def write_double(self, value):
        return self.write_struct(value, self._types['d'])

    def write_7bit_encoded_int(self, value):
        temp = value
        out = ''
        while temp >= 128:
            out += chr(0x000000FF & (temp | 0x80))
            temp >>= 7
        out += chr(temp)
        self.stream.write(out)

    def write_char(self, value):
        raw_value = value.encode('utf-8')
        self.stream.write(raw_value)

    def write_string(self, value):
        raw_value = value.encode('utf-8')
        self.write_7bit_encoded_int(len(raw_value))
        self.stream.write(raw_value)

    def write_bytes(self, value):
        self.extend(str(value))


class BinaryReader(BinaryStream):
    def __init__(self, data, big_endian=False):
        BinaryStream.__init__(self, big_endian)
        self.data = data
        self._index = 0

    def read(self, type_):
        try:
            value = self.read_struct(self._types[type_])
        except KeyError:
            if type_ == 'c':
                value = self.read_char()
            elif type_ == 'str':
                value = self.read_string()
            elif type_ == '7b':
                value = self.read_7bit_encoded_int()
            else:
                raise
        return value

    def read_struct(self, struct_):
        value, = struct_.unpack_from(self.data, self._index)
        self._index += struct_.size
        return value

    def next(self, count):
        return self.data[self._index:self._index + count]

    def seek(self, offset):
        self._index = offset

    def tell(self):
        return self._index

    def pull(self, count):
        value = self.data[self._index:self._index + count]
        self._index += count
        return value

    def peek(self, type_):
        index = self._index
        value = self.read(type_)
        self._index = index
        return value

    def remainder(self):
        rest = self.data[self._index:]
        self._index = len(self.data)
        return rest

    def remaining(self):
        return len(self.data) - self._index

    def unpack(self, fmt):
        local_struct = Struct(str(self._fmt_end + fmt))
        values = local_struct.unpack_from(self.data, self._index)
        self._index += local_struct.size
        return values

    def read_byte(self):
        return self.read_struct(self._types['u1'])

    def read_sbyte(self):
        return self.read_struct(self._types['s1'])

    def read_cbyte(self):
        return self.read_struct(self._types['c1'])

    def read_int16(self):
        return self.read_struct(self._types['s2'])

    def read_uint16(self):
        return self.read_struct(self._types['u2'])

    def read_int32(self):
        return self.read_struct(self._types['s4'])

    def read_uint32(self):
        return self.read_struct(self._types['u4'])

    def read_int64(self):
        return self.read_struct(self._types['s8'])

    def read_uint64(self):
        return self.read_struct(self._types['u8'])

    def read_boolean(self):
        return self.read_struct(self._types['?'])

    def read_single(self):
        return self.read_struct(self._types['f'])

    def read_double(self):
        return self.read_struct(self._types['d'])

    def read_7bit_encoded_int(self):
        value = 0
        shift = 0
        while shift < 32:
            val = ord(self.pull(1))
            value |= (val & 0x7F) << shift
            if val & 128 == 0:
                break
            shift += 7
        if shift >= 32:
            raise ValueError("Shift out of range")
        return value

    def read_char(self):
        raw_value = ord(self.pull(1))
        byte_count = 0
        while raw_value & (0x80 >> byte_count):
            byte_count += 1
        raw_value &= (1 << (8 - byte_count)) - 1
        while byte_count > 1:
            raw_value <<= 6
            raw_value |= ord(self.pull(1)) & 0x3f
            byte_count -= 1
        value = unichr(raw_value)
        return value

    def read_string(self):
        size = self.read_7bit_encoded_int()
        raw_value = self.pull(size)
        value = raw_value.decode('utf-8')
        return value

    def read_bytes(self, count):
        return self.pull(count)


class ByteSwapper(object):
    _TYPECODES = ['b', 'h', 'l']

    def __init__(self):
        # try and figure out a typecode for 16 and 32 bit values
        self.size_types = {}
        for size in [2, 4]:
            cur_type = None
            for typecode in self._TYPECODES:
                test_array = array(typecode)
                if test_array.itemsize == size:
                    cur_type = typecode
                    break
            if cur_type is None:
                raise ValueError("array typecode not found for size: %d" % size)
            self.size_types[size] = cur_type

    def swap(self, swap_size, data):
        try:
            swap_array = array(self.size_types[swap_size], data)
            swap_array.byteswap()
            data = swap_array.tostring()
        except KeyError:
            raise ValueError("unknown byteswap size: %d", swap_size)
        return data

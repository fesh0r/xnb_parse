"""
.NET BinaryStream reader
"""

import struct


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
        'f': 'f',
        'd': 'd',
        'c': 'c',
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
            self._types[name] = struct.Struct(self._fmt_end + type_)


class BinaryReader(BinaryStream):
    def __init__(self, data, big_endian=False):
        BinaryStream.__init__(self, big_endian)
        self._stream = data
        self._index = 0

    def read(self, type_):
        try:
            value = self._types[type_].unpack_from(self._stream, self._index)[0]
            self._index += self._types[type_].size
        except KeyError:
            if type_ == 'str':
                size = self.read_7bit_int()
                value = self.pull(size)
            elif type_ == '7b':
                value = self.read_7bit_int()
            else:
                raise
        return value

    def next(self, count):
        return self._stream[self._index:self._index + count]

    def pull(self, count):
        value = self._stream[self._index:self._index + count]
        self._index += count
        return value

    def peek(self, type_):
        index = self._index
        value = self.read(type_)
        self._index = index
        return value

    def remainder(self):
        v = self._stream[self._index:]
        self._index = len(self._stream)
        return v

    def unpack(self, fmt):
        s = struct.Struct(self._fmt_end + fmt)
        values = s.unpack_from(self._stream, self._index)
        self._index += s.size
        return values

    def calc_size(self, fmt):
        return struct.calcsize(self._fmt_end + fmt)

    def size(self, type_):
        return self._types[type_].size

    def read_7bit_int(self):
        value = 0
        shift = 0
        while shift < 32:
            val = ord(self.pull(1))
            value |= (val & 0x7F) << shift
            if val & 128 == 0:
                break
            shift += 7
        if shift >= 32:
            raise ValueError
        return value

"""
primitive type readers
"""

from __future__ import print_function

from xnb_parse.type_reader import TypeReaderPlugin, BaseTypeReader, ValueTypeReader, ReaderError


class ByteReader(ValueTypeReader, TypeReaderPlugin):
    target_type = 'System.Byte'
    reader_name = 'Microsoft.Xna.Framework.Content.ByteReader'

    def read(self):
        return self.stream.read_byte()


class SByteReader(ValueTypeReader, TypeReaderPlugin):
    target_type = 'System.SByte'
    reader_name = 'Microsoft.Xna.Framework.Content.SByteReader'

    def read(self):
        return self.stream.read_sbyte()


class Int16Reader(ValueTypeReader, TypeReaderPlugin):
    target_type = 'System.Int16'
    reader_name = 'Microsoft.Xna.Framework.Content.Int16Reader'

    def read(self):
        return self.stream.read_int16()


class UInt16Reader(ValueTypeReader, TypeReaderPlugin):
    target_type = 'System.UInt16'
    reader_name = 'Microsoft.Xna.Framework.Content.UInt16Reader'

    def read(self):
        return self.stream.read_uint16()


class Int32Reader(ValueTypeReader, TypeReaderPlugin):
    target_type = 'System.Int32'
    reader_name = 'Microsoft.Xna.Framework.Content.Int32Reader'

    def read(self):
        return self.stream.read_int32()


class UInt32Reader(ValueTypeReader, TypeReaderPlugin):
    target_type = 'System.UInt32'
    reader_name = 'Microsoft.Xna.Framework.Content.UInt32Reader'

    def read(self):
        return self.stream.read_uint32()


class Int64Reader(ValueTypeReader, TypeReaderPlugin):
    target_type = 'System.Int64'
    reader_name = 'Microsoft.Xna.Framework.Content.Int64Reader'

    def read(self):
        return self.stream.read_int64()


class UInt64Reader(ValueTypeReader, TypeReaderPlugin):
    target_type = 'System.UInt64'
    reader_name = 'Microsoft.Xna.Framework.Content.UInt64Reader'

    def read(self):
        return self.stream.read_uint64()


class SingleReader(ValueTypeReader, TypeReaderPlugin):
    target_type = 'System.Single'
    reader_name = 'Microsoft.Xna.Framework.Content.SingleReader'

    def read(self):
        return self.stream.read_single()


class DoubleReader(ValueTypeReader, TypeReaderPlugin):
    target_type = 'System.Double'
    reader_name = 'Microsoft.Xna.Framework.Content.DoubleReader'

    def read(self):
        return self.stream.read_double()


class BooleanReader(ValueTypeReader, TypeReaderPlugin):
    target_type = 'System.Boolean'
    reader_name = 'Microsoft.Xna.Framework.Content.BooleanReader'

    def read(self):
        return self.stream.read_boolean()


class CharReader(ValueTypeReader, TypeReaderPlugin):
    target_type = 'System.Char'
    reader_name = 'Microsoft.Xna.Framework.Content.CharReader'

    def read(self):
        return self.stream.read_char()


class StringReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'System.String'
    reader_name = 'Microsoft.Xna.Framework.Content.StringReader'

    def read(self):
        return self.stream.read_string()


class ObjectReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'System.Object'
    reader_name = 'Microsoft.Xna.Framework.Content.ObjectReader'

    def read(self):
        raise ReaderError('ObjectReader invoked for {}'.format(self.target_type))

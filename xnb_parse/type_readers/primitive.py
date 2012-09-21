"""
primitive types
"""

from xnb_parse.type_reader_manager import BaseTypeReader, ReaderError


class ValueTypeReader(BaseTypeReader):
    is_value_type = True


class ByteReader(ValueTypeReader):
    target_type = 'System.Byte'
    reader_name = 'Microsoft.Xna.Framework.Content.ByteReader'


class SByteReader(ValueTypeReader):
    target_type = 'System.SByte'
    reader_name = 'Microsoft.Xna.Framework.Content.SByteReader'


class Int16Reader(ValueTypeReader):
    target_type = 'System.Int16'
    reader_name = 'Microsoft.Xna.Framework.Content.Int16Reader'


class UInt16Reader(ValueTypeReader):
    target_type = 'System.UInt16'
    reader_name = 'Microsoft.Xna.Framework.Content.UInt16Reader'


class Int32Reader(ValueTypeReader):
    target_type = 'System.Int32'
    reader_name = 'Microsoft.Xna.Framework.Content.Int32Reader'


class UInt32Reader(ValueTypeReader):
    target_type = 'System.UInt32'
    reader_name = 'Microsoft.Xna.Framework.Content.UInt32Reader'


class Int64Reader(ValueTypeReader):
    target_type = 'System.Int64'
    reader_name = 'Microsoft.Xna.Framework.Content.Int64Reader'


class UInt64Reader(ValueTypeReader):
    target_type = 'System.UInt64'
    reader_name = 'Microsoft.Xna.Framework.Content.UInt64Reader'


class SingleReader(ValueTypeReader):
    target_type = 'System.Single'
    reader_name = 'Microsoft.Xna.Framework.Content.SingleReader'


class DoubleReader(ValueTypeReader):
    target_type = 'System.Double'
    reader_name = 'Microsoft.Xna.Framework.Content.DoubleReader'


class BooleanReader(ValueTypeReader):
    target_type = 'System.Boolean'
    reader_name = 'Microsoft.Xna.Framework.Content.BooleanReader'


class CharReader(ValueTypeReader):
    target_type = 'System.Char'
    reader_name = 'Microsoft.Xna.Framework.Content.CharReader'


class StringReader(BaseTypeReader):
    target_type = 'System.String'
    reader_name = 'Microsoft.Xna.Framework.Content.StringReader'


class ObjectReader(BaseTypeReader):
    target_type = 'System.Object'
    reader_name = 'Microsoft.Xna.Framework.Content.ObjectReader'

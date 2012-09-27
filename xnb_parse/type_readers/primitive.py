"""
primitive type readers
"""

from xnb_parse.type_reader_manager import TypeReaderPlugin
from xnb_parse.type_reader import BaseTypeReader, ValueTypeReader


class ByteReader(ValueTypeReader, TypeReaderPlugin):
    target_type = 'System.Byte'
    reader_name = 'Microsoft.Xna.Framework.Content.ByteReader'


class SByteReader(ValueTypeReader, TypeReaderPlugin):
    target_type = 'System.SByte'
    reader_name = 'Microsoft.Xna.Framework.Content.SByteReader'


class Int16Reader(ValueTypeReader, TypeReaderPlugin):
    target_type = 'System.Int16'
    reader_name = 'Microsoft.Xna.Framework.Content.Int16Reader'


class UInt16Reader(ValueTypeReader, TypeReaderPlugin):
    target_type = 'System.UInt16'
    reader_name = 'Microsoft.Xna.Framework.Content.UInt16Reader'


class Int32Reader(ValueTypeReader, TypeReaderPlugin):
    target_type = 'System.Int32'
    reader_name = 'Microsoft.Xna.Framework.Content.Int32Reader'


class UInt32Reader(ValueTypeReader, TypeReaderPlugin):
    target_type = 'System.UInt32'
    reader_name = 'Microsoft.Xna.Framework.Content.UInt32Reader'


class Int64Reader(ValueTypeReader, TypeReaderPlugin):
    target_type = 'System.Int64'
    reader_name = 'Microsoft.Xna.Framework.Content.Int64Reader'


class UInt64Reader(ValueTypeReader, TypeReaderPlugin):
    target_type = 'System.UInt64'
    reader_name = 'Microsoft.Xna.Framework.Content.UInt64Reader'


class SingleReader(ValueTypeReader, TypeReaderPlugin):
    target_type = 'System.Single'
    reader_name = 'Microsoft.Xna.Framework.Content.SingleReader'


class DoubleReader(ValueTypeReader, TypeReaderPlugin):
    target_type = 'System.Double'
    reader_name = 'Microsoft.Xna.Framework.Content.DoubleReader'


class BooleanReader(ValueTypeReader, TypeReaderPlugin):
    target_type = 'System.Boolean'
    reader_name = 'Microsoft.Xna.Framework.Content.BooleanReader'


class CharReader(ValueTypeReader, TypeReaderPlugin):
    target_type = 'System.Char'
    reader_name = 'Microsoft.Xna.Framework.Content.CharReader'


class StringReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'System.String'
    reader_name = 'Microsoft.Xna.Framework.Content.StringReader'


class ObjectReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'System.Object'
    reader_name = 'Microsoft.Xna.Framework.Content.ObjectReader'

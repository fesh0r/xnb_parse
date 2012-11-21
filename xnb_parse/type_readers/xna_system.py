"""
system type readers
"""

from xnb_parse.type_reader_manager import TypeReaderPlugin
from xnb_parse.type_reader import ValueTypeReader, GenericTypeReader, GenericValueTypeReader, ReaderError
from xnb_parse.xna_types.xna_system import XNAList, XNADict


class EnumReader(GenericValueTypeReader, TypeReaderPlugin):
    generic_target_type = 'System.Enum`1'
    generic_reader_name = 'Microsoft.Xna.Framework.Content.EnumReader`1'

    def init_reader(self):
        GenericValueTypeReader.init_reader(self)
        if not self.readers[0].is_enum_type:
            ReaderError("Not enum type reader: '{}'".format(self.readers[0]))

    def read(self):
        return self.readers[0].read()


class NullableReader(GenericValueTypeReader, TypeReaderPlugin):
    generic_target_type = 'System.Nullable`1'
    generic_reader_name = 'Microsoft.Xna.Framework.Content.NullableReader`1'

    def read(self):
        has_value = self.stream.read_boolean()
        if has_value:
            return self.readers[0].read()
        else:
            return None


class ArrayReader(GenericTypeReader, TypeReaderPlugin):
    generic_target_type = 'System.Array`1'
    generic_reader_name = 'Microsoft.Xna.Framework.Content.ArrayReader`1'

    def read(self):
        elements = self.stream.read_int32()
        if self.readers[0].is_value_type:
            return XNAList([self.readers[0].read() for _ in range(elements)])
        else:
            return XNAList([self.stream.read_object(self.readers[0]) for _ in range(elements)])


class ListReader(GenericTypeReader, TypeReaderPlugin):
    generic_target_type = 'System.Collections.Generic.List`1'
    generic_reader_name = 'Microsoft.Xna.Framework.Content.ListReader`1'

    def read(self):
        elements = self.stream.read_int32()
        if self.readers[0].is_value_type:
            return XNAList([self.readers[0].read() for _ in range(elements)])
        else:
            return XNAList([self.stream.read_object(self.readers[0]) for _ in range(elements)])


class DictionaryReader(GenericTypeReader, TypeReaderPlugin):
    generic_target_type = 'System.Collections.Generic.Dictionary`2'
    generic_reader_name = 'Microsoft.Xna.Framework.Content.DictionaryReader`2'

    def read(self):
        elements = self.stream.read_int32()
        values = XNADict()
        if self.readers[1].is_value_type:
            for _ in range(elements):
                key = self.readers[0].read()
                value = self.readers[1].read()
                values[key] = value
        else:
            for _ in range(elements):
                key = self.readers[0].read()
                value = self.stream.read_object(self.readers[1])
                values[key] = value
        return values


class TimeSpanReader(ValueTypeReader, TypeReaderPlugin):
    target_type = 'System.TimeSpan'
    reader_name = 'Microsoft.Xna.Framework.Content.TimeSpanReader'

    def read(self):
        return self.stream.read_int64()


class DateTimeReader(ValueTypeReader, TypeReaderPlugin):
    target_type = 'System.DateTime'
    reader_name = 'Microsoft.Xna.Framework.Content.DateTimeReader'

    def read(self):
        return self.stream.read_int64()


class DecimalReader(ValueTypeReader, TypeReaderPlugin):
    target_type = 'System.Decimal'
    reader_name = 'Microsoft.Xna.Framework.Content.DecimalReader'

    def read(self):
        return self.stream.unpack('4i')


class ExternalReferenceReader(ValueTypeReader, TypeReaderPlugin):
    target_type = 'ExternalReference'
    reader_name = 'Microsoft.Xna.Framework.Content.ExternalReferenceReader'

    def read(self):
        return self.stream.read_external_reference()


class ReflectiveReader(GenericTypeReader, TypeReaderPlugin):
    generic_target_type = 'Reflective'
    generic_reader_name = 'Microsoft.Xna.Framework.Content.ReflectiveReader`1'

    def read(self):
        return self.readers[0].read()

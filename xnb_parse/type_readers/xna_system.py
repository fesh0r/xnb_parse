"""
system type readers
"""

from xnb_parse.type_reader_manager import TypeReaderPlugin
from xnb_parse.type_reader import BaseTypeReader, ValueTypeReader


class TimeSpan(ValueTypeReader, TypeReaderPlugin):
    target_type = 'System.TimeSpan'
    reader_name = 'Microsoft.Xna.Framework.Content.TimeSpanReader'

    def read(self):
        ticks = self.stream.read('s8')
        return ticks


class DateTimeReader(ValueTypeReader, TypeReaderPlugin):
    target_type = 'System.DateTime'
    reader_name = 'Microsoft.Xna.Framework.Content.DateTimeReader'

    def read(self):
        value = self.stream.read('u8')
        return value


class DecimalReader(ValueTypeReader, TypeReaderPlugin):
    target_type = 'System.Decimal'
    reader_name = 'Microsoft.Xna.Framework.Content.DecimalReader'

    def read(self):
        v_a = self.stream.read('u4')
        v_b = self.stream.read('u4')
        v_c = self.stream.read('u4')
        v_d = self.stream.read('u4')
        return v_a, v_b, v_c, v_d


class ExternalReferenceReader(ValueTypeReader, TypeReaderPlugin):
    target_type = 'ExternalReference'
    reader_name = 'Microsoft.Xna.Framework.Content.ExternalReferenceReader'

    def read(self):
        filename = self.stream.read('str')
        return filename

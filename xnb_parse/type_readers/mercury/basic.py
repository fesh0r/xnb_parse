"""
mercury particle engine basic type readers
"""

from __future__ import print_function

from xnb_parse.type_reader import EnumTypeReader, TypeReaderPlugin, ValueTypeReader
from xnb_parse.xna_types.mercury.basic import BlendMode, VariableFloat, VariableFloat3


class VariableFloatReader(ValueTypeReader, TypeReaderPlugin):
    target_type = 'ProjectMercury.VariableFloat'
    reader_name = 'Microsoft.Xna.Framework.Content.ReflectiveReader`1[ProjectMercury.VariableFloat]'

    def read(self):
        value = self.stream.read_single()
        variation = self.stream.read_single()
        return VariableFloat(value, variation)


class VariableFloat3Reader(ValueTypeReader, TypeReaderPlugin):
    target_type = 'ProjectMercury.VariableFloat3'
    reader_name = 'Microsoft.Xna.Framework.Content.ReflectiveReader`1[ProjectMercury.VariableFloat3]'

    def read(self):
        value = self.stream.read_vector3()
        variation = self.stream.read_vector3()
        return VariableFloat3(value, variation)


class BlendModeReader(EnumTypeReader, TypeReaderPlugin):
    target_type = 'ProjectMercury.BlendMode'
    reader_name = 'ProjectMercury.BlendMode'
    enum_type = BlendMode

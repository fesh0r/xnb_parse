"""
FEZ basic type readers
"""

from xnb_parse.type_reader import ValueTypeReader, GenericTypeReader
from xnb_parse.type_reader_manager import TypeReaderPlugin


class FaceOrientationReader(ValueTypeReader, TypeReaderPlugin):
    target_type = u'FezEngine.FaceOrientation'
    reader_name = u'FezEngine.FaceOrientationReader'

    def read(self):
        return self.stream.read_int32()


class LevelNodeTypeReader(ValueTypeReader, TypeReaderPlugin):
    target_type = u'FezEngine.LevelNodeType'
    reader_name = u'FezEngine.LevelNodeTypeReader'

    def read(self):
        return self.stream.read_int32()


class NpcActionReader(ValueTypeReader, TypeReaderPlugin):
    target_type = u'FezEngine.Structure.NpcAction'
    reader_name = u'FezEngine.Readers.NpcActionReader'

    def read(self):
        return self.stream.read_int32()


class ActorTypeReader(ValueTypeReader, TypeReaderPlugin):
    target_type = u'FezEngine.Structure.ActorType'
    reader_name = u'FezEngine.Readers.ActorTypeReader'

    def read(self):
        return self.stream.read_int32()


class CollisionTypeReader(ValueTypeReader, TypeReaderPlugin):
    target_type = u'FezEngine.CollisionType'
    reader_name = u'FezEngine.Readers.CollisionTypeReader'

    def read(self):
        return self.stream.read_int32()


class SurfaceTypeReader(ValueTypeReader, TypeReaderPlugin):
    target_type = u'FezEngine.Structure.SurfaceType'
    reader_name = u'FezEngine.Readers.SurfaceTypeReader'

    def read(self):
        return self.stream.read_int32()


class LiquidTypeReader(ValueTypeReader, TypeReaderPlugin):
    target_type = u'FezEngine.Structure.LiquidType'
    reader_name = u'FezEngine.Readers.LiquidTypeReader'

    def read(self):
        return self.stream.read_int32()


class ViewpointReader(ValueTypeReader, TypeReaderPlugin):
    target_type = u'FezEngine.Viewpoint'
    reader_name = u'FezEngine.Readers.ViewpointReader'

    def read(self):
        return self.stream.read_int32()


class PathEndBehaviorReader(ValueTypeReader, TypeReaderPlugin):
    target_type = u'FezEngine.Structure.PathEndBehavior'
    reader_name = u'FezEngine.Readers.PathEndBehaviorReader'

    def read(self):
        return self.stream.read_int32()


class ComparisonOperatorReader(ValueTypeReader, TypeReaderPlugin):
    target_type = u'FezEngine.Structure.Scripting.ComparisonOperator'
    reader_name = u'FezEngine.Readers.ComparisonOperatorReader'

    def read(self):
        return self.stream.read_int32()


class CodeInputReader(ValueTypeReader, TypeReaderPlugin):
    target_type = u'FezEngine.Structure.Input.CodeInput'
    reader_name = u'FezEngine.Readers.CodeInputReader'

    def read(self):
        return self.stream.read_int32()


class VibrationMotorReader(ValueTypeReader, TypeReaderPlugin):
    target_type = u'FezEngine.Structure.Input.VibrationMotor'
    reader_name = u'FezEngine.Readers.VibrationMotorReader'

    def read(self):
        return self.stream.read_int32()


class SetReader(GenericTypeReader, TypeReaderPlugin):
    generic_target_type = u'Common.Set`1'
    generic_reader_name = u'FezEngine.SetReader`1'

    def read(self):
        return None


class IEqualityComparerFaceOrientationReader(GenericTypeReader, TypeReaderPlugin):
    generic_target_type = u'System.Collections.Generic.IEqualityComparer`1'
    generic_reader_name = u'FezEngine.IEqualityComparerReader`1'

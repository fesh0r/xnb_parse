"""
FEZ basic type readers
"""

from xnb_parse.type_reader import GenericTypeReader, EnumTypeReader
from xnb_parse.type_reader_manager import TypeReaderPlugin


class FaceOrientationReader(EnumTypeReader, TypeReaderPlugin):
    target_type = u'FezEngine.FaceOrientation'
    reader_name = u'FezEngine.FaceOrientationReader'


class LevelNodeTypeReader(EnumTypeReader, TypeReaderPlugin):
    target_type = u'FezEngine.LevelNodeType'
    reader_name = u'FezEngine.LevelNodeTypeReader'


class CollisionTypeReader(EnumTypeReader, TypeReaderPlugin):
    target_type = u'FezEngine.CollisionType'
    reader_name = u'FezEngine.Readers.CollisionTypeReader'


class ViewpointReader(EnumTypeReader, TypeReaderPlugin):
    target_type = u'FezEngine.Viewpoint'
    reader_name = u'FezEngine.Readers.ViewpointReader'


class NpcActionReader(EnumTypeReader, TypeReaderPlugin):
    target_type = u'FezEngine.Structure.NpcAction'
    reader_name = u'FezEngine.Readers.NpcActionReader'


class ActorTypeReader(EnumTypeReader, TypeReaderPlugin):
    target_type = u'FezEngine.Structure.ActorType'
    reader_name = u'FezEngine.Readers.ActorTypeReader'


class SurfaceTypeReader(EnumTypeReader, TypeReaderPlugin):
    target_type = u'FezEngine.Structure.SurfaceType'
    reader_name = u'FezEngine.Readers.SurfaceTypeReader'


class LiquidTypeReader(EnumTypeReader, TypeReaderPlugin):
    target_type = u'FezEngine.Structure.LiquidType'
    reader_name = u'FezEngine.Readers.LiquidTypeReader'


class PathEndBehaviorReader(EnumTypeReader, TypeReaderPlugin):
    target_type = u'FezEngine.Structure.PathEndBehavior'
    reader_name = u'FezEngine.Readers.PathEndBehaviorReader'


class ComparisonOperatorReader(EnumTypeReader, TypeReaderPlugin):
    target_type = u'FezEngine.Structure.Scripting.ComparisonOperator'
    reader_name = u'FezEngine.Readers.ComparisonOperatorReader'


class CodeInputReader(EnumTypeReader, TypeReaderPlugin):
    target_type = u'FezEngine.Structure.Input.CodeInput'
    reader_name = u'FezEngine.Readers.CodeInputReader'


class VibrationMotorReader(EnumTypeReader, TypeReaderPlugin):
    target_type = u'FezEngine.Structure.Input.VibrationMotor'
    reader_name = u'FezEngine.Readers.VibrationMotorReader'


class SetReader(GenericTypeReader, TypeReaderPlugin):
    generic_target_type = u'Common.Set`1'
    generic_reader_name = u'FezEngine.SetReader`1'

    def read(self):
        return None


class IEqualityComparerReader(GenericTypeReader, TypeReaderPlugin):
    generic_target_type = u'System.Collections.Generic.IEqualityComparer`1'
    generic_reader_name = u'FezEngine.IEqualityComparerReader`1'

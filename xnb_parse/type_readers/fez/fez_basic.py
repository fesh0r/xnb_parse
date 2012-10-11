"""
FEZ basic type readers
"""

from xnb_parse.type_reader import GenericTypeReader, EnumTypeReader
from xnb_parse.type_reader_manager import TypeReaderPlugin
from xnb_parse.xna_types.xna_system import XNASet
from xnb_parse.xna_types.fez.fez_basic import (FaceOrientation, LevelNodeType, CollisionType, Viewpoint, NpcAction,
                                               ActorType, SurfaceType, LiquidType, PathEndBehavior, ComparisonOperator,
                                               CodeInput, VibrationMotor)


class FaceOrientationReader(EnumTypeReader, TypeReaderPlugin):
    target_type = u'FezEngine.FaceOrientation'
    reader_name = u'FezEngine.FaceOrientationReader'
    enum_type = FaceOrientation


class LevelNodeTypeReader(EnumTypeReader, TypeReaderPlugin):
    target_type = u'FezEngine.LevelNodeType'
    reader_name = u'FezEngine.LevelNodeTypeReader'
    enum_type = LevelNodeType


class CollisionTypeReader(EnumTypeReader, TypeReaderPlugin):
    target_type = u'FezEngine.CollisionType'
    reader_name = u'FezEngine.Readers.CollisionTypeReader'
    enum_type = CollisionType


class ViewpointReader(EnumTypeReader, TypeReaderPlugin):
    target_type = u'FezEngine.Viewpoint'
    reader_name = u'FezEngine.Readers.ViewpointReader'
    enum_type = Viewpoint


class NpcActionReader(EnumTypeReader, TypeReaderPlugin):
    target_type = u'FezEngine.Structure.NpcAction'
    reader_name = u'FezEngine.Readers.NpcActionReader'
    enum_type = NpcAction


class ActorTypeReader(EnumTypeReader, TypeReaderPlugin):
    target_type = u'FezEngine.Structure.ActorType'
    reader_name = u'FezEngine.Readers.ActorTypeReader'
    enum_type = ActorType


class SurfaceTypeReader(EnumTypeReader, TypeReaderPlugin):
    target_type = u'FezEngine.Structure.SurfaceType'
    reader_name = u'FezEngine.Readers.SurfaceTypeReader'
    enum_type = SurfaceType


class LiquidTypeReader(EnumTypeReader, TypeReaderPlugin):
    target_type = u'FezEngine.Structure.LiquidType'
    reader_name = u'FezEngine.Readers.LiquidTypeReader'
    enum_type = LiquidType


class PathEndBehaviorReader(EnumTypeReader, TypeReaderPlugin):
    target_type = u'FezEngine.Structure.PathEndBehavior'
    reader_name = u'FezEngine.Readers.PathEndBehaviorReader'
    enum_type = PathEndBehavior


class ComparisonOperatorReader(EnumTypeReader, TypeReaderPlugin):
    target_type = u'FezEngine.Structure.Scripting.ComparisonOperator'
    reader_name = u'FezEngine.Readers.ComparisonOperatorReader'
    enum_type = ComparisonOperator


class CodeInputReader(EnumTypeReader, TypeReaderPlugin):
    target_type = u'FezEngine.Structure.Input.CodeInput'
    reader_name = u'FezEngine.Readers.CodeInputReader'
    enum_type = CodeInput


class VibrationMotorReader(EnumTypeReader, TypeReaderPlugin):
    target_type = u'FezEngine.Structure.Input.VibrationMotor'
    reader_name = u'FezEngine.Readers.VibrationMotorReader'
    enum_type = VibrationMotor


class SetReader(GenericTypeReader, TypeReaderPlugin):
    generic_target_type = u'Common.Set`1'
    generic_reader_name = u'FezEngine.SetReader`1'

    def read(self):
        return XNASet()


class IEqualityComparerReader(GenericTypeReader, TypeReaderPlugin):
    generic_target_type = u'System.Collections.Generic.IEqualityComparer`1'
    generic_reader_name = u'FezEngine.IEqualityComparerReader`1'

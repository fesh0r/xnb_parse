"""
FEZ basic type readers
"""

from __future__ import print_function

from xnb_parse.type_reader import TypeReaderPlugin, GenericTypeReader, EnumTypeReader
from xnb_parse.xna_types.xna_system import XNASet
from xnb_parse.xna_types.fez.fez_basic import (FaceOrientation, LevelNodeType, CollisionType, Viewpoint, NpcAction,
                                               ActorType, SurfaceType, LiquidType, PathEndBehavior, ComparisonOperator,
                                               CodeInput, VibrationMotor)


class FaceOrientationReader(EnumTypeReader, TypeReaderPlugin):
    target_type = 'FezEngine.FaceOrientation'
    reader_name = 'FezEngine.FaceOrientationReader'
    enum_type = FaceOrientation


class LevelNodeTypeReader(EnumTypeReader, TypeReaderPlugin):
    target_type = 'FezEngine.LevelNodeType'
    reader_name = 'FezEngine.LevelNodeTypeReader'
    enum_type = LevelNodeType


class CollisionTypeReader(EnumTypeReader, TypeReaderPlugin):
    target_type = 'FezEngine.CollisionType'
    reader_name = 'FezEngine.Readers.CollisionTypeReader'
    enum_type = CollisionType


class ViewpointReader(EnumTypeReader, TypeReaderPlugin):
    target_type = 'FezEngine.Viewpoint'
    reader_name = 'FezEngine.Readers.ViewpointReader'
    enum_type = Viewpoint


class NpcActionReader(EnumTypeReader, TypeReaderPlugin):
    target_type = 'FezEngine.Structure.NpcAction'
    reader_name = 'FezEngine.Readers.NpcActionReader'
    enum_type = NpcAction


class ActorTypeReader(EnumTypeReader, TypeReaderPlugin):
    target_type = 'FezEngine.Structure.ActorType'
    reader_name = 'FezEngine.Readers.ActorTypeReader'
    enum_type = ActorType


class SurfaceTypeReader(EnumTypeReader, TypeReaderPlugin):
    target_type = 'FezEngine.Structure.SurfaceType'
    reader_name = 'FezEngine.Readers.SurfaceTypeReader'
    enum_type = SurfaceType


class LiquidTypeReader(EnumTypeReader, TypeReaderPlugin):
    target_type = 'FezEngine.Structure.LiquidType'
    reader_name = 'FezEngine.Readers.LiquidTypeReader'
    enum_type = LiquidType


class PathEndBehaviorReader(EnumTypeReader, TypeReaderPlugin):
    target_type = 'FezEngine.Structure.PathEndBehavior'
    reader_name = 'FezEngine.Readers.PathEndBehaviorReader'
    enum_type = PathEndBehavior


class ComparisonOperatorReader(EnumTypeReader, TypeReaderPlugin):
    target_type = 'FezEngine.Structure.Scripting.ComparisonOperator'
    reader_name = 'FezEngine.Readers.ComparisonOperatorReader'
    enum_type = ComparisonOperator


class CodeInputReader(EnumTypeReader, TypeReaderPlugin):
    target_type = 'FezEngine.Structure.Input.CodeInput'
    reader_name = 'FezEngine.Readers.CodeInputReader'
    enum_type = CodeInput


class VibrationMotorReader(EnumTypeReader, TypeReaderPlugin):
    target_type = 'FezEngine.Structure.Input.VibrationMotor'
    reader_name = 'FezEngine.Readers.VibrationMotorReader'
    enum_type = VibrationMotor


class SetReader(GenericTypeReader, TypeReaderPlugin):
    generic_target_type = 'Common.Set`1'
    generic_reader_name = 'FezEngine.SetReader`1'

    def read(self):
        return XNASet()


class IEqualityComparerReader(GenericTypeReader, TypeReaderPlugin):
    generic_target_type = 'System.Collections.Generic.IEqualityComparer`1'
    generic_reader_name = 'FezEngine.IEqualityComparerReader`1'

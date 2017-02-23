"""
mercury particle engine modifier type readers
"""

from __future__ import print_function

from xnb_parse.type_reader import BaseTypeReader, ReaderError, TypeReaderPlugin
from xnb_parse.xna_types.mercury.modifiers import (ColourModifier, LinearGravityModifier, ModifierCollection,
                                                   OpacityModifier, RotationRateModifier, ScaleModifier,
                                                   ColourInterpolatorModifier, ColourMergeModifier, DampingModifier,
                                                   HueShiftModifier, OpacityInterpolatorModifier, OpacityOscillator,
                                                   RotationModifier, TrajectoryRotationModifier, RadialForceModifier,
                                                   RadialGravityModifier, RectangleConstraintDeflector,
                                                   RectangleForceModifier, ScaleInterpolatorModifier,
                                                   ScaleMergeModifier, ScaleOscillator, SineForceModifier,
                                                   VelocityClampModifier)
from xnb_parse.xna_types.xna_system import XNAList


class ModifierCollectionReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'ProjectMercury.Modifiers.ModifierCollection'
    reader_name = 'Microsoft.Xna.Framework.Content.ReflectiveReader`1[ProjectMercury.Modifiers.ModifierCollection]'

    def read(self):
        elements = self.stream.read_int32()
        return ModifierCollection(XNAList([self.stream.read_object(ModifierReader) for _ in range(elements)]))


class ModifierReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'ProjectMercury.Modifiers.Modifier'
    reader_name = 'Microsoft.Xna.Framework.Content.ReflectiveReader`1[ProjectMercury.Modifiers.Modifier]'

    def read(self):
        raise ReaderError('ModifierReader invoked for {}'.format(self.target_type))


class OpacityModifierReader(ModifierReader, TypeReaderPlugin):
    target_type = 'ProjectMercury.Modifiers.OpacityModifier'
    reader_name = 'Microsoft.Xna.Framework.Content.ReflectiveReader`1[ProjectMercury.Modifiers.OpacityModifier]'

    def read(self):
        initial = self.stream.read_single()
        ultimate = self.stream.read_single()
        return OpacityModifier(initial, ultimate)


class ScaleModifierReader(ModifierReader, TypeReaderPlugin):
    target_type = 'ProjectMercury.Modifiers.ScaleModifier'
    reader_name = 'Microsoft.Xna.Framework.Content.ReflectiveReader`1[ProjectMercury.Modifiers.ScaleModifier]'

    def read(self):
        initial_scale = self.stream.read_single()
        ultimate_scale = self.stream.read_single()
        return ScaleModifier(initial_scale, ultimate_scale)


class RotationRateModifierReader(ModifierReader, TypeReaderPlugin):
    target_type = 'ProjectMercury.Modifiers.RotationRateModifier'
    reader_name = 'Microsoft.Xna.Framework.Content.ReflectiveReader`1[ProjectMercury.Modifiers.RotationRateModifier]'

    def read(self):
        initial_rate = self.stream.read_single()
        final_rate = self.stream.read_single()
        return RotationRateModifier(initial_rate, final_rate)


class ColourModifierReader(ModifierReader, TypeReaderPlugin):
    target_type = 'ProjectMercury.Modifiers.ColourModifier'
    reader_name = 'Microsoft.Xna.Framework.Content.ReflectiveReader`1[ProjectMercury.Modifiers.ColourModifier]'

    def read(self):
        initial_colour = self.stream.read_vector3()
        ultimate_colour = self.stream.read_vector3()
        return ColourModifier(initial_colour, ultimate_colour)


class LinearGravityModifierReader(ModifierReader, TypeReaderPlugin):
    target_type = 'ProjectMercury.Modifiers.LinearGravityModifier'
    reader_name = 'Microsoft.Xna.Framework.Content.ReflectiveReader`1[ProjectMercury.Modifiers.LinearGravityModifier]'

    def read(self):
        gravity = self.stream.read_vector2()
        return LinearGravityModifier(gravity)


class ColourInterpolatorModifierReader(ModifierReader, TypeReaderPlugin):
    target_type = 'ProjectMercury.Modifiers.ColourInterpolatorModifier'
    reader_name = \
        'Microsoft.Xna.Framework.Content.ReflectiveReader`1[ProjectMercury.Modifiers.ColourInterpolatorModifier]'

    def read(self):
        initial_colour = self.stream.read_vector3()
        middle_colour = self.stream.read_vector3()
        middle_position = self.stream.read_single()
        final_colour = self.stream.read_vector3()
        return ColourInterpolatorModifier(initial_colour, middle_colour, middle_position, final_colour)


class ColourMergeModifierReader(ModifierReader, TypeReaderPlugin):
    target_type = 'ProjectMercury.Modifiers.ColourMergeModifier'
    reader_name = 'Microsoft.Xna.Framework.Content.ReflectiveReader`1[ProjectMercury.Modifiers.ColourMergeModifier]'

    def read(self):
        merge_colour = self.stream.read_vector3()
        return ColourMergeModifier(merge_colour)


class DampingModifierReader(ModifierReader, TypeReaderPlugin):
    target_type = 'ProjectMercury.Modifiers.DampingModifier'
    reader_name = 'Microsoft.Xna.Framework.Content.ReflectiveReader`1[ProjectMercury.Modifiers.DampingModifier]'

    def read(self):
        damping_coefficient = self.stream.read_single()
        return DampingModifier(damping_coefficient)


class HueShiftModifierReader(ModifierReader, TypeReaderPlugin):
    target_type = 'ProjectMercury.Modifiers.HueShiftModifier'
    reader_name = 'Microsoft.Xna.Framework.Content.ReflectiveReader`1[ProjectMercury.Modifiers.HueShiftModifier]'

    def read(self):
        hue_shift = self.stream.single()
        return HueShiftModifier(hue_shift)


class OpacityInterpolatorModifierReader(ModifierReader, TypeReaderPlugin):
    target_type = 'ProjectMercury.Modifiers.OpacityInterpolatorModifier'
    reader_name = \
        'Microsoft.Xna.Framework.Content.ReflectiveReader`1[ProjectMercury.Modifiers.OpacityInterpolatorModifier]'

    def read(self):
        initial_opacity = self.stream.read_single()
        middle_opacity = self.stream.read_single()
        middle_position = self.stream.read_single()
        final_opacity = self.stream.read_single()
        return OpacityInterpolatorModifier(initial_opacity, middle_opacity, middle_position, final_opacity)


class OpacityOscillatorReader(ModifierReader, TypeReaderPlugin):
    target_type = 'ProjectMercury.Modifiers.OpacityOscillator'
    reader_name = 'Microsoft.Xna.Framework.Content.ReflectiveReader`1[ProjectMercury.Modifiers.OpacityOscillator]'

    def read(self):
        frequency = self.stream.read_single()
        minimum_opacity = self.stream.read_single()
        maximum_opacity = self.stream.read_single()
        return OpacityOscillator(frequency, minimum_opacity, maximum_opacity)


class RotationModifierReader(ModifierReader, TypeReaderPlugin):
    target_type = 'ProjectMercury.Modifiers.RotationModifier'
    reader_name = 'Microsoft.Xna.Framework.Content.ReflectiveReader`1[ProjectMercury.Modifiers.RotationModifier]'

    def read(self):
        rotation_rate = self.stream.read_single()
        return RotationModifier(rotation_rate)


class TrajectoryRotationModifierReader(ModifierReader, TypeReaderPlugin):
    target_type = 'ProjectMercury.Modifiers.TrajectoryRotationModifier'
    reader_name = \
        'Microsoft.Xna.Framework.Content.ReflectiveReader`1[ProjectMercury.Modifiers.TrajectoryRotationModifier]'

    def read(self):
        rotation_offset = self.stream.read_single()
        return TrajectoryRotationModifier(rotation_offset)


class RadialForceModifierReader(ModifierReader, TypeReaderPlugin):
    target_type = 'ProjectMercury.Modifiers.RadialForceModifier'
    reader_name = 'Microsoft.Xna.Framework.Content.ReflectiveReader`1[ProjectMercury.Modifiers.RadialForceModifier]'

    def read(self):
        radius = self.stream.read_single()
        position = self.stream.read_vector2()
        force = self.stream.read_vector2()
        strength = self.stream.read_single()
        return RadialForceModifier(radius, position, force, strength)


class RadialGravityModifierReader(ModifierReader, TypeReaderPlugin):
    target_type = 'ProjectMercury.Modifiers.RadialGravityModifier'
    reader_name = 'Microsoft.Xna.Framework.Content.ReflectiveReader`1[ProjectMercury.Modifiers.RadialGravityModifier]'

    def read(self):
        radius = self.stream.read_single()
        position = self.stream.read_vector2()
        return RadialGravityModifier(radius, position)


class RectangleConstraintDeflectorReader(ModifierReader, TypeReaderPlugin):
    target_type = 'ProjectMercury.Modifiers.RectangleConstraintDeflector'
    reader_name = \
        'Microsoft.Xna.Framework.Content.ReflectiveReader`1[ProjectMercury.Modifiers.RectangleConstraintDeflector]'

    def read(self):
        width = self.stream.read_single()
        height = self.stream.read_single()
        position = self.stream.read_vector2()
        return RectangleConstraintDeflector(width, height, position)


class RectangleForceModifierReader(ModifierReader, TypeReaderPlugin):
    target_type = 'ProjectMercury.Modifiers.RectangleForceModifier'
    reader_name = 'Microsoft.Xna.Framework.Content.ReflectiveReader`1[ProjectMercury.Modifiers.RectangleForceModifier]'

    def read(self):
        width = self.stream.read_single()
        height = self.stream.read_single()
        position = self.stream.read_vector2()
        force = self.stream.read_vector2()
        strength = self.stream.read_single()
        return RectangleForceModifier(width, height, position, force, strength)


class ScaleInterpolatorModifierReader(ModifierReader, TypeReaderPlugin):
    target_type = 'ProjectMercury.Modifiers.ScaleInterpolatorModifier'
    reader_name = \
        'Microsoft.Xna.Framework.Content.ReflectiveReader`1[ProjectMercury.Modifiers.ScaleInterpolatorModifier]'

    def read(self):
        initial_scale = self.stream.read_single()
        middle_scale = self.stream.read_single()
        middle_position = self.stream.read_single()
        final_scale = self.stream.read_single()
        return ScaleInterpolatorModifier(initial_scale, middle_scale, middle_position, final_scale)


class ScaleMergeModifierReader(ModifierReader, TypeReaderPlugin):
    target_type = 'ProjectMercury.Modifiers.ScaleMergeModifier'
    reader_name = 'Microsoft.Xna.Framework.Content.ReflectiveReader`1[ProjectMercury.Modifiers.ScaleMergeModifier]'

    def read(self):
        merge_scale = self.stream.read_single()
        return ScaleMergeModifier(merge_scale)


class ScaleOscillatorReader(ModifierReader, TypeReaderPlugin):
    target_type = 'ProjectMercury.Modifiers.ScaleOscillator'
    reader_name = 'Microsoft.Xna.Framework.Content.ReflectiveReader`1[ProjectMercury.Modifiers.ScaleOscillator]'

    def read(self):
        frequency = self.stream.read_single()
        minimum_scale = self.stream.read_single()
        maximum_scale = self.stream.read_single()
        return ScaleOscillator(frequency, minimum_scale, maximum_scale)


class SineForceModifierReader(ModifierReader, TypeReaderPlugin):
    target_type = 'ProjectMercury.Modifiers.SineForceModifier'
    reader_name = 'Microsoft.Xna.Framework.Content.ReflectiveReader`1[ProjectMercury.Modifiers.SineForceModifier]'

    def read(self):
        rotation = self.stream.read_single()
        frequency = self.stream.read_single()
        amplitude = self.stream.read_single()
        return SineForceModifier(rotation, frequency, amplitude)


class VelocityClampModifierReader(ModifierReader, TypeReaderPlugin):
    target_type = 'ProjectMercury.Modifiers.VelocityClampModifier'
    reader_name = 'Microsoft.Xna.Framework.Content.ReflectiveReader`1[ProjectMercury.Modifiers.VelocityClampModifier]'

    def read(self):
        maximum_velocity = self.stream.read_single()
        return VelocityClampModifier(maximum_velocity)

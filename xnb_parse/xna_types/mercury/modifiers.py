"""
mercury particle engine modifier types
"""

from __future__ import print_function


class ModifierCollection(object):
    def __init__(self, modifiers):
        self.modifiers = modifiers

    def __repr__(self):
        return '{}'.format(self.modifiers)


class Modifier(object):
    pass


class OpacityModifier(Modifier):
    def __init__(self, initial, ultimate):
        self.initial = initial
        self.ultimate = ultimate

    def __repr__(self):
        return 'OpacityModifier(initial={}, ultimate={})'.format(self.initial, self.ultimate)


class ScaleModifier(Modifier):
    def __init__(self, initial, ultimate):
        self.initial = initial
        self.ultimate = ultimate

    def __repr__(self):
        return 'ScaleModifier(initial={}, ultimate={})'.format(self.initial, self.ultimate)


class RotationRateModifier(Modifier):
    def __init__(self, initial_rate, final_rate):
        self.initial_rate = initial_rate
        self.final_rate = final_rate

    def __repr__(self):
        return 'RotationRateModifier(initial_rate={}, final_rate={})'.format(self.initial_rate, self.final_rate)


class ColourModifier(Modifier):
    def __init__(self, initial_colour, ultimate_colour):
        self.initial_colour = initial_colour
        self.ultimate_colour = ultimate_colour

    def __repr__(self):
        return 'ColourModifier(initial_colour={}, ultimate_colour={})'.format(self.initial_colour, self.ultimate_colour)


class LinearGravityModifier(Modifier):
    def __init__(self, gravity):
        self.gravity = gravity

    def __repr__(self):
        return 'LinearGravityModifier(gravity={})'.format(self.gravity)


class ColourInterpolatorModifier(Modifier):
    def __init__(self, initial_colour, middle_colour, middle_position, final_colour):
        self.initial_colour = initial_colour
        self.middle_colour = middle_colour
        self.middle_position = middle_position
        self.final_colour = final_colour

    def __repr__(self):
        return 'ColourInterpolatorModifier(' \
               'initial_colour={}, middle_colour={}, middle_position={}, final_colour={})'.format(
                self.initial_colour, self.middle_colour, self.middle_position, self.final_colour)


class ColourMergeModifier(Modifier):
    def __init__(self, merge_colour):
        self.merge_colour = merge_colour

    def __repr__(self):
        return 'ColourMergeModifier(merge_colour={})'.format(self.merge_colour)


class DampingModifier(Modifier):
    def __init__(self, damping_coefficient):
        self.damping_coefficient = damping_coefficient

    def __repr__(self):
        return 'DampingModifier(damping_coefficient={})'.format(self.damping_coefficient)


class HueShiftModifier(Modifier):
    def __init__(self, hue_shift):
        self.hue_shift = hue_shift

    def __repr__(self):
        return 'HueShiftModifier(hue_shift={})'.format(self.hue_shift)


class OpacityInterpolatorModifier(Modifier):
    def __init__(self, initial_opacity, middle_opacity, middle_position, final_opacity):
        self.initial_opacity = initial_opacity
        self.middle_opacity = middle_opacity
        self.middle_position = middle_position
        self.final_opacity = final_opacity

    def __repr__(self):
        return 'OpacityInterpolatorModifier(' \
               'initial_opacity={}, middle_opacity={}, middle_position={}, final_opacity={})'.format(
                self.initial_opacity, self.middle_opacity, self.middle_position, self.final_opacity)


class OpacityOscillator(Modifier):
    def __init__(self, frequency, minimum_opacity, maximum_opacity):
        self.frequency = frequency
        self.minimum_opacity = minimum_opacity
        self.maximum_opacity = maximum_opacity

    def __repr__(self):
        return 'OpacityOscillator(frequency={}, minimum_opacity={}, maximum_opacity={})'.format(
            self.frequency, self.minimum_opacity, self.maximum_opacity)


class RotationModifier(Modifier):
    def __init__(self, rotation_rate):
        self.rotation_rate = rotation_rate

    def __repr__(self):
        return 'RotationModifier(rotation_rate={})'.format(self.rotation_rate)


class TrajectoryRotationModifier(Modifier):
    def __init__(self, rotation_offset):
        self.rotation_offset = rotation_offset

    def __repr__(self):
        return 'TrajectoryRotationModifier(rotation_offset={})'.format(self.rotation_offset)


class RadialForceModifier(Modifier):
    def __init__(self, radius, position, force, strength):
        self.radius = radius
        self.position = position
        self.force = force
        self.strength = strength

    def __repr__(self):
        return 'RadialForceModifier(radius={}, position={}, force={}, strength={})'.format(
            self.radius, self.position, self.force, self.strength)


class RadialGravityModifier(Modifier):
    def __init__(self, radius, position):
        self.radius = radius
        self.position = position

    def __repr__(self):
        return 'RadialGravityModifier(radius={}, position={})'.format(self.radius, self.position)


class RectangleConstraintDeflector(Modifier):
    def __init__(self, width, height, position):
        self.width = width
        self.height = height
        self.position = position

    def __repr__(self):
        return 'RectangleConstraintDeflector(width={}, height={}, position={})'.format(
            self.width, self.height, self.position)


class RectangleForceModifier(Modifier):
    def __init__(self, width, height, position, force, strength):
        self.width = width
        self.height = height
        self.position = position
        self.force = force
        self.strength = strength

    def __repr__(self):
        return 'RectangleForceModifier(width={}, height={}, position={}, force={}, strength={})'.format(
            self.width, self.height, self.position, self.force, self.strength)


class ScaleInterpolatorModifier(Modifier):
    def __init__(self, initial_scale, middle_scale, middle_position, final_scale):
        self.initial_scale = initial_scale
        self.middle_scale = middle_scale
        self.middle_position = middle_position
        self.final_scale = final_scale

    def __repr__(self):
        return 'ScaleInterpolatorModifier(' \
               'initial_scale={}, middle_scale={}, middle_position={}, final_scale={})'.format(
                self.initial_scale, self.middle_scale, self.middle_position, self.final_scale)


class ScaleMergeModifier(Modifier):
    def __init__(self, merge_scale):
        self.merge_scale = merge_scale

    def __repr__(self):
        return 'ScaleMergeModifier(merge_scale={])'.format(self.merge_scale)


class ScaleOscillator(Modifier):
    def __init__(self, frequency, minimum_scale, maximum_scale):
        self.frequency = frequency
        self.minimum_scale = minimum_scale
        self.maximum_scale = maximum_scale

    def __repr__(self):
        return 'ScaleOscillator(frequency={}, minimum_scale={}, maximum_scale={})'.format(
            self.frequency, self.minimum_scale, self.maximum_scale)


class SineForceModifier(Modifier):
    def __init__(self, rotation, frequency, amplitude):
        self.rotation = rotation
        self.frequency = frequency
        self.amplitude = amplitude

    def __repr__(self):
        return 'SineForceModifier(rotation={}, frequency={}, amplitude={})'.format(
            self.rotation, self.frequency, self.amplitude)


class VelocityClampModifier(Modifier):
    def __init__(self, maximum_velocity):
        self.maximum_velocity = maximum_velocity

    def __repr__(self):
        return 'VelocityClampModifier(maximum_velocity={})'.format(self.maximum_velocity)

"""
mercury particle engine emitter types
"""

from __future__ import print_function


class EmitterCollection(object):
    def __init__(self, emitters):
        self.emitters = emitters

    def __repr__(self):
        return '{}'.format(self.emitters)


class Emitter(object):
    def __init__(self, name, budget, term, release_quantity, enabled, release_speed, release_colour, release_opacity,
                 release_scale, release_rotation, release_impulse, particle_texture_asset_name, modifiers, blend_mode,
                 trigger_offset, minimum_trigger_period):
        self.name = name
        self.budget = budget
        self.term = term
        self.release_quantity = release_quantity
        self.enabled = enabled
        self.release_speed = release_speed
        self.release_colour = release_colour
        self.release_opacity = release_opacity
        self.release_scale = release_scale
        self.release_rotation = release_rotation
        self.release_impulse = release_impulse
        self.particle_texture_asset_name = particle_texture_asset_name
        self.modifiers = modifiers
        self.blend_mode = blend_mode
        self.trigger_offset = trigger_offset
        self.minimum_trigger_period = minimum_trigger_period

    def __repr__(self):
        return "Emitter(name={!r}, budget={}, term={}, release_quantity={}, enabled={}, release_speed={}, " \
               "release_colour={}, release_opacity={}, release_scale={}, release_rotation={}, release_impulse={}, " \
               "particle_texture_asset_name={!r}, modifiers={}, blend_mode={!r}, trigger_offset={}, " \
               "minimum_trigger_period={})".format(
                    self.name, self.budget, self.term, self.release_quantity, self.enabled, self.release_speed,
                    self.release_colour, self.release_opacity, self.release_scale, self.release_rotation,
                    self.release_impulse, self.particle_texture_asset_name, self.modifiers, self.blend_mode,
                    self.trigger_offset, self.minimum_trigger_period)


class CircleEmitter(Emitter):
    def __init__(self, name, budget, term, release_quantity, enabled, release_speed, release_colour, release_opacity,
                 release_scale, release_rotation, release_impulse, particle_texture_asset_name, modifiers, blend_mode,
                 trigger_offset, minimum_trigger_period, radius, ring, radiate):
        Emitter.__init__(
            self, name, budget, term, release_quantity, enabled, release_speed, release_colour, release_opacity,
            release_scale, release_rotation, release_impulse, particle_texture_asset_name, modifiers, blend_mode,
            trigger_offset, minimum_trigger_period)
        self.radius = radius
        self.ring = ring
        self.radiate = radiate

    def __repr__(self):
        return "CircleEmitter(name={!r}, budget={}, term={}, release_quantity={}, enabled={}, release_speed={}, " \
               "release_colour={}, release_opacity={}, release_scale={}, release_rotation={}, release_impulse={}, " \
               "particle_texture_asset_name={!r}, modifiers={}, blend_mode={!r}, trigger_offset={}, " \
               "minimum_trigger_period={}, radius={}, ring={}, radiate={})".format(
                    self.name, self.budget, self.term, self.release_quantity, self.enabled, self.release_speed,
                    self.release_colour, self.release_opacity, self.release_scale, self.release_rotation,
                    self.release_impulse, self.particle_texture_asset_name, self.modifiers, self.blend_mode,
                    self.trigger_offset, self.minimum_trigger_period, self.radius, self.ring, self.radiate)

    @staticmethod
    def make(emitter, radius, ring, radiate):
        return CircleEmitter(
            emitter.name, emitter.budget, emitter.term, emitter.release_quantity, emitter.enabled,
            emitter.release_speed, emitter.release_colour, emitter.release_opacity, emitter.release_scale,
            emitter.release_rotation, emitter.release_impulse, emitter.particle_texture_asset_name, emitter.modifiers,
            emitter.blend_mode, emitter.trigger_offset, emitter.minimum_trigger_period, radius, ring, radiate)


class ConeEmitter(Emitter):
    def __init__(self, name, budget, term, release_quantity, enabled, release_speed, release_colour, release_opacity,
                 release_scale, release_rotation, release_impulse, particle_texture_asset_name, modifiers, blend_mode,
                 trigger_offset, minimum_trigger_period, direction, cone_angle):
        Emitter.__init__(
            self, name, budget, term, release_quantity, enabled, release_speed, release_colour, release_opacity,
            release_scale, release_rotation, release_impulse, particle_texture_asset_name, modifiers, blend_mode,
            trigger_offset, minimum_trigger_period)
        self.direction = direction
        self.cone_angle = cone_angle

    def __repr__(self):
        return "ConeEmitter(name={!r}, budget={}, term={}, release_quantity={}, enabled={}, release_speed={}, " \
               "release_colour={}, release_opacity={}, release_scale={}, release_rotation={}, release_impulse={}, " \
               "particle_texture_asset_name={!r}, modifiers={}, blend_mode={!r}, trigger_offset={}, " \
               "minimum_trigger_period={}, direction={}, cone_angle={})".format(
                    self.name, self.budget, self.term, self.release_quantity, self.enabled, self.release_speed,
                    self.release_colour, self.release_opacity, self.release_scale, self.release_rotation,
                    self.release_impulse, self.particle_texture_asset_name, self.modifiers, self.blend_mode,
                    self.trigger_offset, self.minimum_trigger_period, self.direction, self.cone_angle)

    @staticmethod
    def make(emitter, direction, cone_angle):
        return ConeEmitter(
            emitter.name, emitter.budget, emitter.term, emitter.release_quantity, emitter.enabled,
            emitter.release_speed, emitter.release_colour, emitter.release_opacity, emitter.release_scale,
            emitter.release_rotation, emitter.release_impulse, emitter.particle_texture_asset_name, emitter.modifiers,
            emitter.blend_mode, emitter.trigger_offset, emitter.minimum_trigger_period, direction, cone_angle)


class LineEmitter(Emitter):
    def __init__(self, name, budget, term, release_quantity, enabled, release_speed, release_colour, release_opacity,
                 release_scale, release_rotation, release_impulse, particle_texture_asset_name, modifiers, blend_mode,
                 trigger_offset, minimum_trigger_period, length, angle, rectilinear, emit_both_ways):
        Emitter.__init__(
            self, name, budget, term, release_quantity, enabled, release_speed, release_colour, release_opacity,
            release_scale, release_rotation, release_impulse, particle_texture_asset_name, modifiers, blend_mode,
            trigger_offset, minimum_trigger_period)
        self.length = length
        self.angle = angle
        self.rectilinear = rectilinear
        self.emit_both_ways = emit_both_ways

    def __repr__(self):
        return "LineEmitter(name={!r}, budget={}, term={}, release_quantity={}, enabled={}, release_speed={}, " \
               "release_colour={}, release_opacity={}, release_scale={}, release_rotation={}, release_impulse={}, " \
               "particle_texture_asset_name={!r}, modifiers={}, blend_mode={!r}, trigger_offset={}, " \
               "minimum_trigger_period={}, length={}, angle={}, rectilinear={}, emit_both_ways={})".format(
                    self.name, self.budget, self.term, self.release_quantity, self.enabled, self.release_speed,
                    self.release_colour, self.release_opacity, self.release_scale, self.release_rotation,
                    self.release_impulse, self.particle_texture_asset_name, self.modifiers, self.blend_mode,
                    self.trigger_offset, self.minimum_trigger_period, self.length, self.angle, self.rectilinear,
                    self.emit_both_ways)

    @staticmethod
    def make(emitter, length, angle, rectilinear, emit_both_ways):
        return LineEmitter(
            emitter.name, emitter.budget, emitter.term, emitter.release_quantity, emitter.enabled,
            emitter.release_speed, emitter.release_colour, emitter.release_opacity, emitter.release_scale,
            emitter.release_rotation, emitter.release_impulse, emitter.particle_texture_asset_name, emitter.modifiers,
            emitter.blend_mode, emitter.trigger_offset, emitter.minimum_trigger_period, length, angle, rectilinear,
            emit_both_ways)

"""
mercury particle engine emitter type readers
"""

from __future__ import print_function

from xnb_parse.type_reader import BaseTypeReader, TypeReaderPlugin
from xnb_parse.type_readers.mercury.basic import BlendModeReader, VariableFloat3Reader, VariableFloatReader
from xnb_parse.type_readers.mercury.modifiers import ModifierCollectionReader
from xnb_parse.type_readers.xna_primitive import StringReader
from xnb_parse.xna_types.mercury.emitters import Emitter, EmitterCollection, CircleEmitter, ConeEmitter, LineEmitter
from xnb_parse.xna_types.xna_system import XNAList


class EmitterCollectionReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'ProjectMercury.Emitters.EmitterCollection'
    reader_name = 'Microsoft.Xna.Framework.Content.ReflectiveReader`1[ProjectMercury.Emitters.EmitterCollection]'

    def read(self):
        elements = self.stream.read_int32()
        return EmitterCollection(XNAList([self.stream.read_object(EmitterReader) for _ in range(elements)]))


class EmitterReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'ProjectMercury.Emitters.Emitter'
    reader_name = 'Microsoft.Xna.Framework.Content.ReflectiveReader`1[ProjectMercury.Emitters.Emitter]'

    def read(self):
        name = self.stream.read_object(StringReader)
        budget = self.stream.read_int32()
        term = self.stream.read_single()
        release_quantity = self.stream.read_int32()
        enabled = self.stream.read_boolean()
        release_speed = self.stream.read_value_or_object(VariableFloatReader)
        release_colour = self.stream.read_value_or_object(VariableFloat3Reader)
        release_opacity = self.stream.read_value_or_object(VariableFloatReader)
        release_scale = self.stream.read_value_or_object(VariableFloatReader)
        release_rotation = self.stream.read_value_or_object(VariableFloatReader)
        release_impulse = self.stream.read_vector2()
        particle_texture_asset_name = self.stream.read_object(StringReader)
        modifiers = self.stream.read_object(ModifierCollectionReader)
        blend_mode = self.stream.read_value_or_object(BlendModeReader)
        trigger_offset = self.stream.read_vector2()
        minimum_trigger_period = self.stream.read_single()

        return Emitter(name, budget, term, release_quantity, enabled, release_speed, release_colour, release_opacity,
                       release_scale, release_rotation, release_impulse, particle_texture_asset_name, modifiers,
                       blend_mode, trigger_offset, minimum_trigger_period)


class CircleEmitterReader(EmitterReader, TypeReaderPlugin):
    target_type = 'ProjectMercury.Emitters.CircleEmitter'
    reader_name = 'Microsoft.Xna.Framework.Content.ReflectiveReader`1[ProjectMercury.Emitters.CircleEmitter]'

    def read(self):
        emitter = EmitterReader.read(self)
        radius = self.stream.read_single()
        ring = self.stream.read_boolean()
        radiate = self.stream.read_boolean()
        return CircleEmitter.make(emitter, radius, ring, radiate)


class ConeEmitterReader(EmitterReader, TypeReaderPlugin):
    target_type = 'ProjectMercury.Emitters.ConeEmitter'
    reader_name = 'Microsoft.Xna.Framework.Content.ReflectiveReader`1[ProjectMercury.Emitters.ConeEmitter]'

    def read(self):
        emitter = EmitterReader.read(self)
        direction = self.stream.read_single()
        cone_angle = self.stream.read_single()
        return ConeEmitter.make(emitter, direction, cone_angle)


class LineEmitterReader(EmitterReader, TypeReaderPlugin):
    target_type = 'ProjectMercury.Emitters.LineEmitter'
    reader_name = 'Microsoft.Xna.Framework.Content.ReflectiveReader`1[ProjectMercury.Emitters.LineEmitter]'

    def read(self):
        emitter = EmitterReader.read(self)
        length = self.stream.read_single()
        angle = self.stream.read_single()
        rectilinear = self.stream.read_boolean()
        emit_both_ways = self.stream.read_boolean()
        return LineEmitter.make(emitter, length, angle, rectilinear, emit_both_ways)

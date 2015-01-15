"""
FEZ level type readers
"""

from __future__ import print_function

from xnb_parse.type_reader import TypeReaderPlugin, BaseTypeReader, ValueTypeReader
from xnb_parse.type_readers.xna_graphics import Texture2DReader
from xnb_parse.type_readers.xna_math import Vector4Reader
from xnb_parse.type_readers.xna_primitive import Int32Reader, StringReader, BooleanReader
from xnb_parse.type_readers.xna_system import ListReader, DictionaryReader, ArrayReader, TimeSpanReader
from xnb_parse.type_readers.fez.fez_basic import (LevelNodeTypeReader, FaceOrientationReader, CollisionTypeReader,
                                                  LiquidTypeReader, CodeInputReader, ViewpointReader,
                                                  ActorTypeReader, SurfaceTypeReader, PathEndBehaviorReader,
                                                  NpcActionReader, ComparisonOperatorReader, VibrationMotorReader)
from xnb_parse.type_readers.fez.fez_graphics import (ShaderInstancedIndexedPrimitivesReader,
                                                     VertexPositionNormalTextureInstanceReader)
from xnb_parse.xna_types.xna_math import Vector3, Quaternion
from xnb_parse.xna_types.fez.fez_level import (MapTree, MapNode, MapNodeConnection, WinConditions, Sky, SkyLayer, Trile,
                                               TrileSet, Level, TrileFace, TrileEmplacement, Volume,
                                               VolumeActorSettings, DotDialogueLine, Script, ScriptTrigger, Entity,
                                               ScriptAction, ScriptCondition, TrileInstance, InstanceActorSettings,
                                               ArtObjectInstance, ArtObjectActorSettings, PathSegment, CameraNodeData,
                                               SpeechLine, NpcActionContent, NpcInstance, BackgroundPlane, TrileGroup,
                                               MovementPath, AmbienceTrack)


class MapTreeReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'FezEngine.Structure.MapTree'
    reader_name = 'FezEngine.Readers.MapTreeReader'

    def read(self):
        root = self.stream.read_object(MapNodeReader)
        return MapTree(root)


class MapNodeReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'FezEngine.Structure.MapNode'
    reader_name = 'FezEngine.Readers.MapNodeReader'

    def read(self):
        level_name = self.stream.read_string()
        connections = self.stream.read_object(ListReader, [MapNodeConnectionReader])
        node_type = self.stream.read_object(LevelNodeTypeReader)
        conditions = self.stream.read_object(WinConditionsReader)
        has_lesser_gate = self.stream.read_boolean()
        has_warp_gate = self.stream.read_boolean()
        return MapNode(level_name, connections, node_type, conditions, has_lesser_gate, has_warp_gate)


class MapNodeConnectionReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'FezEngine.Structure.MapNode+Connection'
    reader_name = 'FezEngine.Readers.MapNodeConnectionReader'

    def read(self):
        face = self.stream.read_object(FaceOrientationReader)
        node = self.stream.read_object(MapNodeReader)
        branch_oversize = self.stream.read_single()
        return MapNodeConnection(face, node, branch_oversize)


class WinConditionsReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'FezEngine.Structure.WinConditions'
    reader_name = 'FezEngine.Readers.WinConditionsReader'

    def read(self):
        chest_count = self.stream.read_int32()
        locked_door_count = self.stream.read_int32()
        unlocked_door_count = self.stream.read_int32()
        script_ids = self.stream.read_object(ListReader, [Int32Reader])
        cube_shard_count = self.stream.read_int32()
        other_collectible_count = self.stream.read_int32()
        split_up_count = self.stream.read_int32()
        secret_count = self.stream.read_int32()
        return WinConditions(chest_count, locked_door_count, unlocked_door_count, script_ids, cube_shard_count,
                             other_collectible_count, split_up_count, secret_count)


class SkyReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'FezEngine.Structure.Sky'
    reader_name = 'FezEngine.Readers.SkyReader'

    def read(self):
        name = self.stream.read_string()
        background = self.stream.read_string()
        wind_speed = self.stream.read_single()
        density = self.stream.read_single()
        fog_density = self.stream.read_single()
        layers = self.stream.read_object(ListReader, [SkyLayerReader])
        clouds = self.stream.read_object(ListReader, [StringReader])
        shadows = self.stream.read_object(StringReader)
        stars = self.stream.read_object(StringReader)
        cloud_tint = self.stream.read_object(StringReader)
        vertical_tiling = self.stream.read_boolean()
        horizontal_scrolling = self.stream.read_boolean()
        layer_base_height = self.stream.read_single()
        inter_layer_vertical_distance = self.stream.read_single()
        inter_layer_horizontal_distance = self.stream.read_single()
        horizontal_distance = self.stream.read_single()
        vertical_distance = self.stream.read_single()
        layer_base_spacing = self.stream.read_single()
        wind_parallax = self.stream.read_single()
        wind_distance = self.stream.read_single()
        clouds_parallax = self.stream.read_single()
        shadow_opacity = self.stream.read_single()
        foliage_shadows = self.stream.read_boolean()
        no_per_face_layer_x_offset = self.stream.read_boolean()
        layer_base_x_offset = self.stream.read_single()
        return Sky(name, background, wind_speed, density, fog_density, layers, clouds, shadows, stars, cloud_tint,
                   vertical_tiling, horizontal_scrolling, layer_base_height, inter_layer_vertical_distance,
                   inter_layer_horizontal_distance, horizontal_distance, vertical_distance, layer_base_spacing,
                   wind_parallax, wind_distance, clouds_parallax, shadow_opacity, foliage_shadows,
                   no_per_face_layer_x_offset, layer_base_x_offset)


class SkyLayerReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'FezEngine.Structure.SkyLayer'
    reader_name = 'FezEngine.Readers.SkyLayerReader'

    def read(self):
        name = self.stream.read_string()
        in_front = self.stream.read_boolean()
        opacity = self.stream.read_single()
        fog_tint = self.stream.read_single()
        return SkyLayer(name, in_front, opacity, fog_tint)


class TrileSetReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'FezEngine.Structure.TrileSet'
    reader_name = 'FezEngine.Readers.TrileSetReader'

    def read(self):
        name = self.stream.read_string()
        triles = self.stream.read_object(DictionaryReader, [Int32Reader, TrileReader])
        texture_atlas = self.stream.read_object(Texture2DReader)
        return TrileSet(name, triles, texture_atlas)


class TrileReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'FezEngine.Structure.Trile'
    reader_name = 'FezEngine.Readers.TrileReader'

    def read(self):
        name = self.stream.read_string()
        cubemap_path = self.stream.read_string()
        size = self.stream.read_vector3()
        offset = self.stream.read_vector3()
        immaterial = self.stream.read_boolean()
        see_through = self.stream.read_boolean()
        thin = self.stream.read_boolean()
        force_hugging = self.stream.read_boolean()
        faces = self.stream.read_object(DictionaryReader, [FaceOrientationReader, CollisionTypeReader])
        geometry = self.stream.read_object(ShaderInstancedIndexedPrimitivesReader,
                                           [VertexPositionNormalTextureInstanceReader, Vector4Reader])
        actor_settings_type = self.stream.read_object(ActorTypeReader)
        actor_settings_face = self.stream.read_object(FaceOrientationReader)
        surface_type = self.stream.read_object(SurfaceTypeReader)
        atlas_offset = self.stream.read_vector2()
        return Trile(name, cubemap_path, size, offset, immaterial, see_through, thin, force_hugging, faces, geometry,
                     actor_settings_type, actor_settings_face, surface_type, atlas_offset)


class LevelReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'FezEngine.Structure.Level'
    reader_name = 'FezEngine.Readers.LevelReader'

    def read(self):
        name = self.stream.read_object(StringReader)
        size = self.stream.read_vector3()
        starting_position = self.stream.read_object(TrileFaceReader)
        sequence_samples_path = self.stream.read_object(StringReader)
        flat = self.stream.read_boolean()
        skip_postprocess = self.stream.read_boolean()
        base_diffuse = self.stream.read_single()
        base_ambient = self.stream.read_single()
        gomez_halo_name = self.stream.read_object(StringReader)
        halo_filtering = self.stream.read_boolean()
        blinking_alpha = self.stream.read_boolean()
        loops = self.stream.read_boolean()
        water_type = self.stream.read_object(LiquidTypeReader)
        water_height = self.stream.read_single()
        sky_name = self.stream.read_string()
        trile_set_name = self.stream.read_object(StringReader)
        volumes = self.stream.read_object(DictionaryReader, [Int32Reader, VolumeReader])
        scripts = self.stream.read_object(DictionaryReader, [Int32Reader, ScriptReader])
        song_name = self.stream.read_object(StringReader)
        fap_fadeout_start = self.stream.read_int32()
        fap_fadeout_length = self.stream.read_int32()
        triles = self.stream.read_object(DictionaryReader, [TrileEmplacementReader, TrileInstanceReader])
        art_objects = self.stream.read_object(DictionaryReader, [Int32Reader, ArtObjectInstanceReader])
        background_planes = self.stream.read_object(DictionaryReader, [Int32Reader, BackgroundPlaneReader])
        groups = self.stream.read_object(DictionaryReader, [Int32Reader, TrileGroupReader])
        nonplayer_characters = self.stream.read_object(DictionaryReader, [Int32Reader, NpcInstanceReader])
        paths = self.stream.read_object(DictionaryReader, [Int32Reader, MovementPathReader])
        descending = self.stream.read_boolean()
        rainy = self.stream.read_boolean()
        low_pass = self.stream.read_boolean()
        muted_loops = self.stream.read_object(ListReader, [StringReader])
        ambience_tracks = self.stream.read_object(ListReader, [AmbienceTrackReader])
        node_type = self.stream.read_object(LevelNodeTypeReader)
        quantum = self.stream.read_boolean()
        return Level(name, size, starting_position, sequence_samples_path, flat, skip_postprocess, base_diffuse,
                     base_ambient, gomez_halo_name, halo_filtering, blinking_alpha, loops, water_type, water_height,
                     sky_name, trile_set_name, volumes, scripts, song_name, fap_fadeout_start, fap_fadeout_length,
                     triles, art_objects, background_planes, groups, nonplayer_characters, paths, descending, rainy,
                     low_pass, muted_loops, ambience_tracks, node_type, quantum)


class VolumeReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'FezEngine.Structure.Volume'
    reader_name = 'FezEngine.Readers.VolumeReader'

    def read(self):
        orientations = self.stream.read_object(ArrayReader, [FaceOrientationReader])
        v_from = self.stream.read_vector3()
        v_to = self.stream.read_vector3()
        actor_settings = self.stream.read_object(VolumeActorSettingsReader)
        return Volume(orientations, v_from, v_to, actor_settings)


class TrileEmplacementReader(ValueTypeReader, TypeReaderPlugin):
    target_type = 'FezEngine.Structure.TrileEmplacement'
    reader_name = 'FezEngine.Readers.TrileEmplacementReader'

    def read(self):
        return TrileEmplacement._make(self.stream.unpack('3i'))


class TrileInstanceReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'FezEngine.Structure.TrileInstance'
    reader_name = 'FezEngine.Readers.TrileInstanceReader'

    def read(self):
        values = self.stream.unpack('3f i B ?')
        position = Vector3._make(values[0:3])
        trile_id = values[3]
        orientation = values[4]
        actor_settings = None
        has_actor_settings = values[5]
        if has_actor_settings:
            actor_settings = self.stream.read_object(InstanceActorSettingsReader)
        overlapped_triles = self.stream.read_object(ListReader, [TrileInstanceReader])
        return TrileInstance(position, trile_id, orientation, actor_settings, overlapped_triles)


class ArtObjectInstanceReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'FezEngine.Structure.ArtObjectInstance'
    reader_name = 'FezEngine.Readers.ArtObjectInstanceReader'

    def read(self):
        name = self.stream.read_string()
        values = self.stream.unpack('3f 4f 3f')
        position = Vector3._make(values[0:3])
        rotation = Quaternion._make(values[3:7])
        scale = Vector3._make(values[7:10])
        actor_settings = self.stream.read_object(ArtObjectActorSettingsReader)
        return ArtObjectInstance(name, position, rotation, scale, actor_settings)


class BackgroundPlaneReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'FezEngine.Structure.BackgroundPlane'
    reader_name = 'FezEngine.Readers.BackgroundPlaneReader'

    def read(self):
        position = self.stream.read_vector3()
        rotation = self.stream.read_quaternion()
        scale = self.stream.read_vector3()
        size = self.stream.read_vector3()
        texture_name = self.stream.read_string()
        light_map = self.stream.read_boolean()
        allow_overbrightness = self.stream.read_boolean()
        filter_ = self.stream.read_color()
        animated = self.stream.read_boolean()
        doublesided = self.stream.read_boolean()
        opacity = self.stream.read_single()
        attached_group = self.stream.read_object(Int32Reader)
        billboard = self.stream.read_boolean()
        sync_with_samples = self.stream.read_boolean()
        crosshatch = self.stream.read_boolean()
        unknown = self.stream.read_boolean()
        always_on_top = self.stream.read_boolean()
        fullbright = self.stream.read_boolean()
        pixelated_lightmap = self.stream.read_boolean()
        x_texture_repeat = self.stream.read_boolean()
        y_texture_repeat = self.stream.read_boolean()
        clamp_texture = self.stream.read_boolean()
        actor_type = self.stream.read_object(ActorTypeReader)
        attached_plane = self.stream.read_object(Int32Reader)
        parallax_factor = self.stream.read_single()
        return BackgroundPlane(position, rotation, scale, size, texture_name, light_map, allow_overbrightness, filter_,
                               animated, doublesided, opacity, attached_group, billboard, sync_with_samples, crosshatch,
                               unknown, always_on_top, fullbright, pixelated_lightmap, x_texture_repeat,
                               y_texture_repeat, clamp_texture, actor_type, attached_plane, parallax_factor)


class TrileGroupReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'FezEngine.Structure.TrileGroup'
    reader_name = 'FezEngine.Readers.TrileGroupReader'

    def read(self):
        triles = self.stream.read_object(ListReader, [TrileInstanceReader])
        path = self.stream.read_object(MovementPathReader)
        heavy = self.stream.read_boolean()
        actor_type = self.stream.read_object(ActorTypeReader)
        geyser_offset = self.stream.read_single()
        geyser_pause_for = self.stream.read_single()
        geyser_lift_for = self.stream.read_single()
        geyser_apex_height = self.stream.read_single()
        spin_center = self.stream.read_vector3()
        spin_clockwise = self.stream.read_boolean()
        spin_frequency = self.stream.read_single()
        spin_needs_triggering = self.stream.read_boolean()
        spin_180_degrees = self.stream.read_boolean()
        fall_on_rotate = self.stream.read_boolean()
        spin_offset = self.stream.read_single()
        associated_sound = self.stream.read_object(StringReader)
        return TrileGroup(triles, path, heavy, actor_type, geyser_offset, geyser_pause_for, geyser_lift_for,
                          geyser_apex_height, spin_center, spin_clockwise, spin_frequency, spin_needs_triggering,
                          spin_180_degrees, fall_on_rotate, spin_offset, associated_sound)


class TrileFaceReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'FezEngine.Structure.TrileFace'
    reader_name = 'FezEngine.Readers.TrileFaceReader'

    def read(self):
        trile_id = self.stream.read_object(TrileEmplacementReader)
        face = self.stream.read_object(FaceOrientationReader)
        return TrileFace(trile_id, face)


class NpcInstanceReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'FezEngine.Structure.NpcInstance'
    reader_name = 'FezEngine.Readers.NpcInstanceReader'

    def read(self):
        name = self.stream.read_string()
        position = self.stream.read_vector3()
        destination_offset = self.stream.read_vector3()
        walk_speed = self.stream.read_single()
        randomize_speech = self.stream.read_boolean()
        say_first_speech_line_once = self.stream.read_boolean()
        avoids_gomez = self.stream.read_boolean()
        actor_type = self.stream.read_object(ActorTypeReader)
        speech = self.stream.read_object(ListReader, [SpeechLineReader])
        actions = self.stream.read_object(DictionaryReader, [NpcActionReader, NpcActionContentReader])
        return NpcInstance(name, position, destination_offset, walk_speed, randomize_speech, say_first_speech_line_once,
                           avoids_gomez, actor_type, speech, actions)


class MovementPathReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'FezEngine.Structure.MovementPath'
    reader_name = 'FezEngine.Readers.MovementPathReader'

    def read(self):
        segments = self.stream.read_object(ListReader, [PathSegmentReader])
        needs_trigger = self.stream.read_boolean()
        end_behavior = self.stream.read_object(PathEndBehaviorReader)
        sound_name = self.stream.read_object(StringReader)
        is_spline = self.stream.read_boolean()
        offset_seconds = self.stream.read_single()
        save_trigger = self.stream.read_boolean()
        return MovementPath(segments, needs_trigger, end_behavior, sound_name, is_spline, offset_seconds, save_trigger)


class AmbienceTrackReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'FezEngine.Structure.AmbienceTrack'
    reader_name = 'FezEngine.Readers.AmbienceTrackReader'

    def read(self):
        name = self.stream.read_object(StringReader)
        dawn = self.stream.read_boolean()
        day = self.stream.read_boolean()
        dusk = self.stream.read_boolean()
        night = self.stream.read_boolean()
        return AmbienceTrack(name, dawn, day, dusk, night)


class VolumeActorSettingsReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'FezEngine.Structure.VolumeActorSettings'
    reader_name = 'FezEngine.Readers.VolumeActorSettingsReader'

    def read(self):
        faraway_plane_offset = self.stream.read_vector2()
        is_point_of_interest = self.stream.read_boolean()
        dot_dialogue = self.stream.read_object(ListReader, [DotDialogueLineReader])
        water_locked = self.stream.read_boolean()
        code_pattern = self.stream.read_object(ArrayReader, [CodeInputReader])
        is_blackhole = self.stream.read_boolean()
        needs_trigger = self.stream.read_boolean()
        is_secret_passage = self.stream.read_boolean()
        return VolumeActorSettings(faraway_plane_offset, is_point_of_interest, dot_dialogue, water_locked, code_pattern,
                                   is_blackhole, needs_trigger, is_secret_passage)


class DotDialogueLineReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'FezEngine.Structure.DotDialogueLine'
    reader_name = 'FezEngine.Readers.DotDialogueLineReader'

    def read(self):
        resource_text = self.stream.read_object(StringReader)
        grouped = self.stream.read_boolean()
        return DotDialogueLine(resource_text, grouped)


class ScriptReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'FezEngine.Structure.Scripting.Script'
    reader_name = 'FezEngine.Readers.ScriptReader'

    def read(self):
        name = self.stream.read_string()
        timeout = self.stream.read_object(TimeSpanReader)
        triggers = self.stream.read_object(ListReader, [ScriptTriggerReader])
        conditions = self.stream.read_object(ListReader, [ScriptConditionReader])
        actions = self.stream.read_object(ListReader, [ScriptActionReader])
        one_time = self.stream.read_boolean()
        triggerless = self.stream.read_boolean()
        ignore_end_triggers = self.stream.read_boolean()
        level_wide_one_time = self.stream.read_boolean()
        disabled = self.stream.read_boolean()
        is_win_condition = self.stream.read_boolean()
        return Script(name, timeout, triggers, conditions, actions, one_time, triggerless, ignore_end_triggers,
                      level_wide_one_time, disabled, is_win_condition)


class ScriptTriggerReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'FezEngine.Structure.Scripting.ScriptTrigger'
    reader_name = 'FezEngine.Readers.ScriptTriggerReader'

    def read(self):
        entity = self.stream.read_object(EntityReader)
        event = self.stream.read_string()
        return ScriptTrigger(entity, event)


class ScriptActionReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'FezEngine.Structure.Scripting.ScriptAction'
    reader_name = 'FezEngine.Readers.ScriptActionReader'

    def read(self):
        entity = self.stream.read_object(EntityReader)
        operation = self.stream.read_string()
        arguments = self.stream.read_object(ArrayReader, [StringReader])
        killswitch = self.stream.read_boolean()
        blocking = self.stream.read_boolean()
        return ScriptAction(entity, operation, arguments, killswitch, blocking)


class ScriptConditionReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'FezEngine.Structure.Scripting.ScriptCondition'
    reader_name = 'FezEngine.Readers.ScriptConditionReader'

    def read(self):
        entity = self.stream.read_object(EntityReader)
        operator = self.stream.read_object(ComparisonOperatorReader)
        property_ = self.stream.read_string()
        value = self.stream.read_string()
        return ScriptCondition(entity, operator, property_, value)


class EntityReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'FezEngine.Structure.Scripting.Entity'
    reader_name = 'FezEngine.Readers.EntityReader'

    def read(self):
        entity_type = self.stream.read_string()
        identifier = self.stream.read_object(Int32Reader)
        return Entity(entity_type, identifier)


class InstanceActorSettingsReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'FezEngine.Structure.InstanceActorSettings'
    reader_name = 'FezEngine.Readers.InstanceActorSettingsReader'

    def read(self):
        contained_trile = self.stream.read_object(Int32Reader)
        sign_text = self.stream.read_object(StringReader)
        sequence = self.stream.read_object(ArrayReader, [BooleanReader])
        sequence_sample_name = self.stream.read_object(StringReader)
        sequence_alternate_sample_name = self.stream.read_object(StringReader)
        host_volume = self.stream.read_object(Int32Reader)
        return InstanceActorSettings(contained_trile, sign_text, sequence, sequence_sample_name,
                                     sequence_alternate_sample_name, host_volume)


class ArtObjectActorSettingsReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'FezEngine.Structure.ArtObjectActorSettings'
    reader_name = 'FezEngine.Readers.ArtObjectActorSettingsReader'

    def read(self):
        inactive = self.stream.read_boolean()
        contained_trile = self.stream.read_object(ActorTypeReader)
        attached_group = self.stream.read_object(Int32Reader)
        spin_view = self.stream.read_object(ViewpointReader)
        spin_every = self.stream.read_single()
        spin_offset = self.stream.read_single()
        off_center = self.stream.read_boolean()
        rotation_center = self.stream.read_vector3()
        vibration_pattern = self.stream.read_object(ArrayReader, [VibrationMotorReader])
        code_pattern = self.stream.read_object(ArrayReader, [CodeInputReader])
        segment = self.stream.read_object(PathSegmentReader)
        next_node = self.stream.read_object(Int32Reader)
        destination_level = self.stream.read_object(StringReader)
        treasure_map_name = self.stream.read_object(StringReader)
        invisible_sides = self.stream.read_object(ArrayReader, [FaceOrientationReader])
        timeswitch_wind_back_speed = self.stream.read_single()
        return ArtObjectActorSettings(inactive, contained_trile, attached_group, spin_view, spin_every, spin_offset,
                                      off_center, rotation_center, vibration_pattern, code_pattern, segment, next_node,
                                      destination_level, treasure_map_name, invisible_sides, timeswitch_wind_back_speed)


class PathSegmentReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'FezEngine.Structure.PathSegment'
    reader_name = 'FezEngine.Readers.PathSegmentReader'

    def read(self):
        destination = self.stream.read_vector3()
        duration = self.stream.read_object(TimeSpanReader)
        wait_time_on_start = self.stream.read_object(TimeSpanReader)
        wait_time_on_finish = self.stream.read_object(TimeSpanReader)
        acceleration = self.stream.read_single()
        deceleration = self.stream.read_single()
        jitter_factor = self.stream.read_single()
        orientation = self.stream.read_quaternion()
        custom_data = None
        has_custom_data = self.stream.read_boolean()
        if has_custom_data:
            custom_data = self.stream.read_object(CameraNodeDataReader)
        return PathSegment(destination, duration, wait_time_on_start, wait_time_on_finish, acceleration, deceleration,
                           jitter_factor, orientation, custom_data)


class SpeechLineReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'FezEngine.Structure.SpeechLine'
    reader_name = 'FezEngine.Readers.SpeechLineReader'

    def read(self):
        text = self.stream.read_object(StringReader)
        override_content = self.stream.read_object(NpcActionContentReader)
        return SpeechLine(text, override_content)


class NpcActionContentReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'FezEngine.Structure.NpcActionContent'
    reader_name = 'FezEngine.Readers.NpcActionContentReader'

    def read(self):
        animation_name = self.stream.read_object(StringReader)
        sound_name = self.stream.read_object(StringReader)
        return NpcActionContent(animation_name, sound_name)


class CameraNodeDataReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'FezEngine.Structure.CameraNodeData'
    reader_name = 'FezEngine.Readers.CameraNodeDataReader'

    def read(self):
        perspective = self.stream.read_boolean()
        pixels_per_trixel = self.stream.read_int32()
        sound_name = self.stream.read_object(StringReader)
        return CameraNodeData(perspective, pixels_per_trixel, sound_name)

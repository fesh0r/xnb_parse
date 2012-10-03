"""
FEZ level type readers
"""

from xnb_parse.type_reader import BaseTypeReader
from xnb_parse.type_reader_manager import TypeReaderPlugin
from xnb_parse.type_readers.xna_graphics import Texture2DReader
from xnb_parse.type_readers.xna_math import Vector4Reader
from xnb_parse.type_readers.xna_system import ListReader, EnumReader, DictionaryReader
from xnb_parse.type_readers.xna_primitive import Int32Reader, StringReader
from xnb_parse.type_readers.fez.fez_basic import LevelNodeTypeReader, FaceOrientationReader, CollisionTypeReader
from xnb_parse.type_readers.fez.fez_basic import ActorTypeReader, SurfaceTypeReader
from xnb_parse.type_readers.fez.fez_graphics import ShaderInstancedIndexedPrimitivesReader
from xnb_parse.type_readers.fez.fez_graphics import VertexPositionNormalTextureInstanceReader


class MapTreeReader(BaseTypeReader, TypeReaderPlugin):
    target_type = u'FezEngine.Structure.MapTree'
    reader_name = u'FezEngine.Readers.MapTreeReader'

    def read(self):
        root = self.stream.read_object(MapNodeReader)
        return root


class MapNodeReader(BaseTypeReader, TypeReaderPlugin):
    target_type = u'FezEngine.Structure.MapNode'
    reader_name = u'FezEngine.Readers.MapNodeReader'

    def read(self):
        level_name = self.stream.read_string()
        connections = self.stream.read_object(ListReader, [MapNodeConnectionReader])
        node_type = self.stream.read_object(EnumReader, [LevelNodeTypeReader])
        conditions = self.stream.read_object(WinConditionsReader)
        has_lesser_gate = self.stream.read_boolean()
        has_warp_gate = self.stream.read_boolean()
        return level_name, connections, node_type, conditions, has_lesser_gate, has_warp_gate


class MapNodeConnectionReader(BaseTypeReader, TypeReaderPlugin):
    target_type = u'FezEngine.Structure.MapNode+Connection'
    reader_name = u'FezEngine.Readers.MapNodeConnectionReader'

    def read(self):
        face = self.stream.read_object(EnumReader, [FaceOrientationReader])
        node = self.stream.read_object(MapNodeReader)
        branch_oversize = self.stream.read_single()
        return face, node, branch_oversize


class WinConditionsReader(BaseTypeReader, TypeReaderPlugin):
    target_type = u'FezEngine.Structure.WinConditions'
    reader_name = u'FezEngine.Readers.WinConditionsReader'

    def read(self):
        chest_count = self.stream.read_int32()
        locked_door_count = self.stream.read_int32()
        unlocked_door_count = self.stream.read_int32()
        script_ids = self.stream.read_object(ListReader, [Int32Reader])
        cube_shard_count = self.stream.read_int32()
        other_collectible_count = self.stream.read_int32()
        split_up_count = self.stream.read_int32()
        secret_count = self.stream.read_int32()
        return (chest_count, locked_door_count, unlocked_door_count, script_ids, cube_shard_count,
                other_collectible_count, split_up_count, secret_count)


class SkyReader(BaseTypeReader, TypeReaderPlugin):
    target_type = u'FezEngine.Structure.Sky'
    reader_name = u'FezEngine.Readers.SkyReader'

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
        return (name, background, wind_speed, density, fog_density, layers, clouds, shadows, stars, cloud_tint,
                vertical_tiling, horizontal_scrolling, layer_base_height, inter_layer_vertical_distance,
                inter_layer_horizontal_distance, horizontal_distance, vertical_distance, layer_base_spacing,
                wind_parallax, wind_distance, clouds_parallax, shadow_opacity, foliage_shadows,
                no_per_face_layer_x_offset, layer_base_x_offset)


class SkyLayerReader(BaseTypeReader, TypeReaderPlugin):
    target_type = u'FezEngine.Structure.SkyLayer'
    reader_name = u'FezEngine.Readers.SkyLayerReader'

    def read(self):
        name = self.stream.read_string()
        in_front = self.stream.read_boolean()
        opacity = self.stream.read_single()
        fog_tint = self.stream.read_single()
        return name, in_front, opacity, fog_tint


class TrileSetReader(BaseTypeReader, TypeReaderPlugin):
    target_type = u'FezEngine.Structure.TrileSet'
    reader_name = u'FezEngine.Readers.TrileSetReader'

    def read(self):
        name = self.stream.read_string()
        triles = self.stream.read_object(DictionaryReader, [Int32Reader, TrileReader])
        texture_atlas = self.stream.read_object(Texture2DReader)
        return name, triles, texture_atlas


class TrileReader(BaseTypeReader, TypeReaderPlugin):
    target_type = u'FezEngine.Structure.Trile'
    reader_name = u'FezEngine.Readers.TrileReader'

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
        actor_settings_type = self.stream.read_object(EnumReader, [ActorTypeReader])
        actor_settings_face = self.stream.read_object(EnumReader, [FaceOrientationReader])
        surface_type = self.stream.read_object(EnumReader, [SurfaceTypeReader])
        atlas_offset = self.stream.read_vector2()
        return (name, cubemap_path, size, offset, immaterial, see_through, thin, force_hugging, faces, geometry,
                actor_settings_type, actor_settings_face, surface_type, atlas_offset)


class LevelReader(BaseTypeReader, TypeReaderPlugin):
    target_type = u'FezEngine.Structure.Level'
    reader_name = u'FezEngine.Readers.LevelReader'


class VolumeReader(BaseTypeReader, TypeReaderPlugin):
    target_type = u'FezEngine.Structure.Volume'
    reader_name = u'FezEngine.Readers.VolumeReader'


class TrileEmplacementReader(BaseTypeReader, TypeReaderPlugin):
    target_type = u'FezEngine.Structure.TrileEmplacement'
    reader_name = u'FezEngine.Readers.TrileEmplacementReader'


class TrileInstanceReader(BaseTypeReader, TypeReaderPlugin):
    target_type = u'FezEngine.Structure.TrileInstance'
    reader_name = u'FezEngine.Readers.TrileInstanceReader'


class ArtObjectInstanceReader(BaseTypeReader, TypeReaderPlugin):
    target_type = u'FezEngine.Structure.ArtObjectInstance'
    reader_name = u'FezEngine.Readers.ArtObjectInstanceReader'


class BackgroundPlaneReader(BaseTypeReader, TypeReaderPlugin):
    target_type = u'FezEngine.Structure.BackgroundPlane'
    reader_name = u'FezEngine.Readers.BackgroundPlaneReader'


class TrileGroupReader(BaseTypeReader, TypeReaderPlugin):
    target_type = u'FezEngine.Structure.TrileGroup'
    reader_name = u'FezEngine.Readers.TrileGroupReader'


class TrileFaceReader(BaseTypeReader, TypeReaderPlugin):
    target_type = u'FezEngine.Structure.TrileFace'
    reader_name = u'FezEngine.Readers.TrileFaceReader'


class NpcInstanceReader(BaseTypeReader, TypeReaderPlugin):
    target_type = u'FezEngine.Structure.NpcInstance'
    reader_name = u'FezEngine.Readers.NpcInstanceReader'


class MovementPathReader(BaseTypeReader, TypeReaderPlugin):
    target_type = u'FezEngine.Structure.MovementPath'
    reader_name = u'FezEngine.Readers.MovementPathReader'


class AmbienceTrackReader(BaseTypeReader, TypeReaderPlugin):
    target_type = u'FezEngine.Structure.AmbienceTrack'
    reader_name = u'FezEngine.Readers.AmbienceTrackReader'


class VolumeActorSettingsReader(BaseTypeReader, TypeReaderPlugin):
    target_type = u'FezEngine.Structure.VolumeActorSettings'
    reader_name = u'FezEngine.Readers.VolumeActorSettingsReader'


class DotDialogueLineReader(BaseTypeReader, TypeReaderPlugin):
    target_type = u'FezEngine.Structure.DotDialogueLine'
    reader_name = u'FezEngine.Readers.DotDialogueLineReader'


class ScriptReader(BaseTypeReader, TypeReaderPlugin):
    target_type = u'FezEngine.Structure.Scripting.Script'
    reader_name = u'FezEngine.Readers.ScriptReader'


class ScriptTriggerReader(BaseTypeReader, TypeReaderPlugin):
    target_type = u'FezEngine.Structure.Scripting.ScriptTrigger'
    reader_name = u'FezEngine.Readers.ScriptTriggerReader'


class ScriptActionReader(BaseTypeReader, TypeReaderPlugin):
    target_type = u'FezEngine.Structure.Scripting.ScriptAction'
    reader_name = u'FezEngine.Readers.ScriptActionReader'


class ScriptConditionReader(BaseTypeReader, TypeReaderPlugin):
    target_type = u'FezEngine.Structure.Scripting.ScriptCondition'
    reader_name = u'FezEngine.Readers.ScriptConditionReader'


class EntityReader(BaseTypeReader, TypeReaderPlugin):
    target_type = u'FezEngine.Structure.Scripting.Entity'
    reader_name = u'FezEngine.Readers.EntityReader'


class InstanceActorSettingsReader(BaseTypeReader, TypeReaderPlugin):
    target_type = u'FezEngine.Structure.InstanceActorSettings'
    reader_name = u'FezEngine.Readers.InstanceActorSettingsReader'


class ArtObjectActorSettingsReader(BaseTypeReader, TypeReaderPlugin):
    target_type = u'FezEngine.Structure.ArtObjectActorSettings'
    reader_name = u'FezEngine.Readers.ArtObjectActorSettingsReader'


class PathSegmentReader(BaseTypeReader, TypeReaderPlugin):
    target_type = u'FezEngine.Structure.PathSegment'
    reader_name = u'FezEngine.Readers.PathSegmentReader'


class SpeechLineReader(BaseTypeReader, TypeReaderPlugin):
    target_type = u'FezEngine.Structure.SpeechLine'
    reader_name = u'FezEngine.Readers.SpeechLineReader'


class NpcActionContentReader(BaseTypeReader, TypeReaderPlugin):
    target_type = u'FezEngine.Structure.NpcActionContent'
    reader_name = u'FezEngine.Readers.NpcActionContentReader'


class CameraNodeDataReader(BaseTypeReader, TypeReaderPlugin):
    target_type = u'FezEngine.Structure.CameraNodeData'
    reader_name = u'FezEngine.Readers.CameraNodeDataReader'

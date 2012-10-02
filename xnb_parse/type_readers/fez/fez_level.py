"""
FEZ level type readers
"""

from xnb_parse.type_reader import BaseTypeReader
from xnb_parse.type_reader_manager import TypeReaderPlugin
from xnb_parse.type_readers.xna_graphics import Texture2DReader
from xnb_parse.type_readers.xna_math import Vector3Reader, Vector2Reader, Vector4Reader
from xnb_parse.type_readers.xna_system import ListReader, EnumReader, DictionaryReader
from xnb_parse.type_readers.xna_primitive import Int32Reader, StringReader
from xnb_parse.type_readers.fez.fez_basic import LevelNodeTypeReader, FaceOrientationReader, CollisionTypeReader
from xnb_parse.type_readers.fez.fez_basic import ActorTypeReader, SurfaceTypeReader
from xnb_parse.type_readers.fez.fez_graphics import ShaderInstancedIndexedPrimitivesReader
from xnb_parse.type_readers.fez.fez_graphics import VertexPositionNormalTextureInstanceReader


class MapTreeReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'FezEngine.Structure.MapTree'
    reader_name = 'FezEngine.Readers.MapTreeReader'

    def read(self):
        root = self.stream.read_object(MapNodeReader)
        return root


class MapNodeReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'FezEngine.Structure.MapNode'
    reader_name = 'FezEngine.Readers.MapNodeReader'

    def read(self):
        level_name = self.stream.read('str')
        connections = self.stream.read_object(ListReader, [MapNodeConnectionReader])
        node_type = self.stream.read_object(EnumReader, [LevelNodeTypeReader])
        conditions = self.stream.read_object(WinConditionsReader)
        has_lesser_gate = self.stream.read('?')
        has_warp_gate = self.stream.read('?')
        return level_name, connections, node_type, conditions, has_lesser_gate, has_warp_gate


class MapNodeConnectionReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'FezEngine.Structure.MapNode+Connection'
    reader_name = 'FezEngine.Readers.MapNodeConnectionReader'

    def read(self):
        face = self.stream.read_object(EnumReader, [FaceOrientationReader])
        node = self.stream.read_object(MapNodeReader)
        branch_oversize = self.stream.read('f')
        return face, node, branch_oversize


class WinConditionsReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'FezEngine.Structure.WinConditions'
    reader_name = 'FezEngine.Readers.WinConditionsReader'

    def read(self):
        chest_count = self.stream.read('s4')
        locked_door_count = self.stream.read('s4')
        unlocked_door_count = self.stream.read('s4')
        script_ids = self.stream.read_object(ListReader, [Int32Reader])
        cube_shard_count = self.stream.read('s4')
        other_collectible_count = self.stream.read('s4')
        split_up_count = self.stream.read('s4')
        secret_count = self.stream.read('s4')
        return (chest_count, locked_door_count, unlocked_door_count, script_ids, cube_shard_count,
                other_collectible_count, split_up_count, secret_count)


class SkyReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'FezEngine.Structure.Sky'
    reader_name = 'FezEngine.Readers.SkyReader'

    def read(self):
        name = self.stream.read('str')
        background = self.stream.read('str')
        wind_speed = self.stream.read('f')
        density = self.stream.read('f')
        fog_density = self.stream.read('f')
        layers = self.stream.read_object(ListReader, [SkyLayerReader])
        clouds = self.stream.read_object(ListReader, [StringReader])
        shadows = self.stream.read_object(StringReader)
        stars = self.stream.read_object(StringReader)
        cloud_tint = self.stream.read_object(StringReader)
        vertical_tiling = self.stream.read('?')
        horizontal_scrolling = self.stream.read('?')
        layer_base_height = self.stream.read('f')
        inter_layer_vertical_distance = self.stream.read('f')
        inter_layer_horizontal_distance = self.stream.read('f')
        horizontal_distance = self.stream.read('f')
        vertical_distance = self.stream.read('f')
        layer_base_spacing = self.stream.read('f')
        wind_parallax = self.stream.read('f')
        wind_distance = self.stream.read('f')
        clouds_parallax = self.stream.read('f')
        shadow_opacity = self.stream.read('f')
        foliage_shadows = self.stream.read('?')
        no_per_face_layer_x_offset = self.stream.read('?')
        layer_base_x_offset = self.stream.read('f')
        return (name, background, wind_speed, density, fog_density, layers, clouds, shadows, stars, cloud_tint,
                vertical_tiling, horizontal_scrolling, layer_base_height, inter_layer_vertical_distance,
                inter_layer_horizontal_distance, horizontal_distance, vertical_distance, layer_base_spacing,
                wind_parallax, wind_distance, clouds_parallax, shadow_opacity, foliage_shadows,
                no_per_face_layer_x_offset, layer_base_x_offset)


class SkyLayerReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'FezEngine.Structure.SkyLayer'
    reader_name = 'FezEngine.Readers.SkyLayerReader'

    def read(self):
        name = self.stream.read('str')
        in_front = self.stream.read('?')
        opacity = self.stream.read('f')
        fog_tint = self.stream.read('f')
        return name, in_front, opacity, fog_tint


class TrileSetReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'FezEngine.Structure.TrileSet'
    reader_name = 'FezEngine.Readers.TrileSetReader'

    def read(self):
        name = self.stream.read('str')
        triles = self.stream.read_object(DictionaryReader, [Int32Reader, TrileReader])
        texture_atlas = self.stream.read_object(Texture2DReader)
        return name, triles, texture_atlas


class TrileReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'FezEngine.Structure.Trile'
    reader_name = 'FezEngine.Readers.TrileReader'

    def __init__(self, stream=None, version=None):
        BaseTypeReader.__init__(self, stream=stream, version=version)
        TypeReaderPlugin.__init__(self)
        self.vector2_reader = self.stream.get_type_reader(Vector2Reader)
        self.vector3_reader = self.stream.get_type_reader(Vector3Reader)

    def init_reader(self):
        BaseTypeReader.init_reader(self)
        self.vector2_reader.init_reader()
        self.vector3_reader.init_reader()

    def read(self):
        name = self.stream.read('str')
        cubemap_path = self.stream.read('str')
        size = self.vector3_reader.read()
        offset = self.vector3_reader.read()
        immaterial = self.stream.read('?')
        see_through = self.stream.read('?')
        thin = self.stream.read('?')
        force_hugging = self.stream.read('?')
        faces = self.stream.read_object(DictionaryReader, [FaceOrientationReader, CollisionTypeReader])
        geometry = self.stream.read_object(ShaderInstancedIndexedPrimitivesReader,
                                           [VertexPositionNormalTextureInstanceReader, Vector4Reader])
        actor_settings_type = self.stream.read_object(EnumReader, [ActorTypeReader])
        actor_settings_face = self.stream.read_object(EnumReader, [FaceOrientationReader])
        surface_type = self.stream.read_object(EnumReader, [SurfaceTypeReader])
        atlas_offset = self.vector2_reader.read()
        return (name, cubemap_path, size, offset, immaterial, see_through, thin, force_hugging, faces, geometry,
                actor_settings_type, actor_settings_face, surface_type, atlas_offset)

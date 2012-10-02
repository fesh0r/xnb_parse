"""
FEZ level type readers
"""

from xnb_parse.type_reader import BaseTypeReader
from xnb_parse.type_reader_manager import TypeReaderPlugin
from xnb_parse.type_readers.xna_system import ListReader, EnumReader
from xnb_parse.type_readers.xna_primitive import Int32Reader, StringReader
from xnb_parse.type_readers.fez.fez_basic import LevelNodeTypeReader, FaceOrientationReader


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

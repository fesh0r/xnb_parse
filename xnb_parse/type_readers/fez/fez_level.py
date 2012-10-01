"""
FEZ level type readers
"""

from xnb_parse.type_reader import BaseTypeReader, generic_reader_type
from xnb_parse.type_reader_manager import TypeReaderPlugin
from xnb_parse.type_readers.xna_system import ListReader, EnumReader
from xnb_parse.type_readers.xna_primitive import Int32Reader
from xnb_parse.type_readers.fez.fez_basic import LevelNodeTypeReader, FaceOrientationReader


class MapTreeReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'FezEngine.Structure.MapTree'
    reader_name = 'FezEngine.Readers.MapTreeReader'

    def read(self):
        root = self.stream.read_object(MapNodeReader.target_type)
        return root


class MapNodeReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'FezEngine.Structure.MapNode'
    reader_name = 'FezEngine.Readers.MapNodeReader'

    def read(self):
        level_name = self.stream.read('str')
        connections = self.stream.read_object(generic_reader_type(ListReader, [MapNodeConnectionReader]))
        node_type = self.stream.read_object(generic_reader_type(EnumReader, [LevelNodeTypeReader]))
        conditions = self.stream.read_object(WinConditionsReader.target_type)
        has_lesser_gate = self.stream.read('?')
        has_warp_gate = self.stream.read('?')
        return level_name, connections, node_type, conditions, has_lesser_gate, has_warp_gate


class MapNodeConnectionReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'FezEngine.Structure.MapNode+Connection'
    reader_name = 'FezEngine.Readers.MapNodeConnectionReader'

    def read(self):
        face = self.stream.read_object(generic_reader_type(EnumReader, [FaceOrientationReader]))
        node = self.stream.read_object(MapNodeReader.target_type)
        branch_oversize = self.stream.read('f')
        return face, node, branch_oversize


class WinConditionsReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'FezEngine.Structure.WinConditions'
    reader_name = 'FezEngine.Readers.WinConditionsReader'

    def read(self):
        chest_count = self.stream.read('s4')
        locked_door_count = self.stream.read('s4')
        unlocked_door_count = self.stream.read('s4')
        script_ids = self.stream.read_object(generic_reader_type(ListReader, [Int32Reader]))
        cube_shard_count = self.stream.read('s4')
        other_collectible_count = self.stream.read('s4')
        split_up_count = self.stream.read('s4')
        secret_count = self.stream.read('s4')
        return (chest_count, locked_door_count, unlocked_door_count, script_ids, cube_shard_count,
                other_collectible_count, split_up_count, secret_count)

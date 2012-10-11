"""
FEZ level types
"""

from xnb_parse.file_formats.xml_utils import E


class MapTree(object):
    def __init__(self, map_node):
        self.map_node = map_node

    def __str__(self):
        return "MapTree %s" % self.map_node

    def xml(self):
        return E.MapTree(self.map_node.xml())

    def export(self, _):
        return self.xml()


class MapNode(object):
    def __init__(self, level_name, connections, node_type, conditions, has_lesser_gate, has_warp_gate):
        self.level_name = level_name
        self.connections = connections
        self.node_type = node_type
        self.conditions = conditions
        self.has_lesser_gate = has_lesser_gate
        self.has_warp_gate = has_warp_gate

    def __str__(self):
        return "MapNode '%s' t:%s c:%d" % (self.level_name, self.node_type, len(self.connections))

    def xml(self):
        root = E.Node(name=self.level_name, hasLesserGate=str(self.has_lesser_gate),
                      hasWarpGate=str(self.has_warp_gate), type=str(self.node_type))
        if self.conditions:
            root.append(self.conditions.xml())
        if self.connections:
            root.append(self.connections.xml('Connections'))
        return root


class MapNodeConnection(object):
    def __init__(self, face, node, branch_oversize):
        self.face = face
        self.node = node
        self.branch_oversize = branch_oversize

    def __str__(self):
        return "MapNodeConnection f:%s" % self.face

    def xml(self):
        root = E.Connection(face=str(self.face), branchOversize=str(self.branch_oversize))
        root.append(self.node.xml())
        return root


class WinConditions(object):
    def __init__(self, chest_count, locked_door_count, unlocked_door_count, script_ids, cube_shard_count,
                 other_collectible_count, split_up_count, secret_count):
        self.chest_count = chest_count
        self.locked_door_count = locked_door_count
        self.unlocked_door_count = unlocked_door_count
        self.script_ids = script_ids
        self.cube_shard_count = cube_shard_count
        self.other_collectible_count = other_collectible_count
        self.split_up_count = split_up_count
        self.secret_count = secret_count

    def __str__(self):
        return "WinConditions"

    def xml(self):
        root = E.WinConditions(chests=str(self.chest_count), lockedDoors=str(self.locked_door_count),
                               unlockedDoors=str(self.unlocked_door_count), cubeShards=str(self.cube_shard_count),
                               splitUp=str(self.split_up_count), secrets=str(self.secret_count),
                               others=str(self.other_collectible_count))
        if self.script_ids:
            root.append(self.script_ids.xml('Scripts', 'Script'))
        return root

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


class Sky(object):
    def __init__(self, name, background, wind_speed, density, fog_density, layers, clouds, shadows, stars, cloud_tint,
                 vertical_tiling, horizontal_scrolling, layer_base_height, inter_layer_vertical_distance,
                 inter_layer_horizontal_distance, horizontal_distance, vertical_distance, layer_base_spacing,
                 wind_parallax, wind_distance, clouds_parallax, shadow_opacity, foliage_shadows,
                 no_per_face_layer_x_offset, layer_base_x_offset):
        self.name = name
        self.background = background
        self.wind_speed = wind_speed
        self.density = density
        self.fog_density = fog_density
        self.layers = layers
        self.clouds = clouds
        self.shadows = shadows
        self.stars = stars
        self.cloud_tint = cloud_tint
        self.vertical_tiling = vertical_tiling
        self.horizontal_scrolling = horizontal_scrolling
        self.layer_base_height = layer_base_height
        self.inter_layer_vertical_distance = inter_layer_vertical_distance
        self.inter_layer_horizontal_distance = inter_layer_horizontal_distance
        self.horizontal_distance = horizontal_distance
        self.vertical_distance = vertical_distance
        self.layer_base_spacing = layer_base_spacing
        self.wind_parallax = wind_parallax
        self.wind_distance = wind_distance
        self.clouds_parallax = clouds_parallax
        self.shadow_opacity = shadow_opacity
        self.foliage_shadows = foliage_shadows
        self.no_per_face_layer_x_offset = no_per_face_layer_x_offset
        self.layer_base_x_offset = layer_base_x_offset

    def __str__(self):
        return "Sky '%s' b:'%s' l:%d" % (self.name, self.background, len(self.layers))

    def xml(self):
        root = E.Sky(name=self.name, background=self.background, windSpeed=str(self.wind_speed),
                     density=str(self.density), fogDensity=str(self.fog_density),
                     verticalTiling=str(self.vertical_tiling), horizontalScrolling=str(self.horizontal_scrolling),
                     layerBaseHeight=str(self.layer_base_height),
                     interLayerVerticalDistance=str(self.inter_layer_vertical_distance),
                     interLayerHorizontalDistance=str(self.inter_layer_horizontal_distance),
                     horizontalDistance=str(self.horizontal_distance), verticalDistance=str(self.vertical_distance),
                     layerBaseSpacing=str(self.layer_base_spacing), windParallax=str(self.wind_parallax),
                     windDistance=str(self.wind_distance), cloudsParallax=str(self.clouds_parallax),
                     shadowOpacity=str(self.shadow_opacity), foliageShadows=str(self.foliage_shadows),
                     noPerFaceLayerXOffset=str(self.no_per_face_layer_x_offset),
                     layerBaseXOffset=str(self.layer_base_x_offset))
        if self.shadows:
            root.set('shadows', self.shadows)
        if self.stars:
            root.set('stars', self.stars)
        if self.cloud_tint:
            root.set('cloudTint', self.cloud_tint)
        root.append(self.layers.xml('Layers'))
        root.append(self.clouds.xml('Clouds', 'Cloud'))
        return root

    def export(self, _):
        return self.xml()


class SkyLayer(object):
    def __init__(self, name, in_front, opacity, fog_tint):
        self.name = name
        self.in_front = in_front
        self.opacity = opacity
        self.fog_tint = fog_tint

    def __str__(self):
        return "SkyLayer '%s' o:%f" % (self.name, self.opacity)

    def xml(self):
        return E.SkyLayer(name=self.name, opacity=str(self.opacity), fogTint=str(self.fog_tint),
                          inFront=str(self.in_front))


class TrileSet(object):
    def __init__(self, name, triles, texture_atlas):
        self.name = name
        self.triles = triles
        self.texture_atlas = texture_atlas

    def __str__(self):
        return "TrileSet '%s' c:%d" % (self.name, len(self.triles))

    def xml(self):
        root = E.TrileSet(name=self.name)
        root.append(self.triles.xml('Triles', 'TrileEntry'))
        return root

    def export(self, filename):
        self.texture_atlas.export(filename)
        return self.xml()


class Trile(object):
    def __init__(self, name, cubemap_path, size, offset, immaterial, see_through, thin, force_hugging, faces, geometry,
                 actor_settings_type, actor_settings_face, surface_type, atlas_offset):
        self.name = name
        self.cubemap_path = cubemap_path
        self.size = size
        self.offset = offset
        self.immaterial = immaterial
        self.see_through = see_through
        self.thin = thin
        self.force_hugging = force_hugging
        self.faces = faces
        self.geometry = geometry
        self.actor_settings_type = actor_settings_type
        self.actor_settings_face = actor_settings_face
        self.surface_type = surface_type
        self.atlas_offset = atlas_offset

    def __str__(self):
        return "Trile '%s' c:'%s' s:%d" % (self.name, self.cubemap_path, self.size)

    def xml(self):
        root = E.Trile(name=self.name, cubemapPath=self.cubemap_path, immaterial=str(self.immaterial),
                       seeThrough=str(self.see_through), thin=str(self.thin), forceHugging=str(self.force_hugging),
                       surfaceType=str(self.surface_type))
        root.append(E.ActorSettings(type=str(self.actor_settings_type), face=str(self.actor_settings_face)))
        root.append(E.Size(self.size.xml()))
        root.append(E.Offset(self.offset.xml()))
        root.append(E.AtlasOffset(self.atlas_offset.xml()))
        root.append(self.faces.xml('Faces', 'Face'))
        root.append(E.Geometry(self.geometry.xml()))
        return root

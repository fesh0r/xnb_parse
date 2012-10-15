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


class Trile(object):
    __slots__ = ('name', 'cubemap_path', 'size', 'offset', 'immaterial', 'see_through', 'thin', 'force_hugging',
                 'faces', 'geometry', 'actor_settings_type', 'actor_settings_face', 'surface_type', 'atlas_offset')

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


class Level(object):
    def __init__(self, name, size, starting_position, sequence_samples_path, flat, skip_postprocess, base_diffuse,
                 base_ambient, gomez_halo_name, halo_filtering, blinking_alpha, loops, water_type, water_height,
                 sky_name, trile_set_name, volumes, scripts, song_name, fap_fadeout_start, fap_fadeout_length, triles,
                 art_objects, background_planes, groups, nonplayer_characters, paths, descending, rainy, low_pass,
                 muted_loops, ambience_tracks, node_type, quantum):
        self.name = name
        self.size = size
        self.starting_position = starting_position
        self.sequence_samples_path = sequence_samples_path
        self.flat = flat
        self.skip_postprocess = skip_postprocess
        self.base_diffuse = base_diffuse
        self.base_ambient = base_ambient
        self.gomez_halo_name = gomez_halo_name
        self.halo_filtering = halo_filtering
        self.blinking_alpha = blinking_alpha
        self.loops = loops
        self.water_type = water_type
        self.water_height = water_height
        self.sky_name = sky_name
        self.trile_set_name = trile_set_name
        self.volumes = volumes
        self.scripts = scripts
        self.song_name = song_name
        self.fap_fadeout_start = fap_fadeout_start
        self.fap_fadeout_length = fap_fadeout_length
        self.triles = triles
        self.art_objects = art_objects
        self.background_planes = background_planes
        self.groups = groups
        self.nonplayer_characters = nonplayer_characters
        self.paths = paths
        self.descending = descending
        self.rainy = rainy
        self.low_pass = low_pass
        self.muted_loops = muted_loops
        self.ambience_tracks = ambience_tracks
        self.node_type = node_type
        self.quantum = quantum

    def __str__(self):
        return "Level '%s'" % self.name

    def xml(self):
        root = E.Level(name=self.name, flat=str(self.flat),
                       skipPostprocess=str(self.skip_postprocess), baseDiffuse=str(self.base_diffuse),
                       baseAmbient=str(self.base_ambient),
                       haloFiltering=str(self.halo_filtering), blinkingAlpha=str(self.blinking_alpha),
                       loops=str(self.loops), waterType=str(self.water_type), waterHeight=str(self.water_height),
                       skyName=self.sky_name, trileSetName=self.trile_set_name,
                       fapFadeoutStart=str(self.fap_fadeout_start), fapFadeoutLength=str(self.fap_fadeout_length),
                       descending=str(self.descending), rainy=str(self.rainy), lowPass=str(self.low_pass),
                       nodeType=str(self.node_type), quantum=str(self.quantum))
        root.append(E.Size(self.size.xml()))
        if self.sequence_samples_path:
            root.set('sequenceSamplesPath', self.sequence_samples_path)
        if self.gomez_halo_name:
            root.set('gomezHaloName', self.gomez_halo_name)
        if self.song_name:
            root.set('songName', self.song_name)
        if self.starting_position:
            root.append(E.StartingPosition(self.starting_position.xml()))
        if self.volumes:
            root.append(self.volumes.xml('Volumes'))
        if self.scripts:
            root.append(self.scripts.xml('Scripts'))
        # triles
        # art_objects
        # background_planes
        # groups
        # nonplayer_characters:
        # paths
        if self.muted_loops:
            root.append(self.muted_loops.xml('MutedLoops'))
        # ambience_tracks
        return root


class TrileFace(object):
    def __init__(self, trile_id, face):
        self.trile_id = trile_id
        self.face = face

    def __str__(self):
        return "TrileFace f:%s t:%d,%d,%d" % (self.face, self.trile_id.v_x, self.trile_id.v_y, self.trile_id.v_z)

    def xml(self):
        root = E.TrileFace(face=str(self.face))
        root.append(E.TrileId(self.trile_id.xml()))
        return root


class TrileEmplacement(object):
    def __init__(self, v_x, v_y, v_z):
        self.v_x = v_x
        self.v_y = v_y
        self.v_z = v_z

    def __str__(self):
        return "TrileEmplacement(%d,%d,%d)" % (self.v_x, self.v_y, self.v_z)

    def xml(self):
        return E.TrileEmplacement(x=str(self.v_x), y=str(self.v_y), z=str(self.v_z))


class Volume(object):
    def __init__(self, orientations, v_from, v_to, actor_settings):
        self.orientations = orientations
        self.v_from = v_from
        self.v_to = v_to
        self.actor_settings = actor_settings

    def __str__(self):
        return "Volume"

    def xml(self):
        root = E.Volume()
        if self.orientations:
            root.append(self.orientations.xml('Orientations'))
        if self.v_from:
            root.append(E.From(self.v_from.xml()))
        if self.v_to:
            root.append(E.To(self.v_to.xml()))
        if self.actor_settings:
            root.append(E.ActorSettings(self.actor_settings.xml()))
        return root


class VolumeActorSettings(object):
    def __init__(self, faraway_plane_offset, is_point_of_interest, dot_dialogue, water_locked, code_pattern,
                 is_blackhole, needs_trigger, is_secret_passage):
        self.faraway_plane_offset = faraway_plane_offset
        self.is_point_of_interest = is_point_of_interest
        self.dot_dialogue = dot_dialogue
        self.water_locked = water_locked
        self.code_pattern = code_pattern
        self.is_blackhole = is_blackhole
        self.needs_trigger = needs_trigger
        self.is_secret_passage = is_secret_passage

    def __str__(self):
        return "VolumeActorSettings"

    def xml(self):
        root = E.VolumeActorSettings(isPointOfInterest=str(self.is_point_of_interest),
                                     waterLocked=str(self.water_locked), isBlackhole=str(self.is_blackhole),
                                     needsTrigger=str(self.needs_trigger), isSecretPassage=str(self.is_secret_passage))
        root.append(E.FarawayPlaneOffset(self.faraway_plane_offset.xml()))
        if self.dot_dialogue:
            root.append(self.dot_dialogue.xml('DotDialogue'))
        if self.code_pattern:
            root.append(self.code_pattern.xml('CodePattern'))
        return root


class DotDialogueLine(object):
    def __init__(self, resource_text, grouped):
        self.resource_text = resource_text
        self.grouped = grouped

    def __str__(self):
        return "DotDialogueLine '%s'" % self.resource_text

    def xml(self):
        root = E.Line(grouped=str(self.grouped))
        if self.resource_text:
            root.text = self.resource_text
        return root


class Script(object):
    def __init__(self, name, timeout, triggers, conditions, actions, one_time, triggerless, ignore_end_triggers,
                 level_wide_one_time, disabled, is_win_condition):
        self.name = name
        self.timeout = timeout
        self.triggers = triggers
        self.conditions = conditions
        self.actions = actions
        self.one_time = one_time
        self.triggerless = triggerless
        self.ignore_end_triggers = ignore_end_triggers
        self.level_wide_one_time = level_wide_one_time
        self.disabled = disabled
        self.is_win_condition = is_win_condition

    def __str__(self):
        return "Script '%s'" % self.name

    def xml(self):
        root = E.Script(name=self.name, oneTime=str(self.one_time), triggerless=str(self.triggerless),
                        ignoreEndTriggers=str(self.ignore_end_triggers), levelWideOneTime=str(self.level_wide_one_time),
                        disabled=str(self.disabled), isWinCondition=str(self.is_win_condition))
        if self.timeout is not None:
            root.set('timeout', str(self.timeout))
        if self.triggers:
            root.append(self.triggers.xml('Triggers'))
        if self.conditions:
            root.append(self.conditions.xml('Conditions'))
        if self.actions:
            root.append(self.actions.xml('Actions'))
        return root


class ScriptTrigger(object):
    def __init__(self, entity, event):
        self.entity = entity
        self.event = event

    def __str__(self):
        return "ScriptTrigger"

    def xml(self):
        root = E.ScriptTrigger(event=self.event)
        if self.entity:
            root.append(self.entity.xml())
        return root


class Entity(object):
    def __init__(self, entity_type, identifier):
        self.entity_type = entity_type
        self.identifier = identifier

    def __str__(self):
        return "Entity i:%d" % self.identifier

    def xml(self):
        root = E.Entity(entityType=self.entity_type)
        if self.identifier is not None:
            root.set('identifier', str(self.identifier))
        return root


class ScriptAction(object):
    def __init__(self, entity, operation, arguments, killswitch, blocking):
        self.entity = entity
        self.operation = operation
        self.arguments = arguments
        self.killswitch = killswitch
        self.blocking = blocking

    def __str__(self):
        return "ScriptAction a:%s" % self.operation

    def xml(self):
        root = E.ScriptAction(operation=self.operation, killswitch=str(self.killswitch), blocking=str(self.blocking))
        if self.entity:
            root.append(self.entity.xml())
        if self.arguments:
            root.append(self.arguments.xml('Arguments'))
        return root


class ScriptCondition(object):
    def __init__(self, entity, operator, property_, value):
        self.entity = entity
        self.operator = operator
        self.property_ = property_
        self.value = value

    def __str__(self):
        return "ScriptCondition o:%s" % self.operator

    def xml(self):
        root = E.ScriptCondition(operator=str(self.operator), property=self.property_, value=self.value)
        if self.entity:
            root.append(self.entity.xml())
        return root

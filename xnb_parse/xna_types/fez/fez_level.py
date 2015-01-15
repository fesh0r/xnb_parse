"""
FEZ level types
"""

from __future__ import print_function

from collections import namedtuple

from xnb_parse.file_formats.xml_utils import ET


class MapTree(object):
    def __init__(self, map_node):
        self.map_node = map_node

    def __str__(self):
        return "MapTree {}".format(self.map_node)

    def xml(self, parent=None):
        if parent is None:
            root = ET.Element('MapTree')
        else:
            root = ET.SubElement(parent, 'MapTree')
        if self.map_node is not None:
            self.map_node.xml(root)
        return root


class MapNode(object):
    def __init__(self, level_name, connections, node_type, conditions, has_lesser_gate, has_warp_gate):
        self.level_name = level_name
        self.connections = connections
        self.node_type = node_type
        self.conditions = conditions
        self.has_lesser_gate = has_lesser_gate
        self.has_warp_gate = has_warp_gate

    def __str__(self):
        return "MapNode '{}' t:{} c:{}".format(self.level_name, self.node_type, len(self.connections))

    def xml(self, parent):
        root = ET.SubElement(parent, 'Node')
        root.set('name', self.level_name)
        root.set('hasLesserGate', str(self.has_lesser_gate))
        root.set('hasWarpGate', str(self.has_warp_gate))
        if self.node_type is not None:
            root.set('type', str(self.node_type))
        if self.conditions is not None:
            self.conditions.xml(root)
        if self.connections is not None:
            self.connections.xml(root, 'Connections')
        return root


class MapNodeConnection(object):
    def __init__(self, face, node, branch_oversize):
        self.face = face
        self.node = node
        self.branch_oversize = branch_oversize

    def __str__(self):
        return "MapNodeConnection f:{}".format(self.face)

    def xml(self, parent):
        root = ET.SubElement(parent, 'Connection')
        root.set('branchOversize', str(self.branch_oversize))
        if self.face is not None:
            root.set('face', str(self.face))
        if self.node is not None:
            self.node.xml(root)
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

    def xml(self, parent):
        root = ET.SubElement(parent, 'WinConditions')
        root.set('chests', str(self.chest_count))
        root.set('lockedDoors', str(self.locked_door_count))
        root.set('unlockedDoors', str(self.unlocked_door_count))
        root.set('cubeShards', str(self.cube_shard_count))
        root.set('splitUp', str(self.split_up_count))
        root.set('secrets', str(self.secret_count))
        root.set('others', str(self.other_collectible_count))
        if self.script_ids is not None:
            self.script_ids.xml(root, 'Scripts', 'Script')
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
        return "Sky '{}' b:'{}' l:{}".format(self.name, self.background, len(self.layers))

    def xml(self, parent=None):
        if parent is None:
            root = ET.Element('Sky')
        else:
            root = ET.SubElement(parent, 'Sky')
        root.set('name', self.name)
        root.set('background', self.background)
        root.set('windSpeed', str(self.wind_speed))
        root.set('density', str(self.density))
        root.set('fogDensity', str(self.fog_density))
        root.set('verticalTiling', str(self.vertical_tiling))
        root.set('horizontalScrolling', str(self.horizontal_scrolling))
        root.set('layerBaseHeight', str(self.layer_base_height))
        root.set('interLayerVerticalDistance', str(self.inter_layer_vertical_distance))
        root.set('interLayerHorizontalDistance', str(self.inter_layer_horizontal_distance))
        root.set('horizontalDistance', str(self.horizontal_distance))
        root.set('verticalDistance', str(self.vertical_distance))
        root.set('layerBaseSpacing', str(self.layer_base_spacing))
        root.set('windParallax', str(self.wind_parallax))
        root.set('windDistance', str(self.wind_distance))
        root.set('cloudsParallax', str(self.clouds_parallax))
        root.set('shadowOpacity', str(self.shadow_opacity))
        root.set('foliageShadows', str(self.foliage_shadows))
        root.set('noPerFaceLayerXOffset', str(self.no_per_face_layer_x_offset))
        root.set('layerBaseXOffset', str(self.layer_base_x_offset))
        if self.shadows is not None:
            root.set('shadows', self.shadows)
        if self.stars is not None:
            root.set('stars', self.stars)
        if self.cloud_tint is not None:
            root.set('cloudTint', self.cloud_tint)
        if self.layers is not None:
            self.layers.xml(root, 'Layers')
        if self.clouds is not None:
            self.clouds.xml(root, 'Clouds', 'Cloud')
        return root


class SkyLayer(object):
    def __init__(self, name, in_front, opacity, fog_tint):
        self.name = name
        self.in_front = in_front
        self.opacity = opacity
        self.fog_tint = fog_tint

    def __str__(self):
        return "SkyLayer '{}' o:{}".format(self.name, self.opacity)

    def xml(self, parent):
        root = ET.SubElement(parent, 'SkyLayer')
        root.set('name', self.name)
        root.set('opacity', str(self.opacity))
        root.set('fogTint', str(self.fog_tint))
        root.set('inFront', str(self.in_front))
        return root


class TrileSet(object):
    def __init__(self, name, triles, texture_atlas):
        self.name = name
        self.triles = triles
        self.texture_atlas = texture_atlas

    def __str__(self):
        return "TrileSet '{}' c:{}".format(self.name, len(self.triles))

    def xml(self, parent=None):
        if parent is None:
            root = ET.Element('TrileSet')
        else:
            root = ET.SubElement(parent, 'TrileSet')
        root.set('name', self.name)
        if self.triles is not None:
            self.triles.xml(root, 'Triles', 'TrileEntry')
        return root

    def export(self, filename):
        if self.texture_atlas is not None:
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
        return "Trile '{}' c:'{}' s:{}".format(self.name, self.cubemap_path, self.size)

    def xml(self, parent):
        if parent is None:
            root = ET.Element('Trile')
        else:
            root = ET.SubElement(parent, 'Trile')
        root.set('name', self.name)
        root.set('cubemapPath', self.cubemap_path)
        root.set('immaterial', str(self.immaterial))
        root.set('seeThrough', str(self.see_through))
        root.set('thin', str(self.thin))
        root.set('forceHugging', str(self.force_hugging))
        if self.surface_type is not None:
            root.set('surfaceType', str(self.surface_type))
        if self.actor_settings_type is not None or self.actor_settings_face is not None:
            actor_settings_tag = ET.SubElement(root, 'ActorSettings')
            if self.actor_settings_type is not None:
                actor_settings_tag.set('type', str(self.actor_settings_type))
            if self.actor_settings_face is not None:
                actor_settings_tag.set('face', str(self.actor_settings_face))
        self.size.xml(ET.SubElement(root, 'Size'))
        self.offset.xml(ET.SubElement(root, 'Offset'))
        self.atlas_offset.xml(ET.SubElement(root, 'AtlasOffset'))
        if self.faces is not None:
            self.faces.xml(root, 'Faces', 'Face')
        if self.geometry is not None:
            self.geometry.xml(ET.SubElement(root, 'Geometry'))
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
        return "Level '{}'".format(self.name)

    def xml(self, parent=None):
        if parent is None:
            root = ET.Element('Level')
        else:
            root = ET.SubElement(parent, 'Level')
        root.set('flat', str(self.flat))
        root.set('skipPostprocess', str(self.skip_postprocess))
        root.set('baseDiffuse', str(self.base_diffuse))
        root.set('baseAmbient', str(self.base_ambient))
        root.set('haloFiltering', str(self.halo_filtering))
        root.set('blinkingAlpha', str(self.blinking_alpha))
        root.set('loops', str(self.loops))
        root.set('waterHeight', str(self.water_height))
        root.set('skyName', self.sky_name)
        root.set('fapFadeoutStart', str(self.fap_fadeout_start))
        root.set('fapFadeoutLength', str(self.fap_fadeout_length))
        root.set('descending', str(self.descending))
        root.set('rainy', str(self.rainy))
        root.set('lowPass', str(self.low_pass))
        root.set('quantum', str(self.quantum))
        if self.name is not None:
            root.set('name', self.name)
        size_tag = ET.SubElement(root, 'Size')
        self.size.xml(size_tag)
        if self.starting_position is not None:
            starting_position_tag = ET.SubElement(root, 'StartingPosition')
            self.starting_position.xml(starting_position_tag)
        if self.sequence_samples_path is not None:
            root.set('sequenceSamplesPath', self.sequence_samples_path)
        if self.gomez_halo_name is not None:
            root.set('gomezHaloName', self.gomez_halo_name)
        if self.water_type is not None:
            root.set('waterType', str(self.water_type))
        if self.trile_set_name is not None:
            root.set('trileSetName', self.trile_set_name)
        if self.volumes is not None:
            self.volumes.xml(root, 'Volumes')
        if self.scripts is not None:
            self.scripts.xml(root, 'Scripts')
        if self.song_name is not None:
            root.set('songName', self.song_name)
        if self.triles is not None:
            self.triles.xml(root, 'Triles')
        if self.art_objects is not None:
            self.art_objects.xml(root, 'ArtObjects')
        if self.background_planes is not None:
            self.background_planes.xml(root, 'BackgroundPlanes')
        if self.groups is not None:
            self.groups.xml(root, 'Groups')
        if self.nonplayer_characters is not None:
            self.nonplayer_characters.xml(root, 'NonplayerCharacters')
        if self.paths is not None:
            self.paths.xml(root, 'Paths')
        if self.muted_loops is not None:
            self.muted_loops.xml(root, 'MutedLoops')
        if self.ambience_tracks is not None:
            self.ambience_tracks.xml(root, 'AmbienceTracks')
        if self.node_type is not None:
            root.set('nodeType', str(self.node_type))
        return root


class Volume(object):
    def __init__(self, orientations, v_from, v_to, actor_settings):
        self.orientations = orientations
        self.v_from = v_from
        self.v_to = v_to
        self.actor_settings = actor_settings

    def __str__(self):
        return "Volume"

    def xml(self, parent):
        root = ET.SubElement(parent, 'Volume')
        if self.orientations is not None:
            self.orientations.xml(root, 'Orientations')
        from_tag = ET.SubElement(root, 'From')
        self.v_from.xml(from_tag)
        to_tag = ET.SubElement(root, 'To')
        self.v_to.xml(to_tag)
        if self.actor_settings is not None:
            actor_settings_tag = ET.SubElement(root, 'ActorSettings')
            self.actor_settings.xml(actor_settings_tag)
        return root


_TrileEmplacement = namedtuple('TrileEmplacement', ['x', 'y', 'z'])


class TrileEmplacement(_TrileEmplacement):
    __slots__ = ()

    def xml(self, parent):
        root = ET.SubElement(parent, 'TrileEmplacement')
        root.set('x', str(self.x))
        root.set('y', str(self.y))
        root.set('z', str(self.z))
        return root


class TrileInstance(object):
    __slots__ = ('position', 'trile_id', 'orientation', 'actor_settings', 'overlapped_triles')

    def __init__(self, position, trile_id, orientation, actor_settings, overlapped_triles):
        self.position = position
        self.trile_id = trile_id
        self.orientation = orientation
        self.actor_settings = actor_settings
        self.overlapped_triles = overlapped_triles

    def __str__(self):
        return "TrileInstance t:{} p:{},{},{}".format(self.trile_id, self.position.x, self.position.y, self.position.z)

    def xml(self, parent):
        root = ET.SubElement(parent, 'TrileInstance')
        root.set('trileId', str(self.trile_id))
        root.set('orientation', str(self.orientation))
        position_tag = ET.SubElement(root, 'Position')
        self.position.xml(position_tag)
        if self.actor_settings is not None:
            self.actor_settings.xml(root)
        if self.overlapped_triles is not None:
            self.overlapped_triles.xml(root, 'OverlappedTriles')
        return root


class ArtObjectInstance(object):
    def __init__(self, name, position, rotation, scale, actor_settings):
        self.name = name
        self.position = position
        self.rotation = rotation
        self.scale = scale
        self.actor_settings = actor_settings

    def __str__(self):
        return "ArtObjectInstance '{}'".format(self.name)

    def xml(self, parent):
        root = ET.SubElement(parent, 'ArtObjectInstance')
        root.set('name', self.name)
        position_tag = ET.SubElement(root, 'Position')
        self.position.xml(position_tag)
        rotation_tag = ET.SubElement(root, 'Rotation')
        self.rotation.xml(rotation_tag)
        scale_tag = ET.SubElement(root, 'Scale')
        self.scale.xml(scale_tag)
        if self.actor_settings is not None:
            self.actor_settings.xml(root)
        return root


class BackgroundPlane(object):
    __slots__ = ('position', 'rotation', 'scale', 'size', 'texture_name', 'light_map', 'allow_overbrightness',
                 'filter_', 'animated', 'doublesided', 'opacity', 'attached_group', 'billboard', 'sync_with_samples',
                 'crosshatch', 'unknown', 'always_on_top', 'fullbright', 'pixelated_lightmap', 'x_texture_repeat',
                 'y_texture_repeat', 'clamp_texture', 'actor_type', 'attached_plane', 'parallax_factor')

    def __init__(self, position, rotation, scale, size, texture_name, light_map, allow_overbrightness, filter_,
                 animated, doublesided, opacity, attached_group, billboard, sync_with_samples, crosshatch, unknown,
                 always_on_top, fullbright, pixelated_lightmap, x_texture_repeat, y_texture_repeat, clamp_texture,
                 actor_type, attached_plane, parallax_factor):
        self.position = position
        self.rotation = rotation
        self.scale = scale
        self.size = size
        self.texture_name = texture_name
        self.light_map = light_map
        self.allow_overbrightness = allow_overbrightness
        self.filter_ = filter_
        self.animated = animated
        self.doublesided = doublesided
        self.opacity = opacity
        self.attached_group = attached_group
        self.billboard = billboard
        self.sync_with_samples = sync_with_samples
        self.crosshatch = crosshatch
        self.unknown = unknown
        self.always_on_top = always_on_top
        self.fullbright = fullbright
        self.pixelated_lightmap = pixelated_lightmap
        self.x_texture_repeat = x_texture_repeat
        self.y_texture_repeat = y_texture_repeat
        self.clamp_texture = clamp_texture
        self.actor_type = actor_type
        self.attached_plane = attached_plane
        self.parallax_factor = parallax_factor

    def __str__(self):
        return "BackgroundPlane t:'{}'".format(self.texture_name)

    def xml(self, parent):
        root = ET.SubElement(parent, 'BackgroundPlane')
        root.set('textureName', self.texture_name)
        root.set('lightMap', str(self.light_map))
        root.set('allowOverbrightness', str(self.allow_overbrightness))
        root.set('animated', str(self.animated))
        root.set('doubleSided', str(self.doublesided))
        root.set('opacity', str(self.opacity))
        root.set('billboard', str(self.billboard))
        root.set('syncWithSamples', str(self.sync_with_samples))
        root.set('crosshatch', str(self.crosshatch))
        root.set('unknown', str(self.unknown))
        root.set('alwaysOnTop', str(self.always_on_top))
        root.set('fullbright', str(self.fullbright))
        root.set('pixelatedLightmap', str(self.pixelated_lightmap))
        root.set('xTextureRepeat', str(self.x_texture_repeat))
        root.set('yTextureRepeat', str(self.y_texture_repeat))
        root.set('clampTexture', str(self.clamp_texture))
        root.set('parallaxFactor', str(self.parallax_factor))
        self.position.xml(ET.SubElement(root, 'Position'))
        self.rotation.xml(ET.SubElement(root, 'Rotation'))
        self.scale.xml(ET.SubElement(root, 'Scale'))
        root.set('filter', self.filter_.attrib())
        if self.attached_group is not None:
            root.set('attachedGroup', str(self.attached_group))
        if self.actor_type is not None:
            root.set('actorType', str(self.actor_type))
        if self.attached_plane is not None:
            root.set('attachedPlane', str(self.attached_plane))
        return root


class TrileGroup(object):
    def __init__(self, triles, path, heavy, actor_type, geyser_offset, geyser_pause_for, geyser_lift_for,
                 geyser_apex_height, spin_center, spin_clockwise, spin_frequency, spin_needs_triggering,
                 spin_180_degrees, fall_on_rotate, spin_offset, associated_sound):
        self.triles = triles
        self.path = path
        self.heavy = heavy
        self.actor_type = actor_type
        self.geyser_offset = geyser_offset
        self.geyser_pause_for = geyser_pause_for
        self.geyser_lift_for = geyser_lift_for
        self.geyser_apex_height = geyser_apex_height
        self.spin_center = spin_center
        self.spin_clockwise = spin_clockwise
        self.spin_frequency = spin_frequency
        self.spin_needs_triggering = spin_needs_triggering
        self.spin_180_degrees = spin_180_degrees
        self.fall_on_rotate = fall_on_rotate
        self.spin_offset = spin_offset
        self.associated_sound = associated_sound

    def __str__(self):
        return "TrileGroup"

    def xml(self, parent):
        root = ET.SubElement(parent, 'TrileGroup')
        root.set('heavy', str(self.heavy))
        root.set('geyserOffset', str(self.geyser_offset))
        root.set('geyserPauseFor', str(self.geyser_pause_for))
        root.set('geyserLiftFor', str(self.geyser_lift_for))
        root.set('geyserApexHeight', str(self.geyser_apex_height))
        root.set('spinClockwise', str(self.spin_clockwise))
        root.set('spinFrequency', str(self.spin_frequency))
        root.set('spinNeedsTriggering', str(self.spin_needs_triggering))
        root.set('spin180Degrees', str(self.spin_180_degrees))
        root.set('fallOnRotate', str(self.fall_on_rotate))
        root.set('spinOffset', str(self.spin_offset))
        if self.triles is not None:
            self.triles.xml(root, 'Triles')
        if self.path is not None:
            self.path.xml(root)
        if self.actor_type is not None:
            root.set('actorType', str(self.actor_type))
        if self.spin_center is not None:
            self.spin_center.xml(ET.SubElement(root, 'SpinCenter'))
        if self.associated_sound is not None:
            root.set('associatedSound', self.associated_sound)
        return root


class TrileFace(object):
    def __init__(self, trile_id, face):
        self.trile_id = trile_id
        self.face = face

    def __str__(self):
        return "TrileFace f:{} t:{},{},{}".format(self.face, self.trile_id.x, self.trile_id.y, self.trile_id.z)

    def xml(self, parent):
        root = ET.SubElement(parent, 'TrileFace')
        if self.face is not None:
            root.set('face', str(self.face))
        if self.trile_id is not None:
            self.trile_id.xml(ET.SubElement(root, 'TrileId'))
        return root


class NpcInstance(object):
    def __init__(self, name, position, destination_offset, walk_speed, randomize_speech, say_first_speech_line_once,
                 avoids_gomez, actor_type, speech, actions):
        self.name = name
        self.position = position
        self.destination_offset = destination_offset
        self.walk_speed = walk_speed
        self.randomize_speech = randomize_speech
        self.say_first_speech_line_once = say_first_speech_line_once
        self.avoids_gomez = avoids_gomez
        self.actor_type = actor_type
        self.speech = speech
        self.actions = actions

    def __str__(self):
        return "NpcInstance '{}'".format(self.name)

    def xml(self, parent):
        root = ET.SubElement(parent, 'NpcInstance')
        root.set('name', self.name)
        root.set('walkSpeed', str(self.walk_speed))
        root.set('randomizeSpeech', str(self.randomize_speech))
        root.set('sayFirstSpeechLineOnce', str(self.say_first_speech_line_once))
        root.set('avoidsGomez', str(self.avoids_gomez))
        if self.position is not None:
            self.position.xml(ET.SubElement(root, 'Position'))
        if self.destination_offset is not None:
            self.destination_offset.xml(ET.SubElement(root, 'DestinationOffset'))
        if self.actor_type is not None:
            root.set('actorType', str(self.actor_type))
        if self.speech is not None:
            self.speech.xml(root, 'Speech')
        if self.actions is not None:
            self.actions.xml(root, 'Actions', 'Action')
        return root


class MovementPath(object):
    def __init__(self, segments, needs_trigger, end_behavior, sound_name, is_spline, offset_seconds, save_trigger):
        self.segments = segments
        self.needs_trigger = needs_trigger
        self.end_behavior = end_behavior
        self.sound_name = sound_name
        self.is_spline = is_spline
        self.offset_seconds = offset_seconds
        self.save_trigger = save_trigger

    def __str__(self):
        return "MovementPath"

    def xml(self, parent):
        root = ET.SubElement(parent, 'MovementPath')
        root.set('needsTrigger', str(self.needs_trigger))
        root.set('isSpline', str(self.is_spline))
        root.set('offsetSeconds', str(self.offset_seconds))
        root.set('saveTrigger', str(self.save_trigger))
        if self.segments is not None:
            self.segments.xml(root, 'Segments')
        if self.end_behavior is not None:
            root.set('endBehavior', str(self.end_behavior))
        if self.sound_name is not None:
            root.set('soundName', str(self.sound_name))
        return root


class AmbienceTrack(object):
    def __init__(self, name, dawn, day, dusk, night):
        self.name = name
        self.dawn = dawn
        self.day = day
        self.dusk = dusk
        self.night = night

    def __str__(self):
        return "AmbienceTrack '{}'".format(self.name)

    def xml(self, parent):
        root = ET.SubElement(parent, 'AmbienceTrack')
        root.set('dawn', str(self.dawn))
        root.set('day', str(self.day))
        root.set('dusk', str(self.dusk))
        root.set('night', str(self.night))
        if self.name is not None:
            root.set('name', self.name)
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

    def xml(self, parent):
        root = ET.SubElement(parent, 'VolumeActorSettings')
        root.set('isPointOfInterest', str(self.is_point_of_interest))
        root.set('waterLocked', str(self.water_locked))
        root.set('isBlackhole', str(self.is_blackhole))
        root.set('needsTrigger', str(self.needs_trigger))
        root.set('isSecretPassage', str(self.is_secret_passage))
        self.faraway_plane_offset.xml(ET.SubElement(root, 'FarawayPlaneOffset'))
        if self.dot_dialogue is not None:
            self.dot_dialogue.xml(root, 'DotDialogue')
        if self.code_pattern is not None:
            self.code_pattern.xml(root, 'CodePattern')
        return root


class DotDialogueLine(object):
    def __init__(self, resource_text, grouped):
        self.resource_text = resource_text
        self.grouped = grouped

    def __str__(self):
        return "DotDialogueLine '{}'".format(self.resource_text)

    def xml(self, parent):
        root = ET.SubElement(parent, 'Line')
        root.set('grouped', str(self.grouped))
        if self.resource_text is not None:
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
        return "Script '{}'".format(self.name)

    def xml(self, parent):
        root = ET.SubElement(parent, 'Script')
        root.set('name', self.name)
        root.set('oneTime', str(self.one_time))
        root.set('triggerless', str(self.triggerless))
        root.set('ignoreEndTriggers', str(self.ignore_end_triggers))
        root.set('levelWideOneTime', str(self.level_wide_one_time))
        root.set('disabled', str(self.disabled))
        root.set('isWinCondition', str(self.is_win_condition))
        if self.timeout is not None:
            root.set('timeout', str(self.timeout))
        if self.triggers is not None:
            self.triggers.xml(root, 'Triggers')
        if self.conditions is not None:
            self.conditions.xml(root, 'Conditions')
        if self.actions is not None:
            self.actions.xml(root, 'Actions')
        return root


class ScriptTrigger(object):
    def __init__(self, entity, event):
        self.entity = entity
        self.event = event

    def __str__(self):
        return "ScriptTrigger"

    def xml(self, parent):
        root = ET.SubElement(parent, 'ScriptTrigger')
        root.set('event', self.event)
        if self.entity is not None:
            self.entity.xml(root)
        return root


class ScriptAction(object):
    def __init__(self, entity, operation, arguments, killswitch, blocking):
        self.entity = entity
        self.operation = operation
        self.arguments = arguments
        self.killswitch = killswitch
        self.blocking = blocking

    def __str__(self):
        return "ScriptAction a:{}".format(self.operation)

    def xml(self, parent):
        root = ET.SubElement(parent, 'ScriptAction')
        root.set('operation', self.operation)
        root.set('killswitch', str(self.killswitch))
        root.set('blocking', str(self.blocking))
        if self.entity is not None:
            self.entity.xml(root)
        if self.arguments is not None:
            self.arguments.xml(root, 'Arguments')
        return root


class ScriptCondition(object):
    def __init__(self, entity, operator, property_, value):
        self.entity = entity
        self.operator = operator
        self.property_ = property_
        self.value = value

    def __str__(self):
        return "ScriptCondition o:{}".format(self.operator)

    def xml(self, parent):
        root = ET.SubElement(parent, 'ScriptCondition')
        root.set('property', self.property_)
        root.set('value', self.value)
        if self.operator is not None:
            root.set('operator', str(self.operator))
        if self.entity is not None:
            self.entity.xml(root)
        return root


class Entity(object):
    def __init__(self, entity_type, identifier):
        self.entity_type = entity_type
        self.identifier = identifier

    def __str__(self):
        return "Entity i:{}".format(self.identifier)

    def xml(self, parent):
        root = ET.SubElement(parent, 'Entity')
        root.set('entityType', self.entity_type)
        if self.identifier is not None:
            root.set('identifier', str(self.identifier))
        return root


class InstanceActorSettings(object):
    def __init__(self, contained_trile, sign_text, sequence, sequence_sample_name, sequence_alternate_sample_name,
                 host_volume):
        self.contained_trile = contained_trile
        self.sign_text = sign_text
        self.sequence = sequence
        self.sequence_sample_name = sequence_sample_name
        self.sequence_alternate_sample_name = sequence_alternate_sample_name
        self.host_volume = host_volume

    def __str__(self):
        return "InstanceActorSettings"

    def xml(self, parent):
        root = ET.SubElement(parent, 'InstanceActorSettings')
        if self.contained_trile is not None:
            root.set('containedTrile', str(self.contained_trile))
        if self.sign_text is not None:
            root.set('signText', self.sign_text)
        if self.sequence is not None:
            self.sequence.xml(root, 'Sequence')
        if self.sequence_sample_name is not None:
            root.set('sequenceSampleName', self.sequence_sample_name)
        if self.sequence_alternate_sample_name is not None:
            root.set('sequenceAlternateSampleName', self.sequence_alternate_sample_name)
        if self.host_volume is not None:
            root.set('hostVolume', str(self.host_volume))
        return root


class ArtObjectActorSettings(object):
    __slots__ = ('inactive', 'contained_trile', 'attached_group', 'spin_view', 'spin_every', 'spin_offset',
                 'off_center', 'rotation_center', 'vibration_pattern', 'code_pattern', 'segment', 'next_node',
                 'destination_level', 'treasure_map_name', 'invisible_sides', 'timeswitch_wind_back_speed')

    def __init__(self, inactive, contained_trile, attached_group, spin_view, spin_every, spin_offset, off_center,
                 rotation_center, vibration_pattern, code_pattern, segment, next_node, destination_level,
                 treasure_map_name, invisible_sides, timeswitch_wind_back_speed):
        self.inactive = inactive
        self.contained_trile = contained_trile
        self.attached_group = attached_group
        self.spin_view = spin_view
        self.spin_every = spin_every
        self.spin_offset = spin_offset
        self.off_center = off_center
        self.rotation_center = rotation_center
        self.vibration_pattern = vibration_pattern
        self.code_pattern = code_pattern
        self.segment = segment
        self.next_node = next_node
        self.destination_level = destination_level
        self.treasure_map_name = treasure_map_name
        self.invisible_sides = invisible_sides
        self.timeswitch_wind_back_speed = timeswitch_wind_back_speed

    def __str__(self):
        return "ActObjectActorSettings"

    def xml(self, parent):
        root = ET.SubElement(parent, 'ArtObjectActorSettings')
        root.set('inactive', str(self.inactive))
        root.set('spinEvery', str(self.spin_every))
        root.set('spinOffset', str(self.spin_offset))
        root.set('offCenter', str(self.off_center))
        root.set('timeswitchWindBackSpeed', str(self.timeswitch_wind_back_speed))
        if self.contained_trile is not None:
            root.set('containedTrile', str(self.contained_trile))
        if self.attached_group is not None:
            root.set('attachedGroup', str(self.attached_group))
        if self.spin_view is not None:
            root.set('spinView', str(self.spin_view))
        if self.rotation_center is not None:
            self.rotation_center.xml(ET.SubElement(root, 'RotationCenter'))
        if self.vibration_pattern is not None:
            self.vibration_pattern.xml(root, 'VibrationPattern')
        if self.code_pattern is not None:
            self.code_pattern.xml(root, 'CodePattern')
        if self.segment is not None:
            self.segment.xml(ET.SubElement(root, 'Segment'))
        if self.next_node is not None:
            root.set('nextNode', str(self.next_node))
        if self.destination_level is not None:
            root.set('destinationLevel', str(self.destination_level))
        if self.treasure_map_name is not None:
            root.set('treasureMapName', str(self.treasure_map_name))
        return root


class PathSegment(object):
    def __init__(self, destination, duration, wait_time_on_start, wait_time_on_finish, acceleration, deceleration,
                 jitter_factor, orientation, custom_data):
        self.destination = destination
        self.duration = duration
        self.wait_time_on_start = wait_time_on_start
        self.wait_time_on_finish = wait_time_on_finish
        self.acceleration = acceleration
        self.deceleration = deceleration
        self.jitter_factor = jitter_factor
        self.orientation = orientation
        self.custom_data = custom_data

    def __str__(self):
        return "PathSegment"

    def xml(self, parent):
        root = ET.SubElement(parent, 'PathSegment')
        root.set('acceleration', str(self.acceleration))
        root.set('deceleration', str(self.deceleration))
        root.set('jitterFactor', str(self.jitter_factor))
        self.destination.xml(ET.SubElement(root, 'Destination'))
        if self.duration is not None:
            root.set('duration', str(self.duration))
        if self.wait_time_on_start is not None:
            root.set('waitTimeOnStart', str(self.wait_time_on_start))
        if self.wait_time_on_finish is not None:
            root.set('waitTimeOnFinish', str(self.wait_time_on_finish))
        self.orientation.xml(ET.SubElement(root, 'Orientation'))
        if self.custom_data is not None:
            self.custom_data.xml(ET.SubElement(root, 'CustomData'))
        return root


class SpeechLine(object):
    def __init__(self, text, override_content):
        self.text = text
        self.override_content = override_content

    def __str__(self):
        return "SpeechLine '{}'".format(self.text)

    def xml(self, parent):
        root = ET.SubElement(parent, 'SpeechLine')
        if self.text is not None:
            root.set('text', self.text)
        if self.override_content is not None:
            self.override_content.xml(ET.SubElement(root, 'OverrideContent'))
        return root


class NpcActionContent(object):
    def __init__(self, animation_name, sound_name):
        self.animation_name = animation_name
        self.sound_name = sound_name

    def __str__(self):
        return "NpcActionContent"

    def xml(self, parent):
        root = ET.SubElement(parent, 'NpcActionContent')
        if self.animation_name is not None:
            root.set('animationName', self.animation_name)
        if self.sound_name is not None:
            root.set('soundName', self.sound_name)
        return root


class CameraNodeData(object):
    def __init__(self, perspective, pixels_per_trixel, sound_name):
        self.perspective = perspective
        self.pixels_per_trixel = pixels_per_trixel
        self.sound_name = sound_name

    def __str__(self):
        return "CameraNodeData"

    def xml(self, parent):
        root = ET.SubElement(parent, 'CameraNodeData')
        root.set('perspective', str(self.perspective))
        root.set('pixelsPerTrixel', str(self.pixels_per_trixel))
        if self.sound_name is not None:
            root.set('soundName', str(self.sound_name))
        return root

"""
FEZ graphics types
"""

from __future__ import print_function

from xnb_parse.file_formats.xml_utils import ET
from xnb_parse.xna_types.xna_graphics import (Texture2D, FORMAT_COLOR, get_surface_format, VERSION_31, VERSION_40,
                                              FORMAT4_COLOR)


class ArtObject(object):
    def __init__(self, name, cubemap_path, size, geometry, actor_type, no_silhouette, laser_outlets):
        self.name = name
        self.cubemap_path = cubemap_path
        self.size = size
        self.geometry = geometry
        self.actor_type = actor_type
        self.no_silhouette = no_silhouette
        self.laser_outlets = laser_outlets

    def __str__(self):
        return "ArtObject '{}' t:'{}' s:{} g:{}".format(self.name, self.cubemap_path, self.size,
                                                        len(self.geometry.vertices))

    def xml(self, parent=None):
        if parent is None:
            root = ET.Element('ArtObject')
        else:
            root = ET.SubElement(parent, 'ArtObject')
        root.set('name', self.name)
        root.set('cubemapPath', self.cubemap_path)
        root.set('noSilhouette', str(self.no_silhouette))
        self.size.xml(ET.SubElement(root, 'Size'))
        if self.actor_type is not None:
            root.set('actorType', str(self.actor_type))
        if self.geometry is not None:
            self.geometry.xml(root)
        if self.laser_outlets is not None:
            self.laser_outlets.xml(root, 'LaserOutlets')
        return root


class ArtObjectPC(object):
    def __init__(self, name, cubemap, size, geometry, actor_type, no_silhouette):
        self.name = name
        self.cubemap = cubemap
        self.size = size
        self.geometry = geometry
        self.actor_type = actor_type
        self.no_silhouette = no_silhouette

    def __str__(self):
        return "ArtObjectPC '{}' s:{} g:{}".format(self.name, self.size, len(self.geometry.vertices))

    def xml(self, parent=None):
        if parent is None:
            root = ET.Element('ArtObject')
        else:
            root = ET.SubElement(parent, 'ArtObject')
        root.set('name', self.name)
        root.set('noSilhouette', str(self.no_silhouette))
        self.size.xml(ET.SubElement(root, 'Size'))
        if self.actor_type is not None:
            root.set('actorType', str(self.actor_type))
        if self.geometry is not None:
            self.geometry.xml(root)
        return root

    def export(self, filename):
        self.cubemap.export(filename)


class ShaderInstancedIndexedPrimitives(object):
    __slots__ = ('primitive_type', 'vertices', 'indices')

    def __init__(self, primitive_type, vertices, indices):
        self.primitive_type = primitive_type
        self.vertices = vertices
        self.indices = indices

    def __str__(self):
        return "ShaderInstancedIndexedPrimitives t:{} v:{} i:{}".format(self.primitive_type, len(self.vertices),
                                                                        len(self.indices))

    def xml(self, parent):
        root = ET.SubElement(parent, 'ShaderInstancedIndexedPrimitives')
        if self.primitive_type is not None:
            root.set('type', str(self.primitive_type))
        if self.vertices is not None:
            self.vertices.xml(root, 'Vertices')
        if self.indices is not None:
            self.indices.xml(root, 'Indices', 'Index')
        return root


class VertexPositionNormalTextureInstance(object):
    __slots__ = ('position', 'normal', 'texture_coord')

    def __init__(self, position, normal, texture_coord):
        self.position = position
        self.normal = normal
        self.texture_coord = texture_coord

    def __str__(self):
        return "VertexPositionNormalTextureInstance p:{} n:{} c:{}".format(self.position, self.normal,
                                                                           self.texture_coord)

    def xml(self, parent):
        root = ET.SubElement(parent, 'VertexPositionNormalTextureInstance')
        self.position.xml(ET.SubElement(root, 'Position'))
        normal_tag = ET.SubElement(root, 'Normal')
        normal_tag.text = str(self.normal)
        self.texture_coord.xml(ET.SubElement(root, 'TextureCoord'))
        return root


class NpcMetadata(object):
    def __init__(self, walk_speed, avoids_gomez, sound_path, sound_actions):
        self.walk_speed = walk_speed
        self.avoids_gomez = avoids_gomez
        self.sound_path = sound_path
        self.sound_actions = sound_actions

    def __str__(self):
        return "NpcMetadata s:{} a:{}".format(self.sound_path, len(self.sound_actions))

    def xml(self, parent=None):
        if parent is None:
            root = ET.Element('NpcMetadata')
        else:
            root = ET.SubElement(parent, 'NpcMetadata')
        root.set('avoidsGomez', str(self.avoids_gomez))
        root.set('walkSpeed', str(self.walk_speed))
        if self.sound_path is not None:
            root.set('soundPath', self.sound_path)
        if self.sound_actions is not None:
            self.sound_actions.xml(root, 'SoundActions')
        return root


class AnimatedTexture(object):
    surface_format = get_surface_format(VERSION_31, FORMAT_COLOR)

    def __init__(self, width, height, actual_width, actual_height, frames):
        self.width = width
        self.height = height
        self.actual_width = actual_width
        self.actual_height = actual_height
        self.frames = frames

    def __str__(self):
        return "AnimatedTexture d:{}x{} a:{}x{} f:{}".format(self.width, self.height, self.actual_width,
                                                             self.actual_height, len(self.frames))

    def xml(self, parent=None):
        if parent is None:
            root = ET.Element('AnimatedTexture')
        else:
            root = ET.SubElement(parent, 'AnimatedTexture')
        root.set('width', str(self.width))
        root.set('height', str(self.height))
        root.set('actualWidth', str(self.actual_width))
        root.set('actualHeight', str(self.actual_height))
        if self.frames is not None:
            self.frames.xml(root, 'Frames')
        return root

    def export(self, filename):
        if self.frames is not None:
            self.export_single(filename)

    def export_each(self, filename):
        for i, cur_frame in enumerate(self.frames):
            texture = Texture2D(self.surface_format, self.width, self.height, [cur_frame.data])
            cur_filename = "{}_ani\\{}".format(filename, i)
            texture.export(cur_filename)

    def export_single(self, filename):
        texture_data = bytearray()
        for cur_frame in self.frames:
            texture_data.extend(cur_frame.data)
        texture = Texture2D(self.surface_format, self.width, self.height * len(self.frames), [texture_data])
        texture.export(filename + '.ani')


class AnimatedTexturePC(object):
    surface_format = get_surface_format(VERSION_40, FORMAT4_COLOR)

    def __init__(self, width, height, actual_width, actual_height, data, frames):
        self.width = width
        self.height = height
        self.actual_width = actual_width
        self.actual_height = actual_height
        self.data = data
        self.frames = frames

    def __str__(self):
        return "AnimatedTexturePC d:{}x{} a:{}x{} f:{}".format(self.width, self.height, self.actual_width,
                                                               self.actual_height, len(self.frames))

    def xml(self, parent=None):
        if parent is None:
            root = ET.Element('AnimatedTexturePC')
        else:
            root = ET.SubElement(parent, 'AnimatedTexturePC')
        root.set('width', str(self.width))
        root.set('height', str(self.height))
        root.set('actualWidth', str(self.actual_width))
        root.set('actualHeight', str(self.actual_height))
        if self.frames is not None:
            self.frames.xml(root, 'Frames')
        return root

    def export(self, filename):
        if self.data is not None:
            texture = Texture2D(self.surface_format, self.width, self.height, [self.data])
            texture.export(filename + '.ani')


class Frame(object):
    def __init__(self, duration, data):
        self.duration = duration
        self.data = data

    def __str__(self):
        return "Frame d:{} s:{}".format(self.duration, len(self.data))

    def xml(self, parent):
        root = ET.SubElement(parent, 'Frame')
        if self.duration is not None:
            root.set('duration', str(self.duration))
        return root


class FramePC(object):
    def __init__(self, duration, rectangle):
        self.duration = duration
        self.rectangle = rectangle

    def __str__(self):
        return "FramePC d:{} r:{}".format(self.duration, self.rectangle)

    def xml(self, parent):
        root = ET.SubElement(parent, 'FramePC')
        if self.duration is not None:
            root.set('duration', str(self.duration))
        if self.rectangle is not None:
            self.rectangle.xml(root)
        return root

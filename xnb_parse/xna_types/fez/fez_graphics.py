# coding=utf-8
"""
FEZ graphics types
"""

from __future__ import absolute_import, division, unicode_literals

from xnb_parse.binstream import BinaryWriter
from xnb_parse.xnb_reader import VERSION_31
from xnb_parse.file_formats.xml_utils import E
from xnb_parse.xna_types.xna_graphics import Texture2D, FORMAT_COLOR, get_surface_format


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
        return "ArtObject '%s' t:'%s' s:%s g:%d" % (self.name, self.cubemap_path, self.size,
                                                    len(self.geometry.vertices))

    def xml(self):
        root = E.ArtObject(name=self.name, cubemapPath=self.cubemap_path, noSilhouette=str(self.no_silhouette))
        root.append(E.Size(self.size.xml()))
        if self.actor_type is not None:
            root.set('actorType', str(self.actor_type))
        if self.geometry is not None:
            root.append(self.geometry.xml())
        if self.laser_outlets is not None:
            root.append(self.laser_outlets.xml('LaserOutlets'))
        return root


class ShaderInstancedIndexedPrimitives(object):
    __slots__ = ('primitive_type', 'vertices', 'indices')

    def __init__(self, primitive_type, vertices, indices):
        self.primitive_type = primitive_type
        self.vertices = vertices
        self.indices = indices

    def __str__(self):
        return "ShaderInstancedIndexedPrimitives t:%s v:%d i:%d" % (self.primitive_type, len(self.vertices),
                                                                    len(self.indices))

    def xml(self):
        root = E.ShaderInstancedIndexedPrimitives()
        if self.primitive_type is not None:
            root.set('type', str(self.primitive_type))
        if self.vertices is not None:
            root.append(self.vertices.xml('Vertices'))
        if self.indices is not None:
            root.append(self.indices.xml('Indices', 'Index'))
        return root


class VertexPositionNormalTextureInstance(object):
    __slots__ = ('position', 'normal', 'texture_coord')

    def __init__(self, position, normal, texture_coord):
        self.position = position
        self.normal = normal
        self.texture_coord = texture_coord

    def __str__(self):
        return "VertexPositionNormalTextureInstance p:%s n:%d c:%s" % (self.position, self.normal, self.texture_coord)

    def xml(self):
        root = E.VertexPositionNormalTextureInstance()
        root.append(E.Position(self.position.xml()))
        root.append(E.Normal(str(self.normal)))
        root.append(E.TextureCoord(self.texture_coord.xml()))
        return root


class NpcMetadata(object):
    def __init__(self, walk_speed, avoids_gomez, sound_path, sound_actions):
        self.walk_speed = walk_speed
        self.avoids_gomez = avoids_gomez
        self.sound_path = sound_path
        self.sound_actions = sound_actions

    def __str__(self):
        return "NpcMetadata s:%s a:%d" % (self.sound_path, len(self.sound_actions))

    def xml(self):
        root = E.NpcMetadata(avoidsGomez=str(self.avoids_gomez), walkSpeed=str(self.walk_speed))
        if self.sound_path is not None:
            root.set('soundPath', self.sound_path)
        if self.sound_actions is not None:
            root.append(self.sound_actions.xml('SoundActions'))
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
        return "AnimatedTexture d:%dx%d a:%dx%d f:%d" % (self.width, self.height, self.actual_width,
                                                         self.actual_height, len(self.frames))

    def xml(self):
        root = E.AnimatedTexture(width=str(self.width), height=str(self.height), actualWidth=str(self.actual_width),
                                 actualHeight=str(self.actual_height))
        if self.frames is not None:
            root.append(self.frames.xml('Frames'))
        return root

    def export(self, filename):
        if self.frames is not None:
            self.export_single(filename)

    def export_each(self, filename):
        for i, cur_frame in enumerate(self.frames):
            texture = Texture2D(self.surface_format, self.width, self.height, [cur_frame.data])
            cur_filename = "%s_ani\\%d" % (filename, i)
            texture.export(cur_filename)

    def export_single(self, filename):
        texture_data = bytearray()
        for cur_frame in self.frames:
            texture_data.extend(cur_frame.data)
        texture = Texture2D(self.surface_format, self.width, self.height * len(self.frames), [texture_data])
        texture.export(filename + '.ani')


class Frame(object):
    def __init__(self, duration, data):
        self.duration = duration
        raw_stream = BinaryWriter()
        for col in data:
            raw_stream.write_uint32(col.to_packed())
        self.data = raw_stream.serial()

    def __str__(self):
        return "Frame d:%d s:%d" % (self.duration, len(self.data))

    def xml(self):
        root = E.Frame()
        if self.duration is not None:
            root.set('duration', str(self.duration))
        return root

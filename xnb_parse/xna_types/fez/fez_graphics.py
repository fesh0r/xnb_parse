"""
FEZ graphics types
"""

from xnb_parse.binstream import BinaryWriter
from xnb_parse.xnb_reader import VERSION_31
from xnb_parse.file_formats.xml_utils import E
from xnb_parse.xna_types.xna_graphics import Texture2D, FORMAT_COLOR, get_surface_format


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
        root.append(self.frames.xml('Frames'))
        return root

    def export(self, filename):
        self.export_single(filename)
        return self.xml()

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
        return E.Frame(duration=str(self.duration))

"""
media types
"""

from __future__ import print_function

from xnb_parse.file_formats.wav import write_wav
from xnb_parse.file_formats.xml_utils import ET
from xnb_parse.xna_types.xna_primitive import Enum


class SoundEffect(object):
    def __init__(self, sound_format, sound_data, loop_start, loop_length, duration, needs_swap=False):
        self.sound_format = sound_format
        self.sound_data = sound_data
        self.loop_start = loop_start
        self.loop_length = loop_length
        self.duration = duration
        self.needs_swap = needs_swap

    def __str__(self):
        return "SoundEffect fs:{} ds:{} d:{}ms ls:{} ll:{}".format(len(self.sound_format), len(self.sound_data),
                                                                   self.duration, self.loop_start, self.loop_length)

    def export(self, filename):
        write_wav(filename, self.sound_format, self.sound_data, self.needs_swap)

    def xml(self, parent=None):
        if parent is None:
            root = ET.Element('SoundEffect')
        else:
            root = ET.SubElement(parent, 'SoundEffect')
        root.set('loopStart', str(self.loop_start))
        root.set('loopLength', str(self.loop_length))
        root.set('duration', str(self.duration))
        return root


class Song(object):
    def __init__(self, filename, duration):
        self.filename = filename
        self.duration = duration

    def __str__(self):
        return "Song f:'{}' d:{}ms".format(self.filename, self.duration)

    def xml(self, parent=None):
        if parent is None:
            root = ET.Element('Song')
        else:
            root = ET.SubElement(parent, 'Song')
        root.set('filename', self.filename)
        root.set('duration', str(self.duration))
        return root


class Video(object):
    def __init__(self, filename, duration, width, height, fps, video_soundtrack_type):
        self.filename = filename
        self.duration = duration
        self.width = width
        self.height = height
        self.fps = fps
        self.video_soundtrack_type = video_soundtrack_type

    def __str__(self):
        return "Video f:'{}' d:{}ms s:{}x{} f:{:.2f} t:{}".format(self.filename, self.duration, self.width, self.height,
                                                                  self.fps, self.video_soundtrack_type)

    def xml(self, parent=None):
        if parent is None:
            root = ET.Element('Video')
        else:
            root = ET.SubElement(parent, 'Video')
        if self.filename is not None:
            root.set('filename', self.filename)
        if self.duration is not None:
            root.set('duration', str(self.duration))
        if self.width is not None:
            root.set('width', str(self.width))
        if self.height is not None:
            root.set('height', str(self.height))
        if self.fps is not None:
            root.set('fps', str(self.fps))
        if self.video_soundtrack_type is not None:
            root.set('soundtrackType', str(self.video_soundtrack_type))
        return root


class VideoSoundtrackType(Enum):
    __slots__ = ()
    enum_values = dict(enumerate(['Music', 'Dialog', 'MusicAndDialog']))

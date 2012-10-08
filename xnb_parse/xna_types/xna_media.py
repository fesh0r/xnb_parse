"""
media types
"""

from xnb_parse.file_formats.xml_utils import E
from xnb_parse.xna_types.xna_primitive import Enum


class SoundEffect(object):
    def __init__(self, sound_format, sound_data, loop_start, loop_length, duration):
        self.sound_format = sound_format
        self.sound_data = sound_data
        self.loop_start = loop_start
        self.loop_length = loop_length
        self.duration = duration

    def __str__(self):
        return "SoundEffect fs:%d ds:%d d:%dms ls:%d ll:%d" % (len(self.sound_format), len(self.sound_data),
                                                               self.duration, self.loop_start, self.loop_length)

    def xml(self):
        return E.SoundEffect(loopStart=str(self.loop_start), loopLength=str(self.loop_length),
                             duration=str(self.duration))

    def export(self, _):
        return self.xml()


class Song(object):
    def __init__(self, filename, duration):
        self.filename = filename
        self.duration = duration

    def __str__(self):
        return "Song f:'%s' d:%dms" % (self.filename, self.duration)

    def xml(self):
        return E.Song(filename=self.filename, duration=str(self.duration))

    def export(self, _):
        return self.xml()


class Video(object):
    def __init__(self, filename, duration, width, height, fps, video_soundtrack_type):
        self.filename = filename
        self.duration = duration
        self.width = width
        self.height = height
        self.fps = fps
        self.video_soundtrack_type = video_soundtrack_type

    def __str__(self):
        return "Video f:'%s' d:%dms s:%dx%d f:%d t:%s" % (self.filename, self.duration, self.width, self.height,
                                                          self.fps, self.video_soundtrack_type)

    def xml(self):
        return E.Video(filename=self.filename, duration=str(self.duration), width=str(self.width),
                       height=str(self.height), fps=str(self.fps), soundtrackType=str(self.video_soundtrack_type))

    def export(self, _):
        return self.xml()


class VideoSoundtrackType(Enum):
    enum_values = dict(enumerate(['Music', 'Dialog', 'MusicAndDialog']))

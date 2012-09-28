"""
media types
"""


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


class Song(object):
    def __init__(self, filename, duration):
        self.filename = filename
        self.duration = duration

    def __str__(self):
        return "Song f:'%s' d:%dms" % (self.filename, self.duration)


class Video(object):
    def __init__(self, filename, duration, width, height, fps, video_type):
        self.filename = filename
        self.duration = duration
        self.width = width
        self.height = height
        self.fps = fps
        self.video_type = video_type

    def __str__(self):
        return "Video f:'%s' d:%dms s:%dx%d f:%d t:%d" % (self.filename, self.duration, self.width, self.height,
                                                          self.fps, self.video_type)

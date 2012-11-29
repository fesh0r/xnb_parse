"""
media type readers
"""

from __future__ import print_function

from xnb_parse.type_reader import TypeReaderPlugin, BaseTypeReader
from xnb_parse.type_readers.xna_primitive import StringReader, Int32Reader, SingleReader
from xnb_parse.xna_types.xna_media import SoundEffect, Song, Video, VideoSoundtrackType


class SoundEffectReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.Audio.SoundEffect'
    reader_name = 'Microsoft.Xna.Framework.Content.SoundEffectReader'

    def read(self):
        format_size = self.stream.read_int32()
        wave_format = self.stream.read(format_size)
        data_size = self.stream.read_int32()
        wave_data = self.stream.read(data_size)
        loop_start = self.stream.read_int32()
        loop_length = self.stream.read_int32()
        duration = self.stream.read_int32()
        return SoundEffect(wave_format, wave_data, loop_start, loop_length, duration, self.stream.needs_swap)


class SongReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.Media.Song'
    reader_name = 'Microsoft.Xna.Framework.Content.SongReader'

    def read(self):
        filename = self.stream.read_string()
        duration = self.stream.read_int32()
        return Song(filename, duration)


class VideoReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.Media.Video'
    reader_name = 'Microsoft.Xna.Framework.Content.VideoReader'

    def read(self):
        filename = self.stream.read_object(StringReader)
        duration = self.stream.read_object(Int32Reader)
        width = self.stream.read_object(Int32Reader)
        height = self.stream.read_object(Int32Reader)
        fps = self.stream.read_object(SingleReader)
        video_soundtrack_type = VideoSoundtrackType(self.stream.read_object(Int32Reader))
        return Video(filename, duration, width, height, fps, video_soundtrack_type)

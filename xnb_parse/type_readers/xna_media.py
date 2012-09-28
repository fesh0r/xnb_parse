"""
media type readers
"""

from xnb_parse.type_reader import BaseTypeReader
from xnb_parse.type_reader_manager import TypeReaderPlugin
from xnb_parse.xna_types.xna_media import SoundEffect, Song, Video


class SoundEffectReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.Audio.SoundEffect'
    reader_name = 'Microsoft.Xna.Framework.Content.SoundEffectReader'

    def read(self):
        format_size = self.stream.read('u4')
        wave_format = self.stream.pull(format_size)
        data_size = self.stream.read('u4')
        wave_data = self.stream.pull(data_size)
        loop_start = self.stream.read('s4')
        loop_length = self.stream.read('s4')
        duration = self.stream.read('s4')
        return SoundEffect(wave_format, wave_data, loop_start, loop_length, duration)


class SongReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.Media.Song'
    reader_name = 'Microsoft.Xna.Framework.Content.SongReader'

    def read(self):
        filename = self.stream.read_object('System.String')
        duration = self.stream.read_object('System.Int32')
        return Song(filename, duration)


class VideoReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.Media.Video'
    reader_name = 'Microsoft.Xna.Framework.Content.VideoReader'

    def read(self):
        filename = self.stream.read_object('System.String')
        duration = self.stream.read_object('System.Int32')
        width = self.stream.read_object('System.Int32')
        height = self.stream.read_object('System.Int32')
        fps = self.stream.read_object('System.Single')
        video_type = self.stream.read_object('System.Int32')
        return Video(filename, duration, width, height, fps, video_type)

"""
media type readers
"""

from xnb_parse.type_reader import BaseTypeReader
from xnb_parse.type_reader_manager import TypeReaderPlugin


class SoundEffectReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.Audio.SoundEffect'
    reader_name = 'Microsoft.Xna.Framework.Content.SoundEffectReader'


class SongReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.Media.Song'
    reader_name = 'Microsoft.Xna.Framework.Content.SongReader'


class VideoReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.Media.Video'
    reader_name = 'Microsoft.Xna.Framework.Content.VideoReader'

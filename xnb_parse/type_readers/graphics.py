"""
graphics types
"""

from xnb_parse.type_reader_manager import BaseTypeReader


class TextureReader(BaseTypeReader):
    name = 'Texture'


class Texture2DReader(TextureReader):
    name = 'Texture2D'

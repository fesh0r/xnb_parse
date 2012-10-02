"""
FEZ basic type readers
"""

from xnb_parse.type_reader import ValueTypeReader
from xnb_parse.type_reader_manager import TypeReaderPlugin


class FaceOrientationReader(ValueTypeReader, TypeReaderPlugin):
    target_type = 'FezEngine.FaceOrientation'
    reader_name = 'FezEngine.FaceOrientationReader'

    def read(self):
        return self.stream.read('u4')


class LevelNodeTypeReader(ValueTypeReader, TypeReaderPlugin):
    target_type = 'FezEngine.LevelNodeType'
    reader_name = 'FezEngine.LevelNodeTypeReader'

    def read(self):
        return self.stream.read('u4')


class NpcActionReader(ValueTypeReader, TypeReaderPlugin):
    target_type = 'FezEngine.Structure.NpcAction'
    reader_name = 'FezEngine.Readers.NpcActionReader'

    def read(self):
        return self.stream.read('u4')


class ActorTypeReader(ValueTypeReader, TypeReaderPlugin):
    target_type = 'FezEngine.Structure.ActorType'
    reader_name = 'FezEngine.Readers.ActorTypeReader'

    def read(self):
        return self.stream.read('u4')

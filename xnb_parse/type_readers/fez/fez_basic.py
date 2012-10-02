"""
FEZ basic type readers
"""

from xnb_parse.type_reader import ValueTypeReader, GenericTypeReader
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


class CollisionTypeReader(ValueTypeReader, TypeReaderPlugin):
    target_type = 'FezEngine.CollisionType'
    reader_name = 'FezEngine.Readers.CollisionTypeReader'

    def read(self):
        return self.stream.read('u4')


class SurfaceTypeReader(ValueTypeReader, TypeReaderPlugin):
    target_type = 'FezEngine.Structure.SurfaceType'
    reader_name = 'FezEngine.Readers.SurfaceTypeReader'

    def read(self):
        return self.stream.read('u4')


class SetReader(GenericTypeReader, TypeReaderPlugin):
    generic_target_type = 'Common.Set`1'
    generic_reader_name = 'FezEngine.SetReader`1'

    def read(self):
        return None


class IEqualityComparerFaceOrientationReader(GenericTypeReader, TypeReaderPlugin):
    generic_target_type = 'System.Collections.Generic.IEqualityComparer`1'
    generic_reader_name = 'FezEngine.IEqualityComparerReader`1'

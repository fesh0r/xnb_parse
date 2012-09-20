"""
load and manage type readers
"""

from xnb_parse.type_spec import TypeSpec


class TypeReaderManager(object):
    def __init__(self, reader_dir=None):
        self.reader_dir = reader_dir
        self.type_readers = {}

    def get_type(self, name, version):
        name = self.strip_assembly_version(name)
        return BaseTypeReader(name, version)

    @staticmethod
    def strip_assembly_version(name):
        type_spec = TypeSpec.parse(name)
        return type_spec.full_name


class BaseTypeReader(object):
    def __init__(self, name, version):
        self.stream = None
        self.name = name
        self.version = version

    def __str__(self):
        return self.name

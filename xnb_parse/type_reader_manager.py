"""
load and manager type readers
"""


class TypeReaderManager(object):
    def __init__(self, reader_dir=None):
        self.reader_dir = reader_dir
        self.type_readers = {}

    def get_type(self, name, version):
        name = self.strip_assembly_version(name)
        return BaseTypeReader(name, version)

    @staticmethod
    def strip_assembly_version(name):
        return name


class BaseTypeReader(object):
    def __init__(self, name, version):
        self.stream = None
        self.name = name
        self.version = version

    def __str__(self):
        return self.name


class _ArraySpec(object):
    def __init__(self, dimensions, bound):
        self.dimensions = dimensions
        self.bound = bound


class _TypeSpec(object):
    def __init__(self):
        self.name = None
        self.assembly_name = None
        self.nested = []
        self.generic_params = []
        self.array_spec = []
        self.pointer_level = 0
        self.is_byref = False

    @staticmethod
    def parse(type_name):
        if type_name is None:
            raise ValueError('type_name')
        res, pos = _TypeSpec._parse(type_name)
        if pos < len(type_name):
            raise ValueError('Count not parse the whole type name')
        return res

    def add_name(self, type_name):
        if self.name is None:
            self.name = type_name
        else:
            self.nested.append(type_name)

    def add_array(self, array):
        self.array_spec.append(array)

    @staticmethod
    def skip_space(name, pos):
        p = pos
        while p < len(name) and name[p].isspace():
            p += 1
        return p

    @staticmethod
    def _parse(name, pos=0, is_recurse=False, allow_aqn=False):
        in_modifiers = False

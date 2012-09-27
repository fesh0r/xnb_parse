"""
load and manage type readers
"""

import pkgutil

from xnb_parse.type_spec import TypeSpec
from xnb_parse.type_reader import ReaderError


class TypeReaderManager(object):
    type_readers = {}

    def __init__(self, reader_dir=None):
        self.reader_dir = reader_dir
        self.type_readers = {}
        classes = _find_subclasses('xnb_parse.type_readers', TypeReaderPlugin)
        for c in classes:
            if c.reader_name in self.type_readers:
                raise ReaderError("Duplicate type reader: '%s'" % c.reader_name)
            self.type_readers[c.reader_name] = c

    def get_type_reader(self, name):
        type_spec = TypeSpec.parse(name)

        simple_name = type_spec.full_name
        if simple_name in self.type_readers:
            return self.type_readers[simple_name]

        # need special handling for generic type readers

        raise ReaderError("Type reader not found for '%s'" % simple_name)


def _find_subclasses(pkgname, cls):
    # iccck, must be a better way of doing this
    pkg = __import__(pkgname)
    for sub_pkg in pkgname.split('.')[1:]:
        pkg = getattr(pkg, sub_pkg)
    for _, modulename, _ in pkgutil.walk_packages(pkg.__path__, pkg.__name__ + '.'):
        __import__(modulename)
    return cls.__subclasses__()


class Plugin(object):
    """
    marker class for plugins
    """


class TypeReaderPlugin(Plugin):
    """
    type reader plugins
    """

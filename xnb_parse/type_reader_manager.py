"""
load and manage type readers
"""

import pkgutil

from xnb_parse.type_spec import TypeSpec


class Error(Exception):
    pass


class ReaderError(Error):
    pass


class TypeReaderManager(object):
    type_readers = {}

    def __init__(self, reader_dir=None):
        self.reader_dir = reader_dir
        self.type_readers = {}
        classes = _find_subclasses('xnb_parse.type_readers', BaseTypeReader)
        for c in classes:
            if c.reader_name in self.type_readers:
                raise ReaderError("Duplicate type reader: '%s'" % c.reader_name)
            self.type_readers[c.reader_name] = c

    def get_type(self, name):
        type_spec = TypeSpec.parse(name)

        simple_name = type_spec.full_name
        if simple_name in self.type_readers:
            return self.type_readers[simple_name]

        # need special handling for generic type readers

        raise ReaderError("Type reader not found for '%s'" % simple_name)


class BaseTypeReader(object):
    target_type = None
    reader_name = None
    is_value_type = False

    def __init__(self, stream, version):
        self.stream = stream
        self.version = version

    def __str__(self):
        return self.reader_name

    def read(self):
        raise ReaderError("Unimplemented type reader: '%s'" % self.reader_name)


def _find_subclasses(pkgname, cls):
    subclasses = []

    # iccck, must be a better way of doing this
    pkg = __import__(pkgname)
    for d in pkgname.split('.')[1:]:
        pkg = getattr(pkg, d)
    for _, modulename, _ in pkgutil.walk_packages(pkg.__path__, pkg.__name__ + '.'):
#        print 'searching', modulename
        module = __import__(modulename)
        for d in modulename.split('.')[1:]:
            module = getattr(module, d)
        # look through module dictionary for things that are subclass of cls but are not cls itself
        for key, entry in module.__dict__.items():
            if key == cls.__name__:
                continue
            try:
                if issubclass(entry, cls):
#                    print 'Found subclass:', key
                    subclasses.append(entry)
            except TypeError:
                # this happens when a non-type is passed in to issubclass. We don't care as it can't be a subclass of
                # cls if it isn't a type
                continue
    return subclasses

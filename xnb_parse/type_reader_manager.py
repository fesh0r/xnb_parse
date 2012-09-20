"""
load and manage type readers
"""

import pkgutil

from xnb_parse.type_spec import TypeSpec


class TypeReaderManager(object):
    type_readers = {}

    def __init__(self, reader_dir=None):
        self.reader_dir = reader_dir
        self.type_readers = {}
        classes = _find_subclasses('xnb_parse.type_readers', BaseTypeReader)
        print classes

    def get_type(self, name, version):
        name = self.strip_assembly_version(name)
        return name

    @staticmethod
    def strip_assembly_version(name):
        type_spec = TypeSpec.parse(name)
        return type_spec.full_name


class BaseTypeReader(object):
    name = None

    def __str__(self):
        return self.name


def _find_subclasses(pkgname, cls):
    subclasses = []

    # iccck, must be a better way of doing this
    pkg = __import__(pkgname)
    for d in pkgname.split('.')[1:]:
        pkg = getattr(pkg, d)
    for _, modulename, _ in pkgutil.walk_packages(pkg.__path__, pkg.__name__ + '.'):
        print 'searching', modulename
        module = __import__(modulename)
        for d in modulename.split('.')[1:]:
            module = getattr(module, d)
        # look through module dictionary for things that are subclass of cls but are not cls itself
        for key, entry in module.__dict__.items():
            if key == cls.__name__:
                continue
            try:
                if issubclass(entry, cls):
                    print 'Found subclass:', key
                    subclasses.append(entry)
            except TypeError:
                # this happens when a non-type is passed in to issubclass. We don't care as it can't be a subclass of
                # cls if it isn't a type
                continue
    return subclasses

# coding=utf-8
"""
load and manage type readers
"""

from __future__ import absolute_import, division

import pkgutil

from xnb_parse.type_spec import TypeSpec
from xnb_parse.type_reader import ReaderError, GenericTypeReader, BaseTypeReader


class TypeReaderManager(object):
    def __init__(self):
        self.type_readers = {}
        self.type_readers_type = {}
        self.generic_type_readers = {}
        self.generic_type_readers_type = {}
        classes = _find_subclasses('xnb_parse.type_readers', TypeReaderPlugin)
        for class_ in classes:
            if issubclass(class_, GenericTypeReader):
                if class_.generic_reader_name in self.generic_type_readers:
                    raise ReaderError("Duplicate generic type reader name: '%s'" % class_.generic_reader_name)
                self.generic_type_readers[class_.generic_reader_name] = class_
                if class_.generic_target_type in self.generic_type_readers:
                    raise ReaderError("Duplicate generic type reader type: '%s'" % class_.generic_target_type)
                self.generic_type_readers_type[class_.generic_target_type] = class_
            elif issubclass(class_, BaseTypeReader):
                if class_.reader_name in self.type_readers:
                    raise ReaderError("Duplicate type reader name: '%s'" % class_.reader_name)
                self.type_readers[class_.reader_name] = class_
                if class_.target_type in self.type_readers_type:
                    raise ReaderError("Duplicate type reader type: '%s'" % class_.target_type)
                self.type_readers_type[class_.target_type] = class_
            else:
                raise ReaderError("Unknown base class for reader: '%s'" % str(class_))

    def get_type_reader(self, type_reader):
        try:
            name = type_reader.reader_name
        except AttributeError:
            name = type_reader

        type_spec = TypeSpec.parse(name)

        if type_spec.full_name in self.type_readers:
            return self.type_readers[type_spec.full_name]

        if type_spec.generic_params:
            if type_spec.name in self.generic_type_readers:
                generic_type_class = self.generic_type_readers[type_spec.name]
                generic_type_reader_class = generic_type_class.create_from_type(type_spec)
                if generic_type_reader_class.reader_name in self.type_readers:
                    raise ReaderError("Duplicate type reader name from generic: '%s' '%s'" % (
                        generic_type_reader_class.reader_name, generic_type_class.generic_reader_name))
                self.type_readers[generic_type_reader_class.reader_name] = generic_type_reader_class
                if generic_type_reader_class.target_type in self.type_readers_type:
                    raise ReaderError("Duplicate type reader type from generic: '%s' '%s'" % (
                        generic_type_reader_class.target_type, generic_type_class.generic_target_type))
                self.type_readers_type[generic_type_reader_class.target_type] = generic_type_reader_class
                return generic_type_reader_class

        raise ReaderError("Type reader not found: '%s'" % type_spec.full_name)

    def get_type_reader_by_type(self, type_reader):
        try:
            reader_type = type_reader.target_type
        except AttributeError:
            reader_type = type_reader

        type_spec = TypeSpec.parse(reader_type)

        if type_spec.full_name in self.type_readers_type:
            return self.type_readers_type[type_spec.full_name]

        if type_spec.generic_params:
            if type_spec.name in self.generic_type_readers_type:
                generic_type_class = self.generic_type_readers_type[type_spec.name]
                generic_type_reader_class = generic_type_class.create_from_type(type_spec)
                if generic_type_reader_class.reader_name in self.type_readers:
                    raise ReaderError("Duplicate type reader name from generic: '%s' '%s'" % (
                        generic_type_reader_class.reader_name, generic_type_class.generic_reader_name))
                self.type_readers[generic_type_reader_class.reader_name] = generic_type_reader_class
                if generic_type_reader_class.target_type in self.type_readers_type:
                    raise ReaderError("Duplicate type reader type from generic: '%s' '%s'" % (
                        generic_type_reader_class.target_type, generic_type_class.generic_target_type))
                self.type_readers_type[generic_type_reader_class.target_type] = generic_type_reader_class
                return generic_type_reader_class

        raise ReaderError("Type reader not found: '%s'" % type_spec.full_name)


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

"""
Base type readers
"""

from __future__ import print_function

# avoid circular import
VERSION_40 = 5


class Error(Exception):
    pass


class ReaderError(Error):
    pass


class NotGenericError(ReaderError):
    pass


class Plugin(object):
    """
    marker class for plugins
    """


class TypeReaderPlugin(Plugin):
    """
    type reader plugins
    """


class BaseTypeReader(object):
    target_type = None
    reader_name = None
    is_value_type = False
    is_generic_type = False
    is_enum_type = False
    file_platform = None
    file_version = None

    def __init__(self, stream=None, version=None):
        self.stream = stream
        self.version = version

    def __str__(self):
        return self.reader_name

    def read(self):
        raise ReaderError("Unimplemented type reader: '{}'".format(self.reader_name))

    def init_reader(self, file_platform=None, file_version=None):
        self.file_platform = file_platform
        self.file_version = file_version


class ValueTypeReader(BaseTypeReader):
    is_value_type = True


class GenericTypeReader(BaseTypeReader):
    generic_target_type = None
    generic_reader_name = None
    is_generic_type = True
    generic_params = None
    readers = None

    def init_reader(self, file_platform=None, file_version=None):
        BaseTypeReader.init_reader(self, file_platform, file_version)
        if self.readers is None:
            self.readers = []
        for arg in self.generic_params:
            reader = self.stream.get_type_reader_by_type(arg)
            reader.init_reader(file_platform, file_version)
            self.readers.append(reader)

    @classmethod
    def create_from_type(cls, type_spec):
        # really need to figure out how to do this more cleanly
        body = dict(cls.__dict__)
        body['target_type'] = cls.generic_target_type + type_spec.suffix
        body['reader_name'] = cls.generic_reader_name + type_spec.suffix
        body['generic_params'] = [arg.full_name for arg in type_spec.generic_params]
        class_ = type(cls.__name__, cls.__bases__, body)
        return class_


class GenericValueTypeReader(GenericTypeReader):
    is_value_type = True


class EnumTypeReader(ValueTypeReader):
    is_enum_type = True
    enum_type = None
    enum_type4 = None

    def read(self):
        value = self.stream.read_int32()
        if self.file_version == VERSION_40 and self.enum_type4 is not None:
            enum_type = self.enum_type4
        else:
            enum_type = self.enum_type
        if callable(enum_type):
            return enum_type(value)
        else:
            return value


def generic_reader_name(main_type, args=None):
    if args is None:
        args = []
    try:
        full_args = [arg.target_type for arg in args]
    except AttributeError:
        full_args = args
    try:
        return main_type.generic_reader_name + '[' + ','.join(full_args) + ']'
    except AttributeError:
        raise NotGenericError("Not generic type: '{}'".format(main_type))


def generic_reader_type(main_type, args=None):
    if args is None:
        args = []
    try:
        full_args = [arg.target_type for arg in args]
    except AttributeError:
        full_args = args
    try:
        return main_type.generic_target_type + '[' + ','.join(full_args) + ']'
    except AttributeError:
        raise NotGenericError("Not generic type: '{}'".format(main_type.complete_name))

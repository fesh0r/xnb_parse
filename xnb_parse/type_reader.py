"""
Base type readers
"""


class Error(Exception):
    pass


class ReaderError(Error):
    pass


class NotGenericError(ReaderError):
    pass


class BaseTypeReader(object):
    target_type = None
    reader_name = None
    is_value_type = False
    is_generic_type = False
    is_enum_type = False

    def __init__(self, stream=None, version=None):
        self.stream = stream
        self.version = version

    def __str__(self):
        return self.reader_name

    def read(self):
        raise ReaderError("Unimplemented type reader: '%s'" % self.reader_name)

    def init_reader(self):
        pass


class ValueTypeReader(BaseTypeReader):
    is_value_type = True


class GenericTypeReader(BaseTypeReader):
    generic_target_type = None
    generic_reader_name = None
    is_generic_type = True
    generic_params = None
    readers = None

    def init_reader(self):
        BaseTypeReader.init_reader(self)
        if self.readers is None:
            self.readers = []
        for arg in self.generic_params:
            reader = self.stream.get_type_reader_by_type(arg)
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

    def read(self):
        value = self.stream.read_int32()
        if self.enum_type is not None:
            return self.enum_type(value)  # pylint: disable-msg=E1102
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
        raise ReaderError("Not generic type: '%s'" % main_type)


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
        raise NotGenericError("Not generic type: '%s'" % main_type.complete_name)

"""
Base type readers
"""


class Error(Exception):
    pass


class ReaderError(Error):
    pass


class BaseTypeReader(object):
    target_type = None
    reader_name = None
    is_value_type = False
    is_generic_type = False

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
        body['reader_name'] = type_spec.full_name
        body['generic_params'] = [arg.full_name for arg in type_spec.generic_params]
        class_ = type(cls.__name__, cls.__bases__, body)
        return class_


class GenericValueTypeReader(GenericTypeReader):
    is_value_type = True

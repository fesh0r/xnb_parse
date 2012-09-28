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

    @classmethod
    def read_from(cls, stream):
        local_reader = cls.__init__(stream)
        return local_reader.read()

    def init(self):
        pass


class ValueTypeReader(BaseTypeReader):
    is_value_type = True


class GenericTypeReader(BaseTypeReader):
    generic_target_type = None
    generic_reader_name = None
    target_type = None
    reader_name = None
    is_value_type = False
    is_generic_type = True
    name_index = 0
    arguments = []
    readers = []

    def init(self):
        for arg in self.arguments:
            reader = self.stream.type_reader_manager.get_type_reader_by_type(arg)
            self.readers.append(reader)

    @classmethod
    def create(cls, type_spec):
        args = [arg.full_name for arg in type_spec.generic_params]
        class_name = cls.generic_reader_name.rpartition('.')[2]
        class_name = class_name.partition('`')[0]
        class_name += str(cls.name_index)
        cls.name_index += 1
        reader_name = type_spec.full_name
        target_type = cls.generic_target_type
        target_type += ','.join(['[' + arg + ']' for arg in args])
        # really need to figure out how to do this more cleanly
        body = dict(cls.__dict__)
        body['target_type'] = target_type
        body['reader_name'] = reader_name
        body['arguments'] = args
        class_ = type(class_name, cls.__bases__, body)
        return class_


class GenericValueTypeReader(GenericTypeReader):
    is_value_type = True

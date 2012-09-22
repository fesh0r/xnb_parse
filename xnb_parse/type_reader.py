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

    def __init__(self, stream, version):
        self.stream = stream
        self.version = version

    def __str__(self):
        return self.reader_name

    def read(self):
        raise ReaderError("Unimplemented type reader: '%s'" % self.reader_name)


class ValueTypeReader(BaseTypeReader):
    is_value_type = True

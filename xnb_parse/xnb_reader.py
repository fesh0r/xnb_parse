"""
XNB parser
"""

from __future__ import print_function

import os

import sys

from xnb_parse.binstream import BinaryStream
from xnb_parse.type_reader_manager import TypeReaderManager
from xnb_parse.xna_native import decompress
from xnb_parse.type_reader import ReaderError, generic_reader_type
from xnb_parse.type_readers.xna_system import EnumReader
from xnb_parse.xna_types.xna_math import Color, Vector2, Vector3, Vector4, Quaternion, Matrix
from xnb_parse.xna_types.xna_system import XNAList, ExternalReference
from xnb_parse.file_formats.xml_utils import output_xml


XNB_EXTENSION = '.xnb'
XNB_SIGNATURE = b'XNB'
PLATFORM_WINDOWS = b'w'
PLATFORM_XBOX = b'x'
PLATFORM_MOBILE = b'm'
PROFILE_REACH = 0
PROFILE_HIDEF = 1
VERSION_30 = 3
VERSION_31 = 4
VERSION_40 = 5
XNB_PLATFORMS = {PLATFORM_WINDOWS: 'W', PLATFORM_XBOX: 'X', PLATFORM_MOBILE: 'M'}
XNB_VERSIONS = {VERSION_30: '30', VERSION_31: '31', VERSION_40: '40'}
XNB_PROFILES = {PROFILE_REACH: 'r', PROFILE_HIDEF: 'h'}

_PROFILE_MASK = 0x7f
_COMPRESS_MASK = 0x80
_XNB_HEADER = '3s c B B I'


class XNBReader(BinaryStream):
    _type_reader_manager = None

    def __init__(self, data, file_platform=PLATFORM_WINDOWS, file_version=VERSION_40, graphics_profile=PROFILE_REACH,
                 compressed=False, parse=True, expected_type=None):
        BinaryStream.__init__(self, data=data)
        del data
        if XNBReader._type_reader_manager is None:
            XNBReader._type_reader_manager = TypeReaderManager()
        self.type_reader_manager = XNBReader._type_reader_manager
        self.file_platform = file_platform
        self.file_version = file_version
        self.graphics_profile = graphics_profile
        self.compressed = compressed
        self.needs_swap = self.file_platform == PLATFORM_XBOX
        self.type_readers = []
        self.shared_objects = []
        self.content = None
        if parse:
            self.parse(expected_type=expected_type)

    def __str__(self):
        return 'XNB {}{}{} s:{}'.format(XNB_PLATFORMS[self.file_platform], XNB_VERSIONS[self.file_version],
                                        XNB_PROFILES[self.graphics_profile], self.length())

    def parse(self, expected_type=None, verbose=False):
        if self.content is not None:
            return self.content

        reader_count = self.read_7bit_encoded_int()
        for _ in range(reader_count):
            reader_name = self.read_string()
            reader_version = self.read_int32()
            reader = self.get_type_reader(reader_name, reader_version)
            self.type_readers.append(reader)

        if verbose:
            print("Type: {!s}".format(self.type_readers[0]))

        for reader in self.type_readers:
            reader.init_reader(self.file_platform, self.file_version)

        shared_count = self.read_7bit_encoded_int()

        if shared_count:
            raise ReaderError("Shared resources present")

        self.content = self.read_object(expected_type=expected_type)
        if verbose:
            print("Asset: {!s}".format(self.content))

        for i in range(shared_count):
            obj = self.read_object()
            self.shared_objects.append(obj)
            if verbose:
                print("Shared resource {}: {!s}".format(i, obj))

        remaining = self.read()
        if len(remaining):
            print("remaining bytes: {}".format(len(remaining)), file=sys.stderr)
        return self.content

    def get_type_reader(self, type_reader, version=None):
        reader_type_class = self.type_reader_manager.get_type_reader(type_reader)
        return reader_type_class(self, version)

    def get_type_reader_by_type(self, type_reader, version=None):
        reader_type_class = self.type_reader_manager.get_type_reader_by_type(type_reader)
        return reader_type_class(self, version)

    @classmethod
    def load(cls, data=None, filename=None, parse=True, expected_type=None):
        if filename is not None:
            filename = os.path.normpath(filename)
        stream = BinaryStream(data=data, filename=filename)
        del data
        (sig, platform, version, attribs, size) = stream.unpack(_XNB_HEADER)
        if sig != XNB_SIGNATURE:
            raise ReaderError("bad sig: '{!r}'".format(sig))
        if platform not in XNB_PLATFORMS:
            raise ReaderError("bad platform: '{!r}'".format(platform))
        if version not in XNB_VERSIONS:
            raise ReaderError("bad version: {}".format(version))
        stream_length = stream.length()
        if stream_length != size:
            raise ReaderError("bad size: {} != {}".format(stream_length, size))
        compressed = False
        profile = 0
        if version >= VERSION_40:
            profile = attribs & _PROFILE_MASK
            if profile not in XNB_PROFILES:
                raise ReaderError("bad profile: {}".format(profile))
        if version >= VERSION_30:
            compressed = bool(attribs & _COMPRESS_MASK)
            size -= stream.calc_size(_XNB_HEADER)
        if compressed:
            uncomp = stream.read_int32()
            size -= 4
            content_comp = stream.read(size)
            content = decompress(content_comp, uncomp)
        else:
            content = stream.read(size)
        return cls(content, platform, version, profile, compressed, parse=parse, expected_type=expected_type)

    def save(self, filename=None, compress=False):
        if self.file_platform not in XNB_PLATFORMS:
            raise ReaderError("bad platform: '{!r}'".format(self.file_platform))
        if self.file_version not in XNB_VERSIONS:
            raise ReaderError("bad version: {}".format(self.file_version))
        attribs = 0
        if self.file_version >= VERSION_40:
            if self.graphics_profile not in XNB_PROFILES:
                raise ReaderError("bad profile: {}".format(self.graphics_profile))
            attribs |= self.graphics_profile & _PROFILE_MASK
        do_compress = False
        if self.file_version >= VERSION_30:
            if compress:
                do_compress = True
                attribs |= _COMPRESS_MASK
        stream = BinaryStream()
        if do_compress:
            raise ReaderError("Recompression not supported")
        else:
            data = self.getvalue()
            size = len(data) + stream.calc_size(_XNB_HEADER)
        stream.pack(_XNB_HEADER, XNB_SIGNATURE, self.file_platform, self.file_version, attribs, size)
        stream.write(data)
        if filename is not None:
            filename = os.path.normpath(filename)
            dirname = os.path.dirname(filename)
            if not os.path.isdir(dirname):
                os.makedirs(dirname)
            if not filename.endswith(XNB_EXTENSION):
                filename += XNB_EXTENSION
            stream.write_file(filename)
        else:
            return stream.getvalue()

    def read_object(self, expected_type_reader=None, type_params=None, expected_type=None):
        type_id = self.read_7bit_encoded_int()
        if type_id == 0:
            # null object
            return None
        try:
            type_reader = self.type_readers[type_id - 1]
        except IndexError:
            raise ReaderError("type id out of range: {} > {}".format(type_id, len(self.type_readers)))
        if expected_type_reader is not None:
            try:
                if expected_type_reader.is_generic_type and expected_type_reader.target_type is None:
                    expected_type = generic_reader_type(expected_type_reader, type_params)
                elif expected_type_reader.is_enum_type:
                    expected_type = generic_reader_type(EnumReader, [expected_type_reader.target_type])
                else:
                    expected_type = expected_type_reader.target_type
            except AttributeError:
                raise ReaderError("bad expected_type_reader: '{}'".format(expected_type_reader))
        if expected_type is not None:
            if expected_type != 'System.Object':
                if type_reader.target_type != expected_type:
                    # check parent type readers
                    for cls in type_reader.__class__.__mro__:
                        if hasattr(cls, 'target_type'):
                            if cls.target_type == expected_type:
                                break
                    else:
                        raise ReaderError("Unexpected type: '{}' != '{}'".format(type_reader.target_type,
                                                                                 expected_type))
        return type_reader.read()

    def read_value_or_object(self, expected_type):
        if expected_type.is_value_type:
            type_reader = self.get_type_reader(expected_type)
            return type_reader.read()
        else:
            return self.read_object(expected_type=expected_type)

    def read_type_id(self):
        type_id = self.read_7bit_encoded_int()
        if type_id == 0:
            # null object
            return None
        try:
            return self.type_readers[type_id - 1]
        except IndexError:
            raise ReaderError("type id out of range: {} > {}".format(type_id, len(self.type_readers)))

    def export(self, filename, export_file=True, export_xml=True):
        if not hasattr(self, 'content'):
            raise ReaderError("XNB content deleted")
        if self.content is None:
            self.parse()
        filename = os.path.normpath(filename)
        dirname = os.path.dirname(filename)
        if not os.path.isdir(dirname):
            os.makedirs(dirname)
        if export_file and hasattr(self.content, 'export'):
            self.content.export(filename)
        if export_xml and hasattr(self.content, 'xml'):
            output_xml(self.content.xml(), filename + '.xml')

    def read_color(self):
        return Color._make(self.unpack('4B'))

    def read_external_reference(self, expected_type=None):
        filename = self.read_string()
        return ExternalReference(filename, expected_type)

    def read_matrix(self):
        return Matrix(XNAList(self.unpack('16f')))

    def read_quaternion(self):
        return Quaternion._make(self.unpack('4f'))

    def read_vector2(self):
        return Vector2._make(self.unpack('2f'))

    def read_vector3(self):
        return Vector3._make(self.unpack('3f'))

    def read_vector4(self):
        return Vector4._make(self.unpack('4f'))

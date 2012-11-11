# coding=utf-8
"""
XNB parser
"""

from __future__ import absolute_import, division, unicode_literals

import os

from xnb_parse.binstream import BinaryReader, BinaryWriter
from xnb_parse.xna_native import decompress
from xnb_parse.type_reader import ReaderError, generic_reader_type
from xnb_parse.type_readers.xna_system import EnumReader
from xnb_parse.xna_types.xna_math import Color, Vector2, Vector3, Vector4, Quaternion, Matrix
from xnb_parse.xna_types.xna_system import XNAList, ExternalReference
from xnb_parse.file_formats.xml_utils import output_xml


XNB_SIGNATURE = 'XNB'
PLATFORM_WINDOWS = 'w'
PLATFORM_XBOX = 'x'
PLATFORM_MOBILE = 'm'
PROFILE_REACH = 0
PROFILE_HIDEF = 1
VERSION_30 = 3
VERSION_31 = 4
VERSION_40 = 5


class XNBReader(BinaryReader):
    platforms = {PLATFORM_WINDOWS: 'W', PLATFORM_XBOX: 'X', PLATFORM_MOBILE: 'M'}
    versions = {VERSION_30: '30', VERSION_31: '31', VERSION_40: '40'}
    profiles = {PROFILE_REACH: 'r', PROFILE_HIDEF: 'h'}

    _profile_mask = 0x7f
    _compress_mask = 0x80

    _header = '3s c B B I'

    def __init__(self, data, file_platform=PLATFORM_WINDOWS, file_version=VERSION_40, graphics_profile=PROFILE_REACH,
                 compressed=False, type_reader_manager=None, parse=True, expected_type_reader=None):
        BinaryReader.__init__(self, data)
        self.file_platform = file_platform
        self.file_version = file_version
        self.graphics_profile = graphics_profile
        self.compressed = compressed
        self.needs_swap = self.file_platform == PLATFORM_XBOX
        self.type_reader_manager = type_reader_manager
        self.type_readers = []
        self.shared_objects = []
        self.expected_type_reader = expected_type_reader
        self.content = None
        self.length = len(self.data)
        if parse:
            self.parse()

    def __str__(self):
        return 'XNB %s%s%s s:%d' % (self.platforms[self.file_platform], self.versions[self.file_version],
                                    self.profiles[self.graphics_profile], self.length)

    def parse(self, verbose=False):
        if self.type_reader_manager is None:
            raise ValueError("No type reader manager")
        if self.content is not None:
            return self.content

        reader_count = self.read_7bit_encoded_int()
        for _ in range(reader_count):
            reader_name = self.read_string()
            reader_version = self.read_int32()
            reader = self.get_type_reader(reader_name, reader_version)
            self.type_readers.append(reader)

        if verbose:
            print "Type: '%s'" % str(self.type_readers[0])

        for reader in self.type_readers:
            reader.init_reader()

        shared_count = self.read_7bit_encoded_int()

        if shared_count:
            raise ReaderError("Shared resources present")

        self.content = self.read_object(self.expected_type_reader)
        if verbose:
            print "Asset: '%s'" % str(self.content)

        for i in range(shared_count):
            obj = self.read_object()
            self.shared_objects.append(obj)
            if verbose:
                print "Shared resource %d: '%s'" % (i, str(obj))

        if self.remaining():
            raise ReaderError("remaining: %d" % self.remaining())
        del self.data
        return self.content

    def get_type_reader(self, type_reader, version=None):
        reader_type_class = self.type_reader_manager.get_type_reader(type_reader)
        return reader_type_class(self, version)

    def get_type_reader_by_type(self, type_reader, version=None):
        reader_type_class = self.type_reader_manager.get_type_reader_by_type(type_reader)
        return reader_type_class(self, version)

    @classmethod
    def load(cls, data, type_reader_manager=None, parse=True):
        stream = BinaryReader(data)
        (sig, platform, version, attribs, size) = stream.unpack(cls._header)
        if sig != XNB_SIGNATURE:
            raise ValueError("bad sig: '%s'" % repr(sig))
        if platform not in cls.platforms:
            raise ValueError("bad platform: '%s'" % repr(platform))
        if version not in cls.versions:
            raise ValueError("bad version: %d" % version)
        if len(data) != size:
            raise ValueError("bad size: %d != %d" % (len(data), size))
        compressed = False
        profile = 0
        if version >= VERSION_40:
            profile = attribs & cls._profile_mask
            if profile not in cls.profiles:
                raise ValueError("bad profile: %d" % profile)
        if version >= VERSION_30:
            compressed = bool(attribs & cls._compress_mask)
            size -= stream.calc_size(cls._header)
        if compressed:
            uncomp = stream.read_int32()
            size -= 4
            content_comp = stream.read_bytes(size)
            content = decompress(content_comp, uncomp)
        else:
            content = stream.read_bytes(size)
        return cls(content, platform, version, profile, compressed, type_reader_manager, parse)

    def save(self, compress=False):
        if not hasattr(self, 'data'):
            raise ValueError("XNB data deleted")
        if self.file_platform not in self.platforms:
            raise ValueError("bad platform: '%s'" % repr(self.file_platform))
        if self.file_version not in self.versions:
            raise ValueError('bad version: %d' % self.file_version)
        attribs = 0
        if self.file_version >= VERSION_40:
            if self.graphics_profile not in self.profiles:
                raise ValueError("bad profile: %d" % self.graphics_profile)
            attribs |= self.graphics_profile & self._profile_mask
        do_compress = False
        if self.file_version >= VERSION_30:
            if compress:
                do_compress = True
                attribs |= self._compress_mask
        stream = BinaryWriter()
        if do_compress:
            raise ValueError("Recompression not supported")
        else:
            data = self.data
            size = len(data) + stream.calc_size(self._header)
        stream.pack(self._header, str(XNB_SIGNATURE), self.file_platform, self.file_version, attribs, size)
        stream.write_bytes(data)
        return stream.serial()

    def read_object(self, expected_type_reader=None, type_params=None):
        type_reader = self.read_type_id()
        if type_reader is None:
            return None
        if expected_type_reader is not None:
            try:
                if expected_type_reader.is_generic_type and expected_type_reader.target_type is None:
                    expected_type = generic_reader_type(expected_type_reader, type_params)
                elif expected_type_reader.is_enum_type:
                    expected_type = generic_reader_type(EnumReader, [expected_type_reader.target_type])
                else:
                    expected_type = expected_type_reader.target_type
            except AttributeError:
                raise ReaderError("bad expected_type_reader: '%s'" % expected_type_reader)
            if type_reader.target_type != expected_type:
                raise ReaderError("Unexpected type: '%s' != '%s'" % (type_reader.target_type, expected_type))
        return type_reader.read()

    def read_value_or_object(self, type_reader):
        if type_reader.is_value_type:
            return type_reader.read()
        else:
            return self.read_object(type_reader)

    def read_type_id(self):
        type_id = self.read_7bit_encoded_int()
        if type_id == 0:
            # null object
            return None
        if type_id > len(self.type_readers):
            raise ReaderError("type id out of range: %d > %d" % (type_id, len(self.type_readers)))
        return self.type_readers[type_id - 1]

    def export(self, filename):
        if not hasattr(self, 'content'):
            raise ValueError("XNB content deleted")
        if self.content is None:
            raise ValueError("XNB content not parsed")
        if hasattr(self.content, 'export'):
            filename = os.path.normpath(filename)
            dirname = os.path.dirname(filename)
            if not os.path.isdir(dirname):
                os.makedirs(dirname)
            self.content.export(filename)
        if hasattr(self.content, 'xml'):
            filename = os.path.normpath(filename)
            dirname = os.path.dirname(filename)
            if not os.path.isdir(dirname):
                os.makedirs(dirname)
            output_xml(self.content.xml(), filename + '.xml')

    def read_color(self):
        v_r = self.read_byte()
        v_g = self.read_byte()
        v_b = self.read_byte()
        v_a = self.read_byte()
        return Color(r=v_r, g=v_g, b=v_b, a=v_a)

    def read_external_reference(self, expected_type=None):
        filename = self.read_string()
        return ExternalReference(filename, expected_type)

    def read_matrix(self):
        matrix = XNAList()
        for _ in range(16):
            value = self.read_single()
            matrix.append(value)
        return Matrix(matrix)

    def read_quaternion(self):
        v_x = self.read_single()
        v_y = self.read_single()
        v_z = self.read_single()
        v_w = self.read_single()
        return Quaternion(v_x, v_y, v_z, v_w)

    def read_vector2(self):
        v_x = self.read_single()
        v_y = self.read_single()
        return Vector2(v_x, v_y)

    def read_vector3(self):
        v_x = self.read_single()
        v_y = self.read_single()
        v_z = self.read_single()
        return Vector3(v_x, v_y, v_z)

    def read_vector4(self):
        v_x = self.read_single()
        v_y = self.read_single()
        v_z = self.read_single()
        v_w = self.read_single()
        return Vector4(v_x, v_y, v_z, v_w)

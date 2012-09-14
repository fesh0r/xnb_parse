"""
XNB parser
"""

from binstream import BinaryReader


XNB_SIGNATURE = 'XNB'
PLATFORM_WINDOWS = 'w'
PLATFORM_XBOX = 'x'
PLATFORM_MOBILE = 'm'
PROFILE_REACH = 0
PROFILE_HIDEF = 1
VERSION_30 = 3
VERSION_31 = 4
VERSION_40 = 5


class XNB(object):
    platforms = [PLATFORM_WINDOWS, PLATFORM_XBOX, PLATFORM_MOBILE]
    versions = [VERSION_30, VERSION_31, VERSION_40]
    profiles = [PROFILE_REACH, PROFILE_HIDEF]

    _profile_mask = 0x7f
    _compress_mask = 0x80

    _header = '3s c B B I'

    def __init__(self, data, file_platform, file_version, graphics_profile, compressed, file_size):
        self.data = data
        self.file_platform = file_platform
        self.file_version = file_version
        self.graphics_profile = graphics_profile
        self.compressed = compressed
        self.file_size = file_size

    @classmethod
    def read(cls, data):
        stream = BinaryReader(data, False)
        header_struct = stream.struct(cls._header)
        (sig, platform, version, attribs, size) = stream.unpack_with(header_struct)
        if sig != XNB_SIGNATURE:
            raise ValueError('bad sig: %s' % repr(sig))
        if platform not in cls.platforms:
            raise ValueError('bad platform: %s' % repr(platform))
        if version not in cls.versions:
            raise ValueError('bad version: %s' % repr(version))
        if len(data) < size:
            raise ValueError('bad size: %d < %d' % (len(data), size))
        compressed = False
        profile = 0
        if version >= VERSION_40:
            profile = attribs & cls._profile_mask
            if profile not in cls.profiles:
                raise ValueError('bad profile: %s' % repr(profile))
        if version >= VERSION_30:
            compressed = bool(attribs & cls._compress_mask)
        if compressed:
            todo = size - header_struct.size - stream.size('u4')
            size = stream.read('u4')
        else:
            size -= header_struct.size
        return cls(stream.remainder(), platform, version, profile, compressed, size)

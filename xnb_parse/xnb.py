"""
XNB parser
"""

from binstream import BinaryReader, BinaryWriter
from xna_native import decompress


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
    platforms = {PLATFORM_WINDOWS: 'W', PLATFORM_XBOX: 'X', PLATFORM_MOBILE: 'M'}
    versions = {VERSION_30: '30', VERSION_31: '31', VERSION_40: '40'}
    profiles = {PROFILE_REACH: 'r', PROFILE_HIDEF: 'h'}

    _profile_mask = 0x7f
    _compress_mask = 0x80

    _header = '3s c B B I'

    def __init__(self, data, file_platform, file_version, graphics_profile, compressed):
        self.data = data
        self.file_platform = file_platform
        self.file_version = file_version
        self.graphics_profile = graphics_profile
        self.compressed = compressed

    @classmethod
    def read(cls, data):
        stream = BinaryReader(data, False)
        (sig, platform, version, attribs, size) = stream.unpack(cls._header)
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
            size -= stream.calc_size(cls._header)
        if compressed:
            uncomp = stream.read('u4')
            size -= stream.size('u4')
            content_comp = stream.pull(size)
            content = decompress(content_comp, uncomp)
        else:
            content = stream.pull(size)
        return cls(content, platform, version, profile, compressed)

    def write(self, compress=False):
        stream = BinaryWriter(False)
        attribs = 0
        if self.file_platform not in self.platforms:
            raise ValueError('bad platform: %s' % repr(self.file_platform))
        if self.file_version not in self.versions:
            raise ValueError('bad version: %s' % repr(self.file_version))
        if self.file_version >= VERSION_40:
            if self.graphics_profile not in self.profiles:
                raise ValueError('bad profile: %s' % repr(self.graphics_profile))
            attribs |= self.graphics_profile & self._profile_mask
        do_compress = False
        if self.file_version >= VERSION_30:
            if compress:
                do_compress = True
                attribs |= self._compress_mask
        if do_compress:
            raise ValueError('Recompression not supported')
        else:
            data = self.data
            size = len(data) + stream.calc_size(self._header)
        stream.pack(self._header, XNB_SIGNATURE, self.file_platform, self.file_version, attribs, size)
        stream.extend(data)
        return stream.serial()

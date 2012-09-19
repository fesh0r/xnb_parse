"""
load and manage type readers
.net type parser
"""

import re


class TypeReaderManager(object):
    def __init__(self, reader_dir=None):
        self.reader_dir = reader_dir
        self.type_readers = {}

    def get_type(self, name, version):
        name = self.strip_assembly_version(name)
        return BaseTypeReader(name, version)

    @staticmethod
    def strip_assembly_version(name):
        type_spec = TypeSpec.parse(name)
        return type_spec.name


class BaseTypeReader(object):
    def __init__(self, name, version):
        self.stream = None
        self.name = name
        self.version = version

    def __str__(self):
        return self.name


def _skip_space(name, pos):
    p = pos
    while p < len(name) and name[p].isspace():
        p += 1
    return p


_ESCAPE_RE = re.compile(r'([,+&*\[\]\\])')
_UNESCAPE_RE = re.compile(r'\\([,+&*\[\]\\])')


def _name_escape(name):
    return _ESCAPE_RE.sub(r'\\\1', name)


def _name_unescape(name):
    return _UNESCAPE_RE.sub(r'\1', name)


class TypeSpec(object):
    def __init__(self):
        self.name = None
        self.assembly_name = None
        self.nested = None
        self.generic_params = None
        self.array_spec = None
        self.pointer_level = 0
        self.is_byref = False

    def __str__(self):
        return self.name

    @property
    def is_array(self):
        return self.array_spec is not None

    @staticmethod
    def parse(type_name):
        if type_name is None:
            raise ValueError('type_name')
        res, pos = TypeSpec._parse(type_name)
        if pos < len(type_name):
            raise ValueError("Could not parse the whole type name: %d < %d" % (pos, len(type_name)))
        return res

    def add_name(self, type_name):
        if self.name is None:
            self.name = type_name
        else:
            if self.nested is None:
                self.nested = []
            self.nested.append(type_name)

    def add_array(self, dimensions, bound):
        if self.array_spec is None:
            self.array_spec = []
        self.array_spec.append((dimensions, bound))

    @staticmethod
    def _parse(name, pos=0, is_recurse=False, allow_aqn=False):
        print 'parse:', name[pos:], pos, is_recurse, allow_aqn
        in_modifiers = False
        data = TypeSpec()
        pos = _skip_space(name, pos)
        name_start = pos
        while pos < len(name):
            if name[pos] == '\\':
                # skip escaped char
                pos += 1
                if pos >= len(name):
                    raise ValueError("Fell off end of name after backslash")
            elif name[pos] == '+':
                data.add_name(name[name_start:pos])
                name_start = pos + 1
            elif name[pos] == ',' or name[pos] == ']':
                data.add_name(name[name_start:pos])
                name_start = pos + 1
                in_modifiers = True
                if is_recurse and not allow_aqn:
                    return data, pos
            elif name[pos] == '&' or name[pos] == '*' or name[pos] == '[':
                if name[pos] != '[' and is_recurse:
                    raise ValueError("Generic argument can't be byref or pointer type")
                data.add_name(name[name_start:pos])
                name_start = pos + 1
                in_modifiers = True
            if in_modifiers:
                break
            pos += 1
        if name_start < pos:
            data.add_name(name[name_start:pos])
        if in_modifiers:
            while pos < len(name):
                if name[pos] == '\\':
                    # skip escaped char
                    pos += 1
                    if pos >= len(name):
                        raise ValueError("Fell off end of name after backslash")
                elif name[pos] == '&':
                    if data.is_byref:
                        raise ValueError("Can't have a byref of a byref")
                    data.is_byref = True
                    break
                elif name[pos] == '*':
                    if data.is_byref:
                        raise ValueError("Can't have a pointer to a byref type")
                    data.pointer_level += 1
                    break
                elif name[pos] == ',':
                    if is_recurse:
                        end = pos
                        while end < len(name) and name[end] != ']':
                            end += 1
                        if end >= len(name):
                            raise ValueError("Unmatched ']' while parsing generic argument assembly name")
                        data.assembly_name = name[pos + 1:end].strip()
                        pos = end + 1
                        return data, pos
                    data.assembly_name = name[pos + 1:].strip()
                    pos = len(name)
                    break
                elif name[pos] == '[':
                    if data.is_byref:
                        raise ValueError("Byref qualifier must be the last one of a type")
                    pos += 1
                    if pos >= len(name):
                        raise ValueError("Invalid array/generic spec")
                    pos = _skip_space(name, pos)
                    if name[pos] != ',' and name[pos] != '*' and name[pos] != ']':
                        # generic args
                        if data.is_array:
                            raise ValueError("generic args after array spec")
                        args = []
                        while pos < len(name):
                            pos = _skip_space(name, pos)
                            aqn = name[pos] == '['
                            if aqn:
                                pos += 1
                            new_type, pos = TypeSpec._parse(name, pos, True, aqn)
                            args.append(new_type)
                            if pos >= len(name):
                                raise ValueError("Invalid generic arguments spec")
                            if name[pos] == ']':
                                break
                            if name[pos] == ',':
                                pos += 1
                            else:
                                raise ValueError("Invalid generic arguments separator '%s'" % name[pos])
                        if pos >= len(name) or name[pos] != ']':
                            raise ValueError("Error parsing generic params spec")
                        data.generic_params = args
                    else:
                        # array spec
                        dimensions = 1
                        bound = False
                        while pos < len(name) and name[pos] != ']':
                            if name[pos] == '*':
                                if bound:
                                    raise ValueError("Array spec cannot have 2 bound dimensions")
                                bound = True
                            elif name[pos] != ',':
                                raise ValueError("Invalid character in array spec '%s'" % name[pos])
                            else:
                                dimensions += 1
                            pos += 1
                            pos = _skip_space(name, pos)
                        if name[pos] != ']':
                            raise ValueError("Error parsing array spec")
                        if dimensions > 1 and bound:
                            raise ValueError("Invalid array spec, multi-dimensional array cannot be bound")
                        data.add_array(dimensions, bound)
                elif name[pos] == ']':
                    if is_recurse:
                        pos += 1
                        return data, pos
                    raise ValueError("Unmatched ]")
                else:
                    raise ValueError("Bad type def, can't handle '%s' at %d" % (name[pos], pos))
                pos += 1
        return data, pos

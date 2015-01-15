"""
.net type parser
"""

from __future__ import print_function

import re
from collections import namedtuple


class Error(Exception):
    pass


class TypeSpecError(Error):
    pass


def _skip_space(name, start_pos):
    cur_pos = start_pos
    while cur_pos < len(name) and name[cur_pos].isspace():
        cur_pos += 1
    return cur_pos


_ESCAPE_RE = re.compile(r'([,+&*\[\]\\])')
_UNESCAPE_RE = re.compile(r'\\([,+&*\[\]\\])')


def _name_escape(name):
    return _ESCAPE_RE.sub(r'\\\1', name)


def _name_unescape(name):
    return _UNESCAPE_RE.sub(r'\1', name)


ArraySpec = namedtuple('ArraySpec', ['dimensions', 'bound'])

_CACHED_TYPES = {}


class TypeSpec(object):
    def __init__(self, complete_name):
        self.complete_name = complete_name
        self.name = None
        self.assembly_name = None
        self.nested = None
        self.generic_params = None
        self.array_spec = None
        self.pointer_level = 0
        self.is_byref = False

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        return self.name + self.suffix

    @property
    def suffix(self):
        name = ''
        if self.nested:
            name += '+' + '+'.join(self.nested)
        if self.generic_params:
            name += '[' + ','.join([part.full_name for part in self.generic_params]) + ']'
        if self.array_spec:
            for cur_index in self.array_spec:
                if cur_index.bound:
                    part = '*'
                else:
                    part = ',' * (cur_index.dimensions - 1)
                name += '[' + part + ']'
        if self.pointer_level:
            name += '*' * self.pointer_level
        if self.is_byref:
            name += '&'
        return name

    @property
    def is_generic(self):
        return self.generic_params is not None

    @property
    def is_array(self):
        return self.array_spec is not None

    @staticmethod
    def parse(type_name):
        if not type_name:
            raise TypeSpecError("type_name empty")
        if type_name in _CACHED_TYPES:
            return _CACHED_TYPES[type_name]
        res, pos = TypeSpec._parse(type_name)
        if pos < len(type_name):
            raise TypeSpecError("Could not parse the whole type name: {} < {}".format(pos, len(type_name)))
        _CACHED_TYPES[type_name] = res
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
        self.array_spec.append(ArraySpec(dimensions, bound))

    @staticmethod
    def _parse(name, pos=0, is_recurse=False, allow_aqn=False):
        in_modifiers = False
        data = TypeSpec(name)
        pos = _skip_space(name, pos)
        name_start = pos
        while pos < len(name):
            if name[pos] == '\\':
                # skip escaped char
                pos += 1
                if pos >= len(name):
                    raise TypeSpecError("Fell off end of name after backslash")
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
                    raise TypeSpecError("Generic argument can't be byref or pointer type")
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
                if name[pos] == '&':
                    if data.is_byref:
                        raise TypeSpecError("Can't have a byref of a byref")
                    data.is_byref = True
                elif name[pos] == '*':
                    if data.is_byref:
                        raise TypeSpecError("Can't have a pointer to a byref type")
                    data.pointer_level += 1
                elif name[pos] == ',':
                    if is_recurse:
                        end = pos
                        while end < len(name) and name[end] != ']':
                            end += 1
                        if end >= len(name):
                            raise TypeSpecError("Unmatched ']' while parsing generic argument assembly name")
                        data.assembly_name = name[pos + 1:end].strip()
                        pos = end + 1
                        return data, pos
                    data.assembly_name = name[pos + 1:].strip()
                    pos = len(name)
                    break
                elif name[pos] == '[':
                    if data.is_byref:
                        raise TypeSpecError("Byref qualifier must be the last one of a type")
                    pos += 1
                    if pos >= len(name):
                        raise TypeSpecError("Invalid array/generic spec")
                    pos = _skip_space(name, pos)
                    if name[pos] != ',' and name[pos] != '*' and name[pos] != ']':
                        # generic args
                        if data.is_array:
                            raise TypeSpecError("generic args after array spec")
                        args = []
                        while pos < len(name):
                            pos = _skip_space(name, pos)
                            aqn = name[pos] == '['
                            if aqn:
                                pos += 1
                            new_type, pos = TypeSpec._parse(name, pos, True, aqn)
                            args.append(new_type)
                            if pos >= len(name):
                                raise TypeSpecError("Invalid generic arguments spec")
                            if name[pos] == ']':
                                break
                            if name[pos] == ',':
                                pos += 1
                            else:
                                raise TypeSpecError("Invalid generic arguments separator: '{}'".format(name[pos]))
                        if pos >= len(name) or name[pos] != ']':
                            raise TypeSpecError("Error parsing generic params spec")
                        data.generic_params = args
                    else:
                        # array spec
                        dimensions = 1
                        bound = False
                        while pos < len(name) and name[pos] != ']':
                            if name[pos] == '*':
                                if bound:
                                    raise TypeSpecError("Array spec cannot have 2 bound dimensions")
                                bound = True
                            elif name[pos] != ',':
                                raise TypeSpecError("Invalid character in array spec: '{}'".format(name[pos]))
                            else:
                                dimensions += 1
                            pos += 1
                            pos = _skip_space(name, pos)
                        if name[pos] != ']':
                            raise TypeSpecError("Error parsing array spec")
                        if dimensions > 1 and bound:
                            raise TypeSpecError("Invalid array spec, multi-dimensional array cannot be bound")
                        data.add_array(dimensions, bound)
                elif name[pos] == ']':
                    if is_recurse:
                        pos += 1
                        return data, pos
                    raise TypeSpecError("Unmatched ]")
                else:
                    raise TypeSpecError("Bad type def, can't handle '{}' at {}".format(name[pos], pos))
                pos += 1
        if pos > len(name):
            raise TypeSpecError("Fell off end of name")
        return data, pos

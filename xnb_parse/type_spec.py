"""
.net type parser
"""

import re


class Error(Exception):
    pass


class TypeError(Error):
    pass


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
        return self.full_name

    @property
    def full_name(self):
        name = self.name
        if self.nested:
            name += '+' + '+'.join(self.nested)
        if self.generic_params:
            name += ','.join(['[' + n.full_name + ']' for n in self.generic_params])
        if self.array_spec:
            for i in self.array_spec:
                if i[1]:
                    n = '*'
                else:
                    n = ',' * (i[0] - 1)
                name += '[' + n + ']'
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
            raise TypeError('type_name empty')
        res, pos = TypeSpec._parse(type_name)
        if pos < len(type_name):
            raise TypeError("Could not parse the whole type name: %d < %d" % (pos, len(type_name)))
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
        in_modifiers = False
        data = TypeSpec()
        pos = _skip_space(name, pos)
        name_start = pos
        while pos < len(name):
            if name[pos] == '\\':
                # skip escaped char
                pos += 1
                if pos >= len(name):
                    raise TypeError("Fell off end of name after backslash")
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
                    raise TypeError("Generic argument can't be byref or pointer type")
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
                        raise TypeError("Can't have a byref of a byref")
                    data.is_byref = True
                elif name[pos] == '*':
                    if data.is_byref:
                        raise TypeError("Can't have a pointer to a byref type")
                    data.pointer_level += 1
                elif name[pos] == ',':
                    if is_recurse:
                        end = pos
                        while end < len(name) and name[end] != ']':
                            end += 1
                        if end >= len(name):
                            raise TypeError("Unmatched ']' while parsing generic argument assembly name")
                        data.assembly_name = name[pos + 1:end].strip()
                        pos = end + 1
                        return data, pos
                    data.assembly_name = name[pos + 1:].strip()
                    pos = len(name)
                    break
                elif name[pos] == '[':
                    if data.is_byref:
                        raise TypeError("Byref qualifier must be the last one of a type")
                    pos += 1
                    if pos >= len(name):
                        raise TypeError("Invalid array/generic spec")
                    pos = _skip_space(name, pos)
                    if name[pos] != ',' and name[pos] != '*' and name[pos] != ']':
                        # generic args
                        if data.is_array:
                            raise TypeError("generic args after array spec")
                        args = []
                        while pos < len(name):
                            pos = _skip_space(name, pos)
                            aqn = name[pos] == '['
                            if aqn:
                                pos += 1
                            new_type, pos = TypeSpec._parse(name, pos, True, aqn)
                            args.append(new_type)
                            if pos >= len(name):
                                raise TypeError("Invalid generic arguments spec")
                            if name[pos] == ']':
                                break
                            if name[pos] == ',':
                                pos += 1
                            else:
                                raise TypeError("Invalid generic arguments separator '%s'" % name[pos])
                        if pos >= len(name) or name[pos] != ']':
                            raise TypeError("Error parsing generic params spec")
                        data.generic_params = args
                    else:
                        # array spec
                        dimensions = 1
                        bound = False
                        while pos < len(name) and name[pos] != ']':
                            if name[pos] == '*':
                                if bound:
                                    raise TypeError("Array spec cannot have 2 bound dimensions")
                                bound = True
                            elif name[pos] != ',':
                                raise TypeError("Invalid character in array spec '%s'" % name[pos])
                            else:
                                dimensions += 1
                            pos += 1
                            pos = _skip_space(name, pos)
                        if name[pos] != ']':
                            raise TypeError("Error parsing array spec")
                        if dimensions > 1 and bound:
                            raise TypeError("Invalid array spec, multi-dimensional array cannot be bound")
                        data.add_array(dimensions, bound)
                elif name[pos] == ']':
                    if is_recurse:
                        pos += 1
                        return data, pos
                    raise TypeError("Unmatched ]")
                else:
                    raise TypeError("Bad type def, can't handle '%s' at %d" % (name[pos], pos))
                pos += 1
        if pos > len(name):
            raise TypeError("Fell off end of name")
        return data, pos

"""
mercury particle engine basic types
"""

from __future__ import print_function

from collections import namedtuple

from xnb_parse.xna_types.xna_primitive import Enum


_VariableFloat = namedtuple('VariableFlat', ['value', 'variation'])


class VariableFloat(_VariableFloat):
    __slots__ = ()


_VariableFloat3 = namedtuple('VariableFloat3', ['value', 'variation'])


class VariableFloat3(_VariableFloat3):
    __slots__ = ()


class BlendMode(Enum):
    __slots__ = ()
    enum_values = dict(enumerate(['Add', 'Alpha', 'Subtract', 'Multiply', 'None']))

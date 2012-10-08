"""
primitive types
"""


class Enum(object):
    __slots__ = ('_value', '_name')
    enum_values = None

    def __init__(self, value):
        self._value = value
        self._name = self.enum_values[value]

    @property
    def value(self):
        return self._value

    @property
    def name(self):
        return self._name

    def __str__(self):
        return self._name

    def __repr__(self):
        return '%s(%d)' % (self.__class__.__name__, self._value)

"""
primitive types
"""

from xnb_parse.file_formats.xml_utils import E


class Enum(object):
    enum_values = None
    xml_tag = None

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

    def xml(self):
        xml_tag = self.xml_tag if self.xml_tag else self.__class__.__name__
        return E(xml_tag, self._name)

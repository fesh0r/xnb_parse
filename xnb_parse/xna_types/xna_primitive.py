"""
primitive types
"""

from __future__ import print_function

from xnb_parse.file_formats.xml_utils import ET


class Enum(object):
    __slots__ = ('_value', '_name')
    enum_values = None
    xml_tag = None

    def __init__(self, value):
        self._value = value
        self._name = None
        if value is not None:
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
        return '{}({})'.format(self.__class__.__name__, self._value)

    def xml(self, parent):
        xml_tag = self.xml_tag if self.xml_tag else self.__class__.__name__
        root = ET.SubElement(parent, xml_tag)
        root.text = self._name
        return root

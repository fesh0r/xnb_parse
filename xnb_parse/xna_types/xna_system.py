# coding=utf-8
"""
system types
"""

from __future__ import absolute_import, division, unicode_literals, print_function

from xnb_parse.file_formats.xml_utils import E
from xnb_parse.xna_types.xna_primitive import Enum


class XNAList(list):
    __slots__ = ()

    def xml(self, xml_tag='List', xml_entry='Entry', attrib=None):
        root = E(xml_tag)
        for cur_value in self:
            if hasattr(cur_value, 'xml'):
                cur_tag = cur_value.xml()
            elif attrib:
                cur_tag = E(xml_entry)
                cur_tag.set(attrib, unicode(cur_value))
            else:
                cur_tag = E(xml_entry, unicode(cur_value))
            root.append(cur_tag)
        return root


class XNADict(dict):
    __slots__ = ()

    def xml(self, xml_tag='Dict', xml_entry='Entry', attrib=None):
        root = E(xml_tag)
        for cur_key, cur_value in self.items():
            cur_tag = E(xml_entry)
            if hasattr(cur_key, 'xml') and not isinstance(cur_key, Enum):
                cur_tag.append(cur_key.xml())
            else:
                cur_tag.set('key', unicode(cur_key))
            if hasattr(cur_value, 'xml'):
                cur_tag.append(cur_value.xml())
            elif attrib:
                cur_tag.set(attrib, unicode(cur_value))
            else:
                cur_tag.text = unicode(cur_value)
            root.append(cur_tag)
        return root


class XNASet(XNAList):
    __slots__ = ()

    def xml(self, xml_tag='Set', xml_entry='Entry', attrib=None):
        root = XNAList.xml(self, xml_tag=xml_tag, xml_entry=xml_entry, attrib=attrib)
        return root


class ExternalReference(object):
    def __init__(self, filename, expected_type):
        self.filename = filename
        self.expected_type = expected_type

    def __str__(self):
        return "ExternalReference '{}'".format(self.filename)

    def xml(self):
        root = E.ExternalReference(filename=self.filename)
        if self.expected_type is not None:
            root.set('expectedType', self.expected_type.target_type)
        return root

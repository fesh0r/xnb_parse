"""
system types
"""

from __future__ import print_function

import sys
from collections import OrderedDict

from xnb_parse.file_formats.xml_utils import ET
from xnb_parse.xna_types.xna_primitive import Enum


class XNAList(list):
    __slots__ = ()

    def xml(self, parent=None, xml_tag='List', xml_entry='Entry', attrib=None):
        if sys.version < '3':
            conv = unicode
        else:
            conv = str
        if parent is None:
            root = ET.Element(xml_tag)
        else:
            root = ET.SubElement(parent, xml_tag)
        for cur_value in self:
            if hasattr(cur_value, 'xml'):
                cur_value.xml(root)
            elif attrib is not None:
                cur_tag = ET.SubElement(root, xml_entry)
                cur_tag.set(attrib, conv(cur_value))
            else:
                cur_tag = ET.SubElement(root, xml_entry)
                cur_tag.text = conv(cur_value)
        return root


class XNADict(OrderedDict):
    __slots__ = ()

    def xml(self, parent=None, xml_tag='Dict', xml_entry='Entry', attrib=None):
        if sys.version < '3':
            conv = unicode
        else:
            conv = str
        if parent is None:
            root = ET.Element(xml_tag)
        else:
            root = ET.SubElement(parent, xml_tag)
        for cur_key, cur_value in self.items():
            cur_tag = ET.SubElement(root, xml_entry)
            if hasattr(cur_key, 'xml') and not isinstance(cur_key, Enum):
                cur_key.xml(cur_tag)
            else:
                cur_tag.set('key', conv(cur_key))
            if hasattr(cur_value, 'xml'):
                cur_value.xml(cur_tag)
            elif attrib is not None:
                cur_tag.set(attrib, conv(cur_value))
            else:
                cur_tag.text = conv(cur_value)
        return root


class XNASet(XNAList):
    __slots__ = ()

    def xml(self, parent=None, xml_tag='Set', xml_entry='Entry', attrib=None):
        root = XNAList.xml(self, parent=parent, xml_tag=xml_tag, xml_entry=xml_entry, attrib=attrib)
        return root


class ExternalReference(object):
    def __init__(self, filename, expected_type):
        self.filename = filename
        self.expected_type = expected_type

    def __str__(self):
        return "ExternalReference '{}'".format(self.filename)

    def xml(self, parent):
        root = ET.SubElement(parent, 'ExternalReference')
        root.set('filename', self.filename)
        if self.expected_type is not None:
            root.set('expectedType', self.expected_type.target_type)
        return root

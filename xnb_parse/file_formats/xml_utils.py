# coding=utf-8
"""
XML utils
"""

from __future__ import print_function

import lxml.etree as ET
from lxml.builder import ElementMaker


#noinspection PyUnresolvedReferences
def output_xml(xml, filename):
    ET.ElementTree(xml).write(filename, encoding='utf-8', xml_declaration=True, pretty_print=True)


# create factory object
E = ElementMaker()

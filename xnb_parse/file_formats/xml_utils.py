"""
XML utils
"""

import lxml.etree as ET
from lxml.builder import ElementMaker


# create factory object
E = ElementMaker()


def output_xml(xml, filename):
    ET.ElementTree(xml).write(filename, encoding='utf-8', xml_declaration=True, pretty_print=True)

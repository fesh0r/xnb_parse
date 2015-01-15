"""
XML utils
"""

from __future__ import print_function

try:
    import lxml.etree as ET

    def output_xml(xml, filename):
        ET.ElementTree(xml).write(filename, encoding='utf-8', xml_declaration=True, pretty_print=True)
except ImportError:
    import xml.etree.cElementTree as ET

    def output_xml(xml, filename):
        ET.ElementTree(xml).write(filename, encoding='utf-8')

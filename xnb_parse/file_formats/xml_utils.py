# coding=utf-8
"""
XML utils
"""

from __future__ import absolute_import, division, unicode_literals, print_function

try:
    import lxml.etree as ET
    from lxml.builder import ElementMaker

    def output_xml(xml, filename):
        ET.ElementTree(xml).write(filename, encoding='utf-8', xml_declaration=True, pretty_print=True)
except ImportError:
    import functools
    #noinspection PyRedeclaration
    import xml.etree.cElementTree as ET

    #noinspection PyRedeclaration
    class ElementMaker(object):
        def __call__(self, tag, *children, **attrib):
            elem = ET.Element(tag, attrib)
            for item in children:
                if isinstance(item, dict):
                    elem.attrib.update(item)
                elif isinstance(item, basestring):
                    if len(elem):
                        elem[-1].tail = (elem[-1].tail or "") + item
                    else:
                        elem.text = (elem.text or "") + item
                elif ET.iselement(item):
                    elem.append(item)
                else:
                    raise TypeError("bad argument: '{!r}".format(item))
            return elem

        def __getattr__(self, tag):
            return functools.partial(self, tag)

    def indent(elem, level=0):
        i = '\n' + '  ' * level
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + '  '
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                indent(elem, level + 1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i

    #noinspection PyRedeclaration
    def output_xml(xml, filename):
        indent(xml)
        ET.ElementTree(xml).write(filename, encoding='utf-8')


# create factory object
E = ElementMaker()

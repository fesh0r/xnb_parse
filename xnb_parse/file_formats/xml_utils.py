"""
XML utils
"""

import functools
import xml.etree.cElementTree as ET


class _E(object):
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
                raise TypeError("bad argument: %r" % item)
        return elem

    def __getattr__(self, tag):
        return functools.partial(self, tag)


# create factory object
E = _E()


def output_xml(xml, filename):
    ET.ElementTree(xml).write(filename, encoding='utf-8', xml_declaration=True)

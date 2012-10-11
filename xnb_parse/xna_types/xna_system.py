"""
system types
"""

from xnb_parse.file_formats.xml_utils import E


class XNAList(list):
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

    def export(self, _):
        return self.xml()


class XNADict(dict):
    def xml(self, xml_tag='Dict', xml_entry='Entry', attrib=None):
        root = E(xml_tag)
        for cur_key, cur_value in self.items():
            cur_tag = E(xml_entry)
            if hasattr(cur_key, 'xml'):
                raise ValueError("XNADict key is xml")
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

    def export(self, _):
        return self.xml()

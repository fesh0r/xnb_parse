"""
system types
"""

from xnb_parse.file_formats.xml_utils import E


class XNAList(list):
    def xml(self, xml_tag='List', xml_entry='Entry'):
        root = E(xml_tag)
        for cur_value in self:
            if hasattr(cur_value, 'xml'):
                root.append(cur_value.xml())
            else:
                root.append(E(xml_entry, unicode(cur_value)))
        return root

    def export(self, _):
        return self.xml()


class XNADict(dict):
    def xml(self, xml_tag='Dict', xml_entry='Entry'):
        root = E(xml_tag)
        for cur_key, cur_value in self.items():
            if hasattr(cur_value, 'xml'):
                root.append(E(xml_entry, cur_value.xml(), key=unicode(cur_key)))
            else:
                root.append(E(xml_entry, unicode(cur_value), key=unicode(cur_key)))
        return root

    def export(self, _):
        return self.xml()

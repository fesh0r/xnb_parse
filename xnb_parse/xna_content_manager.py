"""
XNA ContentManager
"""

from __future__ import print_function

import fnmatch
import os
from collections import OrderedDict

from xnb_parse.type_reader import ReaderError
from xnb_parse.xnb_reader import XNBReader
from xnb_parse.file_formats.xml_utils import output_xml


class ContentManager(object):
    content_extension = '.xnb'

    def __init__(self, root_dir):
        root_dir = os.path.normpath(root_dir)
        if not os.path.isdir(root_dir):
            raise ReaderError("Content root directory not found: '%s'" % root_dir)
        self.root_dir = root_dir
        self._asset_dict = OrderedDict()
        for k, v in self.find_assets():
            if k not in self._asset_dict:
                self._asset_dict[k] = v
        self.assets = self._asset_dict.keys()

    def xnb(self, asset_name, expected_type=None, parse=True):
        asset_name = asset_name.replace('\\', '/')
        asset_name = asset_name.lower()
        asset_filename = os.path.join(self.root_dir, self._asset_dict[asset_name])
        return XNBReader.load(filename=asset_filename, expected_type=expected_type, parse=parse)

    def load(self, asset_name, expected_type=None):
        return self.xnb(asset_name, expected_type).content

    def find_assets(self):
        for path, _, filelist in os.walk(self.root_dir, followlinks=True):
            sub_dir = os.path.relpath(path, self.root_dir)
            for asset_filename in fnmatch.filter(filelist, '*' + self.content_extension):
                if sub_dir != '.':
                    asset_filename = os.path.join(sub_dir, asset_filename)
                asset = asset_filename[:-len(self.content_extension)]
                asset = asset.replace(os.sep, '/')
                asset = asset.lower()
                yield asset, asset_filename

    def filter(self, search='*'):
        return fnmatch.filter(self.assets, search)

    @staticmethod
    def export(asset, asset_name, export_dir, export_file=True, export_xml=True):
        filename = os.path.join(export_dir, os.path.normpath(asset_name))
        dirname = os.path.dirname(filename)
        if not os.path.isdir(dirname):
            os.makedirs(dirname)
        if export_file and hasattr(asset, 'export'):
            asset.export(filename)
        if export_xml and hasattr(asset, 'xml'):
            output_xml(asset.xml(), filename + '.xml')

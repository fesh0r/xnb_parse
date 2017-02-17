"""
Fez ContentManager
"""

from __future__ import print_function

import os

from xnb_parse.identify import identify_buffer
from xnb_parse.xna_content_manager import ContentManager
from xnb_parse.xnb_reader import XNBReader
from xnb_parse.binstream import BinaryStream


class FezContentManager(ContentManager):
    content_pak_files = ['Essentials.pak', 'Updates.pak', 'Other.pak']

    def find_assets(self):
        for pak_file in self.content_pak_files:
            filename = os.path.join(self.root_dir, pak_file)
            if os.path.isfile(filename):
                stream = BinaryStream(filename=filename)
                capacity = stream.read_int32()
                for _ in range(capacity):
                    asset_name = stream.read_string()
                    asset_size = stream.read_int32()
                    asset_data = stream.read(asset_size)
                    asset_name = asset_name.replace('\\', '/')
                    asset_name = asset_name.lower()
                    yield asset_name, asset_data

    def xnb(self, asset_name, expected_type=None, parse=True):
        asset_name = asset_name.replace('\\', '/')
        asset_name = asset_name.lower()
        return XNBReader.load(data=self._asset_dict[asset_name], expected_type=expected_type, parse=parse)

    def save(self, asset_name, out_dir):
        asset_data = self._asset_dict[asset_name]
        extension = identify_buffer(asset_data)
        filename = os.path.join(out_dir, os.path.normpath(asset_name) + extension)
        dirname = os.path.dirname(filename)
        if not os.path.isdir(dirname):
            os.makedirs(dirname)
        with open(filename, 'wb') as out_file:
            out_file.write(asset_data)

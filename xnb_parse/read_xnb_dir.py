"""
Dump info from directory of XNBs
"""

from __future__ import print_function

import sys
import time

from xnb_parse.type_reader import ReaderError
from xnb_parse.xna_content_manager import ContentManager


def read_xnb_dir(content_dir, export_dir=None):
    content_manager = ContentManager(content_dir)
    for asset_name in content_manager.assets:
        print(asset_name)
        try:
            asset = content_manager.load(asset_name)
            if export_dir is not None:
                content_manager.export(asset, asset_name, export_dir)
        except (ReaderError, KeyError) as ex:
            print("FAILED: '{}' {}: {}".format(asset_name, type(ex).__name__, ex), file=sys.stderr)


def main():
    if 1 < len(sys.argv) <= 3:
        totaltime = time.time()
        content_dir = sys.argv[1]
        export_dir = None
        if len(sys.argv) > 2:
            export_dir = sys.argv[2]
        read_xnb_dir(content_dir, export_dir)
        print('> Done in {:.2f} seconds'.format(time.time() - totaltime))
    else:
        print('read_xnb_dir.py content_dir [export_dir]', file=sys.stderr)

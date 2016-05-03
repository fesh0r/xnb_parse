"""
Decompress XNB files.
Requires win32
"""

from __future__ import print_function

import sys
import time
import os

from xnb_parse.xna_content_manager import ContentManager


def read_xnb(in_dir, out_dir):
    content_manager = ContentManager(in_dir)
    out_dir = os.path.normpath(out_dir)
    for asset_name in content_manager.assets:
        print(asset_name)
        xnb = content_manager.xnb(asset_name, parse=False)
        out_file = os.path.join(out_dir, os.path.normpath(asset_name))
        xnb.save(filename=out_file)


def main():
    if len(sys.argv) == 3:
        totaltime = time.time()
        read_xnb(os.path.normpath(sys.argv[1]), os.path.normpath(sys.argv[2]))
        print('> Done in {:.2f} seconds'.format(time.time() - totaltime))
    else:
        print('xnb_decomp.py in_dir out_dir', file=sys.stderr)

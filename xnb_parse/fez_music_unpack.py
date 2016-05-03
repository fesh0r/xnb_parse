"""
Extract oggs from FEZ PC Music.pak file
"""

from __future__ import print_function

import sys
import os
import time

from xnb_parse.fez_music_content_manager import FezMusicContentManager


def unpack(content_dir, out_dir):
    content_manager = FezMusicContentManager(content_dir)
    out_dir = os.path.normpath(out_dir)
    for asset_name in content_manager.assets:
        print(asset_name)
        content_manager.save(asset_name, out_dir)


def main():
    if len(sys.argv) == 3:
        totaltime = time.time()
        unpack(os.path.normpath(sys.argv[1]), os.path.normpath(sys.argv[2]))
        print('> Done in {:.2f} seconds'.format(time.time() - totaltime))
    else:
        print('fez_music_unpack.py Content out_dir', file=sys.stderr)

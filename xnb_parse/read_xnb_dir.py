"""
Dump info from directory of XNBs
"""

from __future__ import print_function

import sys
import os
import time
import fnmatch

from xnb_parse.xnb_reader import XNBReader
from xnb_parse.type_reader import ReaderError


def read_xnb_dir(in_dir, out_dir=None):
    in_dir = os.path.normpath(in_dir)
    if out_dir is not None:
        out_dir = os.path.normpath(out_dir)
    for path, _, filelist in os.walk(in_dir, followlinks=True):
        sub_dir = os.path.relpath(path, in_dir)
        for cur_file in fnmatch.filter(filelist, '*.xnb'):
            short_name = os.path.join(sub_dir, cur_file)
            in_file = os.path.normpath(os.path.join(in_dir, short_name))
            out_file = None
            if out_dir is not None:
                out_file = os.path.normpath(os.path.join(out_dir, short_name).replace('.xnb', ''))
            print(in_file)
            try:
                xnb = XNBReader.load(filename=in_file)
                if out_file is not None:
                    xnb.export(out_file, export_xml=False)
            except ReaderError as ex:
                print("ReaderError in '{}'".format(short_name))
                print(ex)
            except Exception:
                print("Unexpected error in '{}'".format(short_name))
                raise


def main():
    if 1 < len(sys.argv) <= 3:
        totaltime = time.time()
        in_dir = sys.argv[1]
        out_dir = None
        if len(sys.argv) > 2:
            out_dir = sys.argv[2]
        read_xnb_dir(in_dir, out_dir)
        print('> Done in {:.2f} seconds'.format(time.time() - totaltime))
    else:
        print('read_xnb_dir.py content_dir [export_dir]')

# coding=utf-8
"""
Decompress XNB files.
Requires win32
"""

from __future__ import print_function

import sys
import time
import os
import fnmatch

from xnb_parse.xnb_reader import XNBReader


def read_xnb(in_dir, out_dir):
    for path, _, filelist in os.walk(in_dir, followlinks=True):
        sub_dir = os.path.relpath(path, in_dir)
        for cur_file in fnmatch.filter(filelist, '*.xnb'):
            in_file = os.path.normpath(os.path.join(in_dir, sub_dir, cur_file))
            out_file = os.path.normpath(os.path.join(out_dir, sub_dir, cur_file))
            if not os.path.isdir(os.path.dirname(out_file)):
                os.makedirs(os.path.dirname(out_file))

            print(in_file)
            with open(in_file, 'rb') as in_handle:
                in_data = in_handle.read()
            xnb = XNBReader.load(in_data, parse=False)
            out_data = xnb.save()
            with open(out_file, 'wb') as out_handle:
                out_handle.write(out_data)


def main():
    if len(sys.argv) == 3:
        totaltime = time.time()
        read_xnb(os.path.normpath(sys.argv[1]), os.path.normpath(sys.argv[2]))
        print('> Done in {:.2f} seconds'.format(time.time() - totaltime))
    else:
        print('xnb_decomp.py in_dir out_dir')

"""
Dump info from XNB
"""

from __future__ import print_function

import sys
import os
import time

from xnb_parse.xnb_reader import XNBReader


def read_xnb(in_file):
    in_file = os.path.normpath(in_file)
    print(in_file)
    xnb = XNBReader.load(filename=in_file, parse=False)
    print(xnb.parse())
    out_filebase = os.path.normpath(os.path.join('../export', in_file.replace('.xnb', '')))
    xnb.export(out_filebase)


def main():
    if len(sys.argv) > 1:
        totaltime = time.time()
        for filename in sys.argv[1:]:
            read_xnb(filename)
        print('> Done in {:.2f} seconds'.format(time.time() - totaltime))
    else:
        print('read_xnb.py file1.xnb ...', file=sys.stderr)

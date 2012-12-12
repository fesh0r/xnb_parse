"""
Dump info from XACT files
"""

from __future__ import print_function

import sys
import os
import time

from xnb_parse.xact.xsb import XSB
from xnb_parse.xact.xwb import XWB


def read_xact(in_xsb_file, in_xwb_file, out_dir=None):
    in_xsb_file = os.path.normpath(in_xsb_file)
    print(in_xsb_file)
    xsb = XSB(filename=in_xsb_file)
    in_xwb_file = os.path.normpath(in_xwb_file)
    print(in_xwb_file)
    xwb = XWB(filename=in_xwb_file)
    if out_dir is not None:
        xwb.export(out_dir)


def main():
    if 1 < len(sys.argv) <= 4:
        totaltime = time.time()
        in_xsb_file = sys.argv[1]
        in_xwb_file = sys.argv[2]
        out_dir = None
        if len(sys.argv) > 3:
            out_dir = sys.argv[3]
        read_xact(in_xsb_file, in_xwb_file, out_dir)
        print('> Done in {:.2f} seconds'.format(time.time() - totaltime))
    else:
        print('read_xact.py file.xsb file.xwb [export_dir]')

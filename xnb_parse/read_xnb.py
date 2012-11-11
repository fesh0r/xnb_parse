# coding=utf-8
"""
Dump info from XNB
"""

from __future__ import absolute_import

import sys
import os
import time

from xnb_parse.xnb_reader import XNBReader
from xnb_parse.type_reader_manager import TypeReaderManager


def read_xnb(in_file, type_reader_manager=None):
    in_file = os.path.normpath(in_file)
    print in_file
    with open(in_file, 'rb') as in_handle:
        in_data = in_handle.read()
    xnb = XNBReader.load(in_data, type_reader_manager, parse=False)
    print xnb.parse()
    out_filebase = os.path.normpath(os.path.join('../export', in_file.replace('.xnb', '')))
    xnb.export(out_filebase)


def main():
    if len(sys.argv) > 1:
        totaltime = time.time()
        type_reader_manager = TypeReaderManager()
        for filename in sys.argv[1:]:
            read_xnb(filename, type_reader_manager)
        print '> Done in %.2f seconds' % (time.time() - totaltime)
    else:
        print 'read_xnb.py file1.xnb ...'

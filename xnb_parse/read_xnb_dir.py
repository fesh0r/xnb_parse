"""
Dump info from directory of XNBs
"""

import sys
import os
import time
import fnmatch

from xnb_parse.xnb_reader import XNBReader
from xnb_parse.type_reader import ReaderError
from xnb_parse.type_reader_manager import TypeReaderManager


def read_xnb(in_dir, type_reader_manager=None):
    for path, _, filelist in os.walk(in_dir, followlinks=True):
        sub_dir = os.path.relpath(path, in_dir)
        for cur_file in fnmatch.filter(filelist, '*.xnb'):
            in_file = os.path.normpath(os.path.join(in_dir, sub_dir, cur_file))

            print in_file,
            with open(in_file, 'rb') as in_handle:
                in_data = in_handle.read()
            xnb = XNBReader.load(in_data, type_reader_manager, parse=False)
            print xnb,
            try:
                print xnb.parse(),
                xnb.export(os.path.join('../export', in_file.replace('.xnb', '')))
                print 'done'
            except ReaderError as ex:
                print "Error in '%s'" % in_file
                print ex


def main():
    if len(sys.argv) > 1:
        totaltime = time.time()
        type_reader_manager = TypeReaderManager()
        for filename in sys.argv[1:]:
            read_xnb(os.path.normpath(filename), type_reader_manager)
        print '> Done in %.2f seconds' % (time.time() - totaltime)
    else:
        print 'read_xnb.py file1.xnb ...'

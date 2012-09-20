"""
Decompress XNB files.
Requires win32
"""

import sys
import time
import os
import fnmatch

from xnb_parse.xnb import XNB


def read_xnb(in_dir, out_dir):
    for path, _, filelist in os.walk(in_dir, followlinks=True):
        sub_dir = os.path.relpath(path, in_dir)
        for cur_file in fnmatch.filter(filelist, '*.xnb'):
            in_file = os.path.normpath(os.path.join(in_dir, sub_dir, cur_file))
            out_file = os.path.normpath(os.path.join(out_dir, sub_dir, cur_file))
            if not os.path.isdir(os.path.dirname(out_file)):
                os.makedirs(os.path.dirname(out_file))

#            print 'Reading %s' % in_file
            with open(in_file, 'rb') as f:
                d = f.read()
            xnb = XNB.read(d)
#            print 'Writing %s' % out_file
            out = xnb.write()
            with open(out_file, 'wb') as f:
                f.write(out)


def main():
    if len(sys.argv) == 3:
        totaltime = time.time()
        read_xnb(os.path.normpath(sys.argv[1]), os.path.normpath(sys.argv[2]))
        print '> Done in %.2f seconds' % (time.time() - totaltime)
    else:
        print 'xnb_decomp.py in_dir out_dir'

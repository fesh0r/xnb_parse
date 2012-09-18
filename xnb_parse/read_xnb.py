#!/usr/bin/python
"""
Dump info from XNB
"""

import sys
import time

from xnb import XNB


def read_xnb(filename):
    print 'Reading %s' % filename
    with open(filename, 'rb') as f:
        d = f.read()
    xnb = XNB.read(d)
    print xnb


def main():
    if len(sys.argv) > 1:
        totaltime = time.time()
        for filename in sys.argv[1:]:
            read_xnb(filename)
        print '> Done in %.2f seconds' % (time.time() - totaltime)
    else:
        print 'read_xnb.py file1.xnb ...'


if __name__ == '__main__':
    main()

#!/usr/bin/python
"""
Dump info from XNB
"""

import sys

from xnb import XNB


def read_xnb(filename):
    print 'Reading %s' % filename
    with open(filename, 'rb') as f:
        d = f.read()

    print 'Parsing %s' % filename
    xnb = XNB.read(d)
    print xnb


def main():
    if len(sys.argv) > 1:
        for filename in sys.argv[1:]:
            read_xnb(filename)
    else:
        print 'No file specified, giving up'


if __name__ == '__main__':
    main()

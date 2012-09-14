#!/usr/bin/python
"""
Dump info from XNB
"""

import argparse
import os

from xnb import XNB


def read_xnb(filename):
    print 'Reading %s' % filename
    with open(filename, 'rb') as f:
        d = f.read()

    print 'Parsing %s' % filename
    xnb = XNB.read(d)
    print xnb


def main():
    parser = argparse.ArgumentParser(description='Dump XNB file')
    parser.add_argument('xnb_file', help='xnb file')
    args = parser.parse_args()
    read_xnb(args.xnb_file)


if __name__ == '__main__':
    main()

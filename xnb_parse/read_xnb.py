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

    print 'Parsing %s' % filename
    xnb = XNB.read(d)

    filename2 = 'out_' + filename

    print 'Building %s' % filename2
    out = xnb.write()

    print 'Writing %s' % filename2
    with open(filename2, 'wb') as f:
        f.write(out)


def main():
    if len(sys.argv) > 1:
        totaltime = time.time()
        for filename in sys.argv[1:]:
            read_xnb(filename)
        print '> Done in %.2f seconds' % (time.time() - totaltime)
    else:
        print 'No file specified, giving up'


if __name__ == '__main__':
    main()

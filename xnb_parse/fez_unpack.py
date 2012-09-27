"""
Extract FEZ .pak files
"""

import sys
import os
import time

from xnb_parse.binstream import BinaryReader


def unpack(in_file, out_dir):
    with open(in_file, 'rb') as in_handle:
        in_data = in_handle.read()
    stream = BinaryReader(in_data)
    capacity = stream.read('u4')
    for _ in range(capacity):
        filename = stream.read('str')
        filesize = stream.read('u4')
        filedata = stream.pull(filesize)
        print '"%s" : %d' % (filename, filesize)
        filename = os.path.normpath(filename + '.xnb')
        filename = os.path.join(out_dir, filename)
        filedir = os.path.dirname(filename)
        if filedir:
            if not os.path.isdir(filedir):
                os.makedirs(filedir)
        with open(filename, 'wb') as out_file:
            out_file.write(filedata)


def main():
    if len(sys.argv) == 3:
        totaltime = time.time()
        unpack(os.path.normpath(sys.argv[1]), os.path.normpath(sys.argv[2]))
        print '> Done in %.2f seconds' % (time.time() - totaltime)
    else:
        print 'fez_unpack.py in.pak out_dir'

# coding=utf-8
"""
Extract FEZ .pak files
"""

import sys
import os
import time

from xnb_parse.binstream import BinaryStream


def unpack(in_file, out_dir):
    stream = BinaryStream(filename=in_file)
    capacity = stream.read_int32()
    for _ in range(capacity):
        filename = stream.read_string()
        size = stream.read_int32()
        data = stream.read(size)
        print(filename)
        filename = filename.replace('\\', os.sep)
        filename = os.path.normpath(filename + '.xnb')
        filename = os.path.join(out_dir, filename)
        filedir = os.path.dirname(filename)
        if filedir:
            if not os.path.isdir(filedir):
                os.makedirs(filedir)
        with open(filename, 'wb') as out_file:
            out_file.write(data)


def main():
    if len(sys.argv) == 3:
        totaltime = time.time()
        unpack(os.path.normpath(sys.argv[1]), os.path.normpath(sys.argv[2]))
        print('> Done in {:.2f} seconds'.format(time.time() - totaltime))
    else:
        print('fez_unpack.py in.pak out_dir')

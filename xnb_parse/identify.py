"""
Identify file data based on content
"""

from __future__ import print_function

import os
import time
import sys


def identify_buffer(data):
    if data[:3] == b'XNB':
        return '.xnb'
    elif data[:4] == b'OggS':
        return '.ogg'
    elif data[:4] == b'XGSF' or data[:4] == b'FSGX':
        return '.xgs'
    elif data[:4] == b'SDBK' or data[:4] == b'KBDS':
        return '.xsb'
    elif data[:4] == b'WBND' or data[:4] == b'DNBW':
        return '.xwb'
    elif data[2:4] == b'\xff\xfe' or data[:2] == b'\xfe\xff':
        return '.fxo'
    return '.bin'


def identify_file(filename):
    with open(filename, 'rb') as file_handle:
        data = file_handle.read()
    return identify_buffer(data)


def main():
    if len(sys.argv) == 2:
        totaltime = time.time()
        ext = identify_file(os.path.normpath(sys.argv[1]))
        print('{} {}'.format(sys.argv[1], ext))
        print('> Done in {:.2f} seconds'.format(time.time() - totaltime))
    else:
        print('identify.py filename', file=sys.stderr)

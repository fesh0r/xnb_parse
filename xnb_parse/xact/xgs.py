"""
parse XGS files
"""

from __future__ import print_function
from collections import OrderedDict

from xnb_parse.type_reader import ReaderError
from xnb_parse.xact.xwb import filetime_to_datetime
from xnb_parse.binstream import BinaryStream


XGS_L_SIGNATURE = b'XGSF'
XGS_B_SIGNATURE = b'FSGX'


class XGS(object):
    def __init__(self, data=None, filename=None):
        # open in little endian initially
        stream = BinaryStream(data=data, filename=filename)
        del data

        # check sig to find actual endianess
        h_sig = stream.peek(len(XGS_L_SIGNATURE))
        if h_sig == XGS_L_SIGNATURE:
            big_endian = False
        elif h_sig == XGS_B_SIGNATURE:
            big_endian = True
        else:
            raise ValueError("bad sig: {!r}".format(h_sig))

        # switch stream to correct endianess
        stream.set_endian(big_endian)

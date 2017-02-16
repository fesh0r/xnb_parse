"""
wrapper for native XNA functions
Requires win32
"""

from __future__ import print_function

from contextlib import contextmanager

import os
import platform
import sys
import ctypes


_XNA_VERSIONS = ['v4.0', 'v3.1', 'v3.0']
_DLL_NAME = 'XnaNative.dll'

_native_dir = None


def _find_native():
    global _native_dir
    if _native_dir:
        return _native_dir

    if not sys.platform == 'win32' or not platform.architecture()[0] == '32bit':
        raise IOError("win32 required for decompression")
    try:
        import winreg
    except ImportError:
        import _winreg as winreg

    native_path = None
    for ver in _XNA_VERSIONS:
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 'SOFTWARE\\Microsoft\\XNA\\Framework\\' + ver)
            lib_path, _ = winreg.QueryValueEx(key, 'NativeLibraryPath')
            if lib_path:
                lib_path = os.path.join(os.path.normpath(str(lib_path)), _DLL_NAME)
                if os.path.isfile(lib_path):
                    native_path = lib_path
                    break
        except WindowsError:
            pass
    if native_path is None:
        # TODO: must be a better way of doing this
        lib_path = os.path.realpath(os.path.join(os.path.dirname(__file__), '../bin'))
        lib_path = os.path.join(os.path.normpath(lib_path), _DLL_NAME)
        if os.path.isfile(lib_path):
            native_path = lib_path
    if native_path is None:
        raise IOError("{} not found".format(_DLL_NAME))
    _native_dir = native_path
    return native_path


@contextmanager
def decomp_context(dll):
    ctx = dll.CreateDecompressionContext()
    if ctx is None:
        raise IOError("CreateDecompressionContext failed")
    yield ctx
    dll.DestroyDecompressionContext(ctx)


def decompress(in_buf, out_size):
    dll = ctypes.CDLL(_find_native())

    with decomp_context(dll) as ctx:
        in_size = len(in_buf)
        compressed_position = 0
        compressed_todo = in_size
        decompressed_position = 0
        decompressed_todo = out_size

        s_in_buf = ctypes.create_string_buffer(in_buf, in_size)
        s_out_buf = ctypes.create_string_buffer(out_size)

        while decompressed_todo > 0 and compressed_todo > 0:
            compressed_size = in_size - compressed_position
            decompressed_size = out_size - decompressed_position

            s_compressed_size = ctypes.c_uint(compressed_size)
            s_decompressed_size = ctypes.c_uint(decompressed_size)
            err = dll.Decompress(ctx, ctypes.byref(s_out_buf, decompressed_position), ctypes.byref(s_decompressed_size),
                                 ctypes.byref(s_in_buf, compressed_position), ctypes.byref(s_compressed_size))
            r_compressed_size = int(s_compressed_size.value)
            r_decompressed_size = int(s_decompressed_size.value)

            if err:
                raise IOError("Decompress failed: {}".format(err))
            if r_compressed_size == 0 and r_decompressed_size == 0:
                raise IOError("Decompress failed")

            compressed_position += r_compressed_size
            decompressed_position += r_decompressed_size
            compressed_todo -= r_compressed_size
            decompressed_todo -= r_decompressed_size
    return s_out_buf.raw


def main():
    _find_native()

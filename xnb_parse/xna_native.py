"""
wrapper for native XNA functions
"""

import os
import platform
import sys
import ctypes


_XNA_VERSIONS = ['v4.0', 'v3.1', 'v3.0']
_DLL_NAME = 'XnaNative.dll'


def _find_native():
    if not sys.platform == 'win32' or not platform.architecture()[0] == '32bit':
        raise IOError("win32 required for decompression")
    import _winreg

    native_path = None
    for ver in _XNA_VERSIONS:
        try:
            key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, 'SOFTWARE\\Microsoft\\XNA\\Framework\\' + ver)
            lib_path, _ = _winreg.QueryValueEx(key, 'NativeLibraryPath')
            if lib_path:
                lib_path = os.path.join(os.path.normpath(lib_path), _DLL_NAME)
                if os.path.isfile(lib_path):
                    native_path = lib_path
                    break
        except WindowsError:
            pass
    if native_path is None:
        raise IOError("%s not found" % _DLL_NAME)
    return native_path


def decompress(in_buf, out_size):
    dll = ctypes.CDLL(_find_native())
    ctx = dll.CreateDecompressionContext()
    if ctx is None:
        raise IOError("CreateDecompressionContext failed")

    in_size = len(in_buf)
    compressed_position = 0
    compressed_todo = in_size
    decompressed_position = 0
    decompressed_todo = out_size

    s_in_buf = ctypes.create_string_buffer(in_buf)
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
            raise IOError("Decompress failed: %d" % err)
        if r_compressed_size == 0 and r_decompressed_size == 0:
            raise IOError("Decompress failed")

        compressed_position += r_compressed_size
        decompressed_position += r_decompressed_size
        compressed_todo -= r_compressed_size
        decompressed_todo -= r_decompressed_size
    dll.DestroyDecompressionContext(ctx)
    return s_out_buf.raw

"""
wrapper for native XNA functions
"""

import os
import sys
import ctypes


_XNA_VERSIONS = ['v4.0', 'v3.1', 'v3.0']
_DLL_NAME = 'XnaNative.dll'
_BUF_SIZE = 0x10000


class XnaNative(object):
    __instance = None
    __single = False

    def __init__(self):
        if not sys.platform.startswith('win'):
            raise IOError('win32 required for decompression')
        if self.__single:
            return
        self.__single = True
        native_path = self.find_native()
        dll = ctypes.CDLL(native_path)
        dll.CreateDecompressionContext.restype = ctypes.c_void_p
        dll.CreateDecompressionContext.argtypes = ()
        dll.DestroyDecompressionContext.restype = None
        dll.DestroyDecompressionContext.argtypes = (ctypes.c_void_p,)
        dll.Decompress.restype = ctypes.c_int
        dll.Decompress.argtypes = (ctypes.c_void_p, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_uint),
                                   ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_uint))
        dll.CreateCompressionContext.restype = ctypes.c_void_p
        dll.CreateCompressionContext.argtypes = ()
        dll.DestroyCompressionContext.restype = None
        dll.DestroyCompressionContext.argtypes = (ctypes.c_void_p,)
        dll.Compress.restype = ctypes.c_int
        dll.Compress.argtypes = (ctypes.c_void_p, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_uint),
                                 ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_uint))
        self.dll = dll

    # yay singletons
    def __new__(cls):
        if not cls.__instance:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    @staticmethod
    def find_native():
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
            raise IOError('XnaNative.dll not found')
        return native_path


def decompress(in_buf, out_size):
    dll = XnaNative().dll
    ctx = dll.CreateDecompressionContext()
    if ctx is None:
        raise IOError('CreateDecompressionContext failed')
    in_size = len(in_buf)
    s_in_size = ctypes.c_uint(in_size)
    s_out_size = ctypes.c_uint(out_size)
    s_out_buf = ctypes.create_string_buffer(out_size)
    err = dll.Decompress(ctx, s_out_buf, s_out_size, in_buf, s_in_size)
    if err:
        raise IOError('Decompress failed: %d' % err)
    r_in_size = int(s_in_size.value)
    r_out_size = int(s_out_size.value)
    if out_size != r_out_size:
        raise IOError('Decompress out size: %d != %d' % (r_out_size, out_size))
    if in_size != r_in_size:
        raise IOError('Decompress in size: %d != %d' % (r_in_size, out_size))
    dll.DestroyDecompressionContext(ctx)
    return s_out_buf.raw

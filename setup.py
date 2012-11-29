from cx_Freeze import setup, Executable

setup(
    name='xnb_parse',
    url='http://fesh.geek.nz/rc/xnb_parse',
    version='0.8',
    description='XNB Parser',
    author='Andrew McRae',
    author_email='xnb_parse@fesh.geek.nz',
    packages=[
        'xnb_parse',
        'xnb_parse.type_readers',
        'xnb_parse.type_readers.fez',
        'xnb_parse.xna_types',
        'xnb_parse.xna_types.fez',
        'xnb_parse.file_formats',
        'xnb_parse.xact',
    ],
    requires=['cx_Freeze', 'lxml', 'pyglet'],
    options={
        'build_exe': {
            'optimize': 1,
            'compressed': True,
            'create_shared_zip': True,
            'includes': [
                'lxml.etree', 'lxml._elementpath', 'gzip', 'inspect', 'atexit',
            ],
            'excludes': [
                'ssl', 'bz2', 'select', 'hashlib', 'socket', 'pyexpat',
                'test', 'Tkinter', 'unittest', 'doctest', 'xml', 'optparse', 'locale', 'calendar', 'gettext', 'difflib',
                'cookielib', 'urllib', 'urllib2', 'subprocess', 'cgi', 'rfc822', 'tempfile', 'plistlib', 'webbrowser',
                'logging', 'email', 'tarfile', 'argparse', 'zipfile', 'random', 'mimetools', 'tempfile',
                'ctypes.macholib',
                'pyglet.window.cocoa', 'pyglet.window.xlib', 'pyglet.window.carbon', 'pyglet.media', 'pyglet.libs.x11',
                'pyglet.libs.darwin',
            ]
        },
    },
    executables=[
        Executable('fez_decomp.py'),
        Executable('read_xact.py'),
        Executable('read_xnb_dir.py'),
        Executable('show_ao.py'),
    ],
)

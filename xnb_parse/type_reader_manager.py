"""
load and manage type readers
"""

import pkgutil

from xnb_parse.type_spec import TypeSpec


class TypeReaderManager(object):
    type_readers = {}

    def __init__(self, reader_dir=None):
        self.reader_dir = reader_dir
        self.type_readers = {}
        classes = _find_subclasses('xnb_parse', 'type_readers', BaseTypeReader)
        print classes

    def get_type(self, name, version):
        name = self.strip_assembly_version(name)
        return name

    @staticmethod
    def strip_assembly_version(name):
        type_spec = TypeSpec.parse(name)
        return type_spec.full_name


class BaseTypeReader(object):
    name = None

    def __str__(self):
        return self.name


def _find_subclasses(root_pkgname, plugin_pkgname, cls):
    """
    Find all subclass of cls in py files located below path
    (does look in sub directories)

    @param cls: the base class that all subclasses should inherit from
    @type cls: class
    @rtype: list
    @return: a list if classes that are subclasses of cls
    """

    subclasses = []

    # iccck, must be a better way of doing this
    plugin_pkg = getattr(__import__(root_pkgname, globals(), locals(), [plugin_pkgname]), plugin_pkgname)
    for _, modulename, _ in pkgutil.walk_packages(plugin_pkg.__path__, plugin_pkg.__name__ + '.'):
        print 'searching', modulename
        path_name, _, module_name = modulename.rpartition('.')
        module = getattr(__import__(path_name, globals(), locals(), [module_name]), module_name)

        # look through module dictionary for things that are subclass of cls but are not cls itself
        for key, entry in module.__dict__.items():
            if key == cls.__name__:
                continue
            try:
                if issubclass(entry, cls):
                    print 'Found subclass:', key
                    subclasses.append(entry)
            except TypeError:
                # this happens when a non-type is passed in to issubclass. We don't care as it can't be a subclass of
                # cls if it isn't a type
                continue
    return subclasses

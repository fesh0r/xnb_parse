"""
math types
"""

from __future__ import print_function

from collections import namedtuple

from xnb_parse.file_formats.xml_utils import ET


_Color = namedtuple('Color', ['r', 'g', 'b', 'a'])


class Color(_Color):
    __slots__ = ()

    def to_packed(self):
        return self.r | self.g << 8 | self.b << 16 | self.a << 24

    @staticmethod
    def from_packed(data):
        v_r = data & 0xff
        v_g = data >> 8 & 0xff
        v_b = data >> 16 & 0xff
        v_a = data >> 24 & 0xff
        return Color(v_r, v_g, v_b, v_a)

    @staticmethod
    def from_string(data):
        clean_data = data
        if clean_data.startswith('#'):
            clean_data = clean_data[1:]
        if len(clean_data) == 6:
            clean_data = 'ff' + clean_data
        if len(clean_data) != 8:
            raise ValueError("Invalid color: '{}'".format(data))
        v_a = int(clean_data[0:2], 16)
        v_r = int(clean_data[2:4], 16)
        v_g = int(clean_data[4:6], 16)
        v_b = int(clean_data[6:8], 16)
        return Color(v_r, v_g, v_b, v_a)

    def attrib(self):
        return "#{:02X}{:02X}{:02X}{:02X}".format(self.a, self.r, self.g, self.b)

    def xml(self, parent):
        root = ET.SubElement(parent, 'Color')
        root.set('c', self.attrib())
        return root


_Rectangle = namedtuple('Rectangle', ['x', 'y', 'w', 'h'])


class Rectangle(_Rectangle):
    __slots__ = ()

    def xml(self, parent):
        root = ET.SubElement(parent, 'Rectangle')
        root.set('x', str(self.x))
        root.set('y', str(self.y))
        root.set('w', str(self.w))
        root.set('h', str(self.h))
        return root


_Quarternion = namedtuple('Quarternion', ['x', 'y', 'z', 'w'])


class Quaternion(_Quarternion):
    __slots__ = ()

    def xml(self, parent):
        root = ET.SubElement(parent, 'Quaternion')
        root.set('x', str(self.x))
        root.set('y', str(self.y))
        root.set('z', str(self.z))
        root.set('w', str(self.w))
        return root


_Vector2 = namedtuple('Vector2', ['x', 'y'])


class Vector2(_Vector2):
    __slots__ = ()

    def xml(self, parent):
        root = ET.SubElement(parent, 'Vector2')
        root.set('x', str(self.x))
        root.set('y', str(self.y))
        return root


_Vector3 = namedtuple('Vector3', ['x', 'y', 'z'])


class Vector3(_Vector3):
    __slots__ = ()

    def xml(self, parent):
        root = ET.SubElement(parent, 'Vector3')
        root.set('x', str(self.x))
        root.set('y', str(self.y))
        root.set('z', str(self.z))
        return root


_Vector4 = namedtuple('Vector4', ['x', 'y', 'z', 'w'])


class Vector4(_Vector4):
    __slots__ = ()

    def xml(self, parent):
        root = ET.SubElement(parent, 'Vector4')
        root.set('x', str(self.x))
        root.set('y', str(self.y))
        root.set('z', str(self.z))
        root.set('w', str(self.w))
        return root


_Point = namedtuple('Point', ['x', 'y'])


class Point(_Point):
    __slots__ = ()

    def xml(self, parent):
        root = ET.SubElement(parent, 'Point')
        root.set('x', str(self.x))
        root.set('y', str(self.y))
        return root


_Plane = namedtuple('Plane', ['normal', 'd'])


class Plane(_Plane):
    __slots__ = ()

    def xml(self, parent):
        root = ET.SubElement(parent, 'Plane')
        root.set('d', str(self.d))
        self.normal.xml(root)
        return root


_BoundingBox = namedtuple('BoundingBox', ['min', 'max'])


class BoundingBox(_BoundingBox):
    __slots__ = ()

    def xml(self, parent):
        root = ET.SubElement(parent, 'BoundingBox')
        self.min.xml(root)
        self.max.xml(root)
        return root


_BoundingSphere = namedtuple('BoundingSphere', ['center', 'radius'])


class BoundingSphere(_BoundingSphere):
    __slots__ = ()

    def xml(self, parent):
        root = ET.SubElement(parent, 'BoundingSphere')
        root.set('radius', str(self.radius))
        self.center.xml(root)
        return root


_Ray = namedtuple('Ray', ['pos', 'dir'])


class Ray(_Ray):
    __slots__ = ()

    def xml(self, parent):
        root = ET.SubElement(parent, 'Ray')
        self.pos.xml(root)
        self.dir.xml(root)
        return root


class Matrix(object):
    __slots__ = ('value',)

    def __init__(self, value):
        if len(value) != 16:
            raise ValueError("Invalid Matrix")
        self.value = value

    def __repr__(self):
        return 'Matrix(' + ','.join([str(v) for v in self.value]) + ')'

    def xml(self, parent):
        root = self.value.xml(parent, 'Matrix', 'Cell')
        return root


_BoundingFrustum = namedtuple('BoundingFrustum', ['v'])


class BoundingFrustum(_BoundingFrustum):
    __slots__ = ()

    def xml(self, parent):
        root = ET.SubElement(parent, 'BoundingFrustum')
        self.v.xml(root)
        return root

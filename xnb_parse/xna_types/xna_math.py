"""
math types
"""

from collections import namedtuple

from xnb_parse.file_formats.xml_utils import E


_Color = namedtuple('Color', ['r', 'g', 'b', 'a'])  # pylint: disable-msg=C0103


class Color(_Color):  # pylint: disable-msg=W0232
    # pylint: disable-msg=E1101
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

    def xml(self):
        root = E.Color(c=self.attrib())
        return root


_Rectangle = namedtuple('Rectangle', ['x', 'y', 'w', 'h'])  # pylint: disable-msg=C0103


class Rectangle(_Rectangle):  # pylint: disable-msg=W0232
    # pylint: disable-msg=E1101
    __slots__ = ()

    def xml(self):
        root = E.Rectangle(x=str(self.x), y=str(self.y), w=str(self.w), h=str(self.h))
        return root


_Quarternion = namedtuple('Quarternion', ['x', 'y', 'z', 'w'])  # pylint: disable-msg=C0103


class Quaternion(_Quarternion):  # pylint: disable-msg=W0232
    # pylint: disable-msg=E1101
    __slots__ = ()

    def xml(self):
        root = E.Quaternion(x=str(self.x), y=str(self.y), z=str(self.z), w=str(self.w))
        return root


_Vector2 = namedtuple('Vector2', ['x', 'y'])  # pylint: disable-msg=C0103


class Vector2(_Vector2):  # pylint: disable-msg=W0232
    # pylint: disable-msg=E1101
    __slots__ = ()

    def xml(self):
        root = E.Vector2(x=str(self.x), y=str(self.y))
        return root


_Vector3 = namedtuple('Vector3', ['x', 'y', 'z'])  # pylint: disable-msg=C0103


class Vector3(_Vector3):  # pylint: disable-msg=W0232
    # pylint: disable-msg=E1101
    __slots__ = ()

    def xml(self):
        root = E.Vector3(x=str(self.x), y=str(self.y), z=str(self.z))
        return root


_Vector4 = namedtuple('Vector4', ['x', 'y', 'z', 'w'])  # pylint: disable-msg=C0103


class Vector4(_Vector4):  # pylint: disable-msg=W0232
    # pylint: disable-msg=E1101
    __slots__ = ()

    def xml(self):
        root = E.Vector4(x=str(self.x), y=str(self.y), z=str(self.z), w=str(self.w))
        return root


_Point = namedtuple('Point', ['x', 'y'])  # pylint: disable-msg=C0103


class Point(_Point):  # pylint: disable-msg=W0232
    # pylint: disable-msg=E1101
    __slots__ = ()

    def xml(self):
        root = E.Point(x=str(self.x), y=str(self.y))
        return root


_Plane = namedtuple('Plane', ['normal', 'd'])  # pylint: disable-msg=C0103


class Plane(_Plane):  # pylint: disable-msg=W0232
    # pylint: disable-msg=E1101
    __slots__ = ()

    def xml(self):
        root = E.Plane(self.normal.xml(), d=str(self.d))
        return root


_BoundingBox = namedtuple('BoundingBox', ['min', 'max'])  # pylint: disable-msg=C0103


class BoundingBox(_BoundingBox):  # pylint: disable-msg=W0232
    # pylint: disable-msg=E1101
    __slots__ = ()

    def xml(self):
        root = E.BoundingBox(self.min.xml(), self.max.xml())
        return root


_BoundingSphere = namedtuple('BoundingSphere', ['center', 'radius'])  # pylint: disable-msg=C0103


class BoundingSphere(_BoundingSphere):  # pylint: disable-msg=W0232
    # pylint: disable-msg=E1101
    __slots__ = ()

    def xml(self):
        root = E.BoundingSphere(self.center.xml(), radius=str(self.radius))
        return root


_Ray = namedtuple('Ray', ['pos', 'dir'])  # pylint: disable-msg=C0103


class Ray(_Ray):  # pylint: disable-msg=W0232
    # pylint: disable-msg=E1101
    __slots__ = ()

    def xml(self):
        root = E.Ray(self.pos.xml(), self.dir.xml())
        return root


class Matrix(object):
    __slots__ = ('value',)

    def __init__(self, value):
        if len(value) != 16:
            raise ValueError("Invalid Matrix")
        self.value = value

    def __repr__(self):
        return 'Matrix(' + ','.join([str(v) for v in self.value]) + ')'

    def xml(self):
        root = self.value.xml('Matrix', 'Cell')
        return root


_BoundingFrustum = namedtuple('BoundingFrustum', ['v'])  # pylint: disable-msg=C0103


class BoundingFrustum(_BoundingFrustum):  # pylint: disable-msg=W0232
    # pylint: disable-msg=E1101
    __slots__ = ()

    def xml(self):
        root = E.BoundingFrustum(self.v.xml())
        return root

# coding=utf-8
"""
math types
"""

from __future__ import absolute_import, division, unicode_literals, print_function

from collections import namedtuple

from xnb_parse.file_formats.xml_utils import E


# pylint: disable-msg=E1001,W0232,E1101
#noinspection PyClassicStyleClass,PyOldStyleClasses,PyUnresolvedReferences
class Color(namedtuple('Color', ['r', 'g', 'b', 'a'])):
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


# pylint: disable-msg=E1001,W0232,E1101
#noinspection PyClassicStyleClass,PyOldStyleClasses,PyUnresolvedReferences
class Rectangle(namedtuple('Rectangle', ['x', 'y', 'w', 'h'])):
    __slots__ = ()

    def xml(self):
        root = E.Rectangle(x=str(self.x), y=str(self.y), w=str(self.w), h=str(self.h))
        return root


# pylint: disable-msg=E1001,W0232,E1101
#noinspection PyClassicStyleClass,PyOldStyleClasses,PyUnresolvedReferences
class Quaternion(namedtuple('Quarternion', ['x', 'y', 'z', 'w'])):
    __slots__ = ()

    def xml(self):
        root = E.Quaternion(x=str(self.x), y=str(self.y), z=str(self.z), w=str(self.w))
        return root


# pylint: disable-msg=E1001,W0232,E1101
#noinspection PyClassicStyleClass,PyOldStyleClasses,PyUnresolvedReferences
class Vector2(namedtuple('Vector2', ['x', 'y'])):
    __slots__ = ()

    def xml(self):
        root = E.Vector2(x=str(self.x), y=str(self.y))
        return root


# pylint: disable-msg=E1001,W0232,E1101
#noinspection PyClassicStyleClass,PyOldStyleClasses,PyUnresolvedReferences
class Vector3(namedtuple('Vector3', ['x', 'y', 'z'])):
    __slots__ = ()

    def xml(self):
        root = E.Vector3(x=str(self.x), y=str(self.y), z=str(self.z))
        return root


# pylint: disable-msg=E1001,W0232,E1101
#noinspection PyClassicStyleClass,PyOldStyleClasses,PyUnresolvedReferences
class Vector4(namedtuple('Vector4', ['x', 'y', 'z', 'w'])):
    __slots__ = ()

    def xml(self):
        root = E.Vector4(x=str(self.x), y=str(self.y), z=str(self.z), w=str(self.w))
        return root


# pylint: disable-msg=E1001,W0232,E1101
#noinspection PyClassicStyleClass,PyOldStyleClasses,PyUnresolvedReferences
class Point(namedtuple('Point', ['x', 'y'])):
    __slots__ = ()

    def xml(self):
        root = E.Point(x=str(self.x), y=str(self.y))
        return root


# pylint: disable-msg=E1001,W0232,E1101
#noinspection PyClassicStyleClass,PyOldStyleClasses,PyUnresolvedReferences
class Plane(namedtuple('Plane', ['normal', 'd'])):
    __slots__ = ()

    def xml(self):
        root = E.Plane(self.normal.xml(), d=str(self.d))
        return root


# pylint: disable-msg=E1001,W0232,E1101
#noinspection PyClassicStyleClass,PyOldStyleClasses,PyUnresolvedReferences
class BoundingBox(namedtuple('BoundingBox', ['min', 'max'])):
    __slots__ = ()

    def xml(self):
        root = E.BoundingBox(self.min.xml(), self.max.xml())
        return root


# pylint: disable-msg=E1001,W0232,E1101
#noinspection PyClassicStyleClass,PyOldStyleClasses,PyUnresolvedReferences
class BoundingSphere(namedtuple('BoundingSphere', ['center', 'radius'])):
    __slots__ = ()

    def xml(self):
        root = E.BoundingSphere(self.center.xml(), radius=str(self.radius))
        return root


# pylint: disable-msg=E1001,W0232,E1101
#noinspection PyClassicStyleClass,PyOldStyleClasses,PyUnresolvedReferences
class Ray(namedtuple('Ray', ['pos', 'dir'])):
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


# pylint: disable-msg=E1001,W0232,E1101
#noinspection PyClassicStyleClass,PyOldStyleClasses,PyUnresolvedReferences
class BoundingFrustum(namedtuple('BoundingFrustum', ['v'])):
    __slots__ = ()

    def xml(self):
        root = E.BoundingFrustum(self.v.xml())
        return root

"""
math types
"""

from collections import namedtuple

from xnb_parse.file_formats.xml_utils import E


# pylint: disable-msg=E1001,W0232,E1101
#noinspection PyClassicStyleClass,PyOldStyleClasses,PyUnresolvedReferences
class Color(namedtuple('Color', ['r', 'g', 'b', 'a'])):
    __slots__ = ()

    def to_packed(self):
        return (self.r & 0xff) | ((self.g & 0xff) << 8) | ((self.b & 0xff) << 16) | ((self.a & 0xff) << 24)

    @staticmethod
    def from_packed(data):
        v_r = (data >> 0) & 0xff
        v_g = (data >> 8) & 0xff
        v_b = (data >> 16) & 0xff
        v_a = (data >> 24)
        return Color(v_r, v_g, v_b, v_a)

    @staticmethod
    def from_string(data):
        clean_data = data
        if clean_data.startswith('#'):
            clean_data = clean_data[1:]
        if len(clean_data) == 6:
            clean_data = 'ff' + clean_data
        if len(clean_data) != 8:
            raise ValueError("Invalid color: '%s'" % data)
        v_a = int(clean_data[0:2], 16)
        v_r = int(clean_data[2:4], 16)
        v_g = int(clean_data[4:6], 16)
        v_b = int(clean_data[6:8], 16)
        return Color(v_r, v_g, v_b, v_a)

    def attrib(self):
        return "#%02X%02X%02X%02X" % (self.a, self.r, self.g, self.b)

    def xml(self):
        return E.Color(c=self.attrib())


# pylint: disable-msg=E1001,W0232,E1101
#noinspection PyClassicStyleClass,PyOldStyleClasses,PyUnresolvedReferences
class Rectangle(namedtuple('Rectangle', ['x', 'y', 'w', 'h'])):
    __slots__ = ()

    def xml(self):
        return E.Rectangle(x=str(self.x), y=str(self.y), w=str(self.w), h=str(self.h))


# pylint: disable-msg=E1001,W0232,E1101
#noinspection PyClassicStyleClass,PyOldStyleClasses,PyUnresolvedReferences
class Quaternion(namedtuple('Quarternion', ['x', 'y', 'z', 'w'])):
    __slots__ = ()

    def xml(self):
        return E.Quaternion(x=str(self.x), y=str(self.y), z=str(self.z), w=str(self.w))


# pylint: disable-msg=E1001,W0232,E1101
#noinspection PyClassicStyleClass,PyOldStyleClasses,PyUnresolvedReferences
class Vector2(namedtuple('Vector2', ['x', 'y'])):
    __slots__ = ()

    def xml(self):
        return E.Vector2(x=str(self.x), y=str(self.y))


# pylint: disable-msg=E1001,W0232,E1101
#noinspection PyClassicStyleClass,PyOldStyleClasses,PyUnresolvedReferences
class Vector3(namedtuple('Vector3', ['x', 'y', 'z'])):
    __slots__ = ()

    def xml(self):
        return E.Vector3(x=str(self.x), y=str(self.y), z=str(self.z))


# pylint: disable-msg=E1001,W0232,E1101
#noinspection PyClassicStyleClass,PyOldStyleClasses,PyUnresolvedReferences
class Vector4(namedtuple('Vector4', ['x', 'y', 'z', 'w'])):
    __slots__ = ()

    def xml(self):
        return E.Vector4(x=str(self.x), y=str(self.y), z=str(self.z), w=str(self.w))


# pylint: disable-msg=E1001,W0232,E1101
#noinspection PyClassicStyleClass,PyOldStyleClasses,PyUnresolvedReferences
class Point(namedtuple('Point', ['x', 'y'])):
    __slots__ = ()

    def xml(self):
        return E.Point(x=str(self.x), y=str(self.y))


# pylint: disable-msg=E1001,W0232,E1101
#noinspection PyClassicStyleClass,PyOldStyleClasses,PyUnresolvedReferences
class Plane(namedtuple('Plane', ['normal', 'd'])):
    __slots__ = ()

    def xml(self):
        return E.Plane(self.normal.xml(), d=str(self.d))


# pylint: disable-msg=E1001,W0232,E1101
#noinspection PyClassicStyleClass,PyOldStyleClasses,PyUnresolvedReferences
class BoundingBox(namedtuple('BoundingBox', ['min', 'max'])):
    __slots__ = ()

    def xml(self):
        return E.BoundingBox(self.min.xml(), self.max.xml())


# pylint: disable-msg=E1001,W0232,E1101
#noinspection PyClassicStyleClass,PyOldStyleClasses,PyUnresolvedReferences
class BoundingSphere(namedtuple('BoundingSphere', ['center', 'radius'])):
    __slots__ = ()

    def xml(self):
        return E.BoundingSphere(self.center.xml(), radius=str(self.radius))


# pylint: disable-msg=E1001,W0232,E1101
#noinspection PyClassicStyleClass,PyOldStyleClasses,PyUnresolvedReferences
class Ray(namedtuple('Ray', ['pos', 'dir'])):
    __slots__ = ()

    def xml(self):
        return E.Ray(self.pos.xml(), self.dir.xml())


class Matrix(object):
    __slots__ = ('value',)

    def __init__(self, value):
        if len(value) != 16:
            raise ValueError("Invalid Matrix")
        self.value = value

    def __repr__(self):
        return 'Matrix(' + ','.join([str(v) for v in self.value]) + ')'

    def xml(self):
        root = E.Matrix()
        for cell in self.value:
            root.append(E.Cell(str(cell)))
        return root


# pylint: disable-msg=E1001,W0232,E1101
#noinspection PyClassicStyleClass,PyOldStyleClasses,PyUnresolvedReferences
class BoundingFrustum(namedtuple('BoundingFrustum', ['v'])):
    __slots__ = ()

    def xml(self):
        return E.BoundingFrustum(self.v.xml())

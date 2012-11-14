# coding=utf-8
"""
math type readers
"""

from __future__ import print_function

from xnb_parse.type_reader_manager import TypeReaderPlugin
from xnb_parse.type_reader import BaseTypeReader, ValueTypeReader
from xnb_parse.xna_types.xna_math import Rectangle, Point, Plane, BoundingBox, BoundingSphere, Ray, BoundingFrustum


class Vector2Reader(ValueTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.Vector2'
    reader_name = 'Microsoft.Xna.Framework.Content.Vector2Reader'

    def read(self):
        return self.stream.read_vector2()


class Vector3Reader(ValueTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.Vector3'
    reader_name = 'Microsoft.Xna.Framework.Content.Vector3Reader'

    def read(self):
        return self.stream.read_vector3()


class Vector4Reader(ValueTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.Vector4'
    reader_name = 'Microsoft.Xna.Framework.Content.Vector4Reader'

    def read(self):
        return self.stream.read_vector4()


class MatrixReader(ValueTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.Matrix'
    reader_name = 'Microsoft.Xna.Framework.Content.MatrixReader'

    def read(self):
        return self.stream.read_matrix()


class QuaternionReader(ValueTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.Quaternion'
    reader_name = 'Microsoft.Xna.Framework.Content.QuaternionReader'

    def read(self):
        return self.stream.read_quaternion()


class ColorReader(ValueTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.Graphics.Color'
    reader_name = 'Microsoft.Xna.Framework.Content.ColorReader'

    def read(self):
        return self.stream.read_color()


class PlaneReader(ValueTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.Plane'
    reader_name = 'Microsoft.Xna.Framework.Content.PlaneReader'

    def read(self):
        plane_normal = self.stream.read_vector3()
        plane_d = self.stream.read_single()
        return Plane(plane_normal, plane_d)


class PointReader(ValueTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.Point'
    reader_name = 'Microsoft.Xna.Framework.Content.PointReader'

    def read(self):
        v_x = self.stream.read_int32()
        v_y = self.stream.read_int32()
        return Point(v_x, v_y)


class RectangleReader(ValueTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.Rectangle'
    reader_name = 'Microsoft.Xna.Framework.Content.RectangleReader'

    def read(self):
        v_x = self.stream.read_int32()
        v_y = self.stream.read_int32()
        v_w = self.stream.read_int32()
        v_h = self.stream.read_int32()
        return Rectangle(v_x, v_y, v_w, v_h)


class BoundingBoxReader(ValueTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.BoundingBox'
    reader_name = 'Microsoft.Xna.Framework.Content.BoundingBoxReader'

    def read(self):
        v_min = self.stream.read_vector3()
        v_max = self.stream.read_vector3()
        return BoundingBox(v_min, v_max)


class BoundingSphereReader(ValueTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.BoundingSphere'
    reader_name = 'Microsoft.Xna.Framework.Content.BoundingSphereReader'

    def read(self):
        v_centre = self.stream.read_vector3()
        v_radius = self.stream.read_single()
        return BoundingSphere(v_centre, v_radius)


class BoundingFrustumReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.BoundingFrustum'
    reader_name = 'Microsoft.Xna.Framework.Content.BoundingFrustumReader'

    def read(self):
        value = self.stream.read_matrix()
        return BoundingFrustum(value)


class RayReader(ValueTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.Ray'
    reader_name = 'Microsoft.Xna.Framework.Content.RayReader'

    def read(self):
        v_pos = self.stream.read_vector3()
        v_dir = self.stream.read_vector3()
        return Ray(v_pos, v_dir)


class CurveReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.Curve'
    reader_name = 'Microsoft.Xna.Framework.Content.CurveReader'

    def read(self):
        pre_loop = self.stream.read_int32()
        post_loop = self.stream.read_int32()
        key_count = self.stream.read_int32()
        keys = []
        for _ in range(key_count):
            pos = self.stream.read_single()
            value = self.stream.read_single()
            tangent_in = self.stream.read_single()
            tangent_out = self.stream.read_single()
            cont = self.stream.read_int32()
            key = (pos, value, tangent_in, tangent_out, cont)
            keys.append(key)
        return pre_loop, post_loop, keys

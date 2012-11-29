"""
math type readers
"""

from __future__ import print_function

from xnb_parse.type_reader import TypeReaderPlugin, BaseTypeReader, ValueTypeReader
from xnb_parse.xna_types.xna_math import (Rectangle, Point, Plane, BoundingBox, BoundingSphere, Ray, BoundingFrustum,
                                          Vector2, Vector3, Vector4, Matrix, Quaternion, Color)
from xnb_parse.xna_types.xna_system import XNAList


class Vector2Reader(ValueTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.Vector2'
    reader_name = 'Microsoft.Xna.Framework.Content.Vector2Reader'

    def read(self):
        return Vector2._make(self.stream.unpack('2f'))


class Vector3Reader(ValueTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.Vector3'
    reader_name = 'Microsoft.Xna.Framework.Content.Vector3Reader'

    def read(self):
        return Vector3._make(self.stream.unpack('3f'))


class Vector4Reader(ValueTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.Vector4'
    reader_name = 'Microsoft.Xna.Framework.Content.Vector4Reader'

    def read(self):
        return Vector4._make(self.stream.unpack('4f'))


class MatrixReader(ValueTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.Matrix'
    reader_name = 'Microsoft.Xna.Framework.Content.MatrixReader'

    def read(self):
        return Matrix(XNAList(self.stream.unpack('16f')))


class QuaternionReader(ValueTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.Quaternion'
    reader_name = 'Microsoft.Xna.Framework.Content.QuaternionReader'

    def read(self):
        return Quaternion._make(self.stream.unpack('4f'))


class ColorReader(ValueTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.Graphics.Color'
    reader_name = 'Microsoft.Xna.Framework.Content.ColorReader'

    def read(self):
        return Color._make(self.stream.unpack('4B'))


class PlaneReader(ValueTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.Plane'
    reader_name = 'Microsoft.Xna.Framework.Content.PlaneReader'

    def read(self):
        values = self.stream.unpack('3f f')
        plane_normal = Vector3._make(values[0:3])
        plane_d = values[3]
        return Plane(plane_normal, plane_d)


class PointReader(ValueTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.Point'
    reader_name = 'Microsoft.Xna.Framework.Content.PointReader'

    def read(self):
        return Point._make(self.stream.unpack('2i'))


class RectangleReader(ValueTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.Rectangle'
    reader_name = 'Microsoft.Xna.Framework.Content.RectangleReader'

    def read(self):
        return Rectangle._make(self.stream.unpack('4i'))


class BoundingBoxReader(ValueTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.BoundingBox'
    reader_name = 'Microsoft.Xna.Framework.Content.BoundingBoxReader'

    def read(self):
        values = self.stream.unpack('3f 3f')
        v_min = Vector3._make(values[0:3])
        v_max = Vector3._make(values[3:6])
        return BoundingBox(v_min, v_max)


class BoundingSphereReader(ValueTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.BoundingSphere'
    reader_name = 'Microsoft.Xna.Framework.Content.BoundingSphereReader'

    def read(self):
        values = self.stream.unpack('3f f')
        v_centre = Vector3._make(values[0:3])
        v_radius = values[3]
        return BoundingSphere(v_centre, v_radius)


class BoundingFrustumReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.BoundingFrustum'
    reader_name = 'Microsoft.Xna.Framework.Content.BoundingFrustumReader'

    def read(self):
        return BoundingFrustum._make(Matrix(XNAList(self.stream.unpack('16f'))))


class RayReader(ValueTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.Ray'
    reader_name = 'Microsoft.Xna.Framework.Content.RayReader'

    def read(self):
        values = self.stream.unpack('3f 3f')
        v_pos = Vector3._make(values[0:3])
        v_dir = Vector3._make(values[3:6])
        return Ray(v_pos, v_dir)


class CurveReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.Curve'
    reader_name = 'Microsoft.Xna.Framework.Content.CurveReader'

    def read(self):
        pre_loop, post_loop, key_count = self.stream.unpack('3i')
        keys = []
        for _ in range(key_count):
            v_pos, v_value, v_tangent_in, v_tangent_out, v_cont = self.stream.unpack('ffffi')
            key = (v_pos, v_value, v_tangent_in, v_tangent_out, v_cont)
            keys.append(key)
        return pre_loop, post_loop, keys

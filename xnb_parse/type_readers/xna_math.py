"""
math type readers
"""

from xnb_parse.type_reader_manager import TypeReaderPlugin
from xnb_parse.type_reader import BaseTypeReader, ValueTypeReader


class Vector2Reader(ValueTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.Vector2'
    reader_name = 'Microsoft.Xna.Framework.Content.Vector2Reader'

    def read(self):
        v_x = self.stream.read('f')
        v_y = self.stream.read('f')
        return v_x, v_y


class Vector3Reader(ValueTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.Vector3'
    reader_name = 'Microsoft.Xna.Framework.Content.Vector3Reader'

    def read(self):
        v_x = self.stream.read('f')
        v_y = self.stream.read('f')
        v_z = self.stream.read('f')
        return v_x, v_y, v_z


class Vector4Reader(ValueTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.Vector4'
    reader_name = 'Microsoft.Xna.Framework.Content.Vector4Reader'

    def read(self):
        v_x = self.stream.read('f')
        v_y = self.stream.read('f')
        v_z = self.stream.read('f')
        v_w = self.stream.read('f')
        return v_x, v_y, v_z, v_w


class MatrixReader(ValueTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.Matrix'
    reader_name = 'Microsoft.Xna.Framework.Content.MatrixReader'

    def read(self):
        matrix = []
        for _ in range(16):
            value = self.stream.read('f')
            matrix.append(value)
        return matrix


class QuaternionReader(ValueTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.Quaternion'
    reader_name = 'Microsoft.Xna.Framework.Content.QuaternionReader'

    def read(self):
        v_x = self.stream.read('f')
        v_y = self.stream.read('f')
        v_z = self.stream.read('f')
        v_w = self.stream.read('f')
        return v_x, v_y, v_z, v_w


class ColorReader(ValueTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.Color'
    reader_name = 'Microsoft.Xna.Framework.Content.ColorReader'

    def read(self):
        v_r = self.stream.read('u1')
        v_g = self.stream.read('u1')
        v_b = self.stream.read('u1')
        v_a = self.stream.read('u1')
        return v_r, v_g, v_b, v_a


class PlaneReader(ValueTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.Plane'
    reader_name = 'Microsoft.Xna.Framework.Content.PlaneReader'

    def read(self):
        plane_normal = Vector2Reader.read_from(self.stream)
        plane_d = self.stream.read('f')
        return plane_normal, plane_d


class PointReader(ValueTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.Point'
    reader_name = 'Microsoft.Xna.Framework.Content.PointReader'

    def read(self):
        v_x = self.stream.read('s4')
        v_y = self.stream.read('s4')
        return v_x, v_y


class RectangleReader(ValueTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.Rectangle'
    reader_name = 'Microsoft.Xna.Framework.Content.RectangleReader'

    def read(self):
        v_x = self.stream.read('s4')
        v_y = self.stream.read('s4')
        v_w = self.stream.read('s4')
        v_h = self.stream.read('s4')
        return v_x, v_y, v_w, v_h


class BoundingBoxReader(ValueTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.BoundingBox'
    reader_name = 'Microsoft.Xna.Framework.Content.BoundingBoxReader'

    def read(self):
        v_min = Vector3Reader.read_from(self.stream)
        v_max = Vector3Reader.read_from(self.stream)
        return v_min, v_max


class BoundingSphereReader(ValueTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.BoundingSphere'
    reader_name = 'Microsoft.Xna.Framework.Content.BoundingSphereReader'

    def read(self):
        v_centre = Vector3Reader.read_from(self.stream)
        v_radius = self.stream.read('f')
        return v_centre, v_radius


class BoundingFrustumReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.BoundingFrustum'
    reader_name = 'Microsoft.Xna.Framework.Content.BoundingFrustumReader'

    def read(self):
        value = MatrixReader.read_from(self.stream)
        return value


class RayReader(ValueTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.Ray'
    reader_name = 'Microsoft.Xna.Framework.Content.RayReader'

    def read(self):
        v_pos = Vector3Reader.read_from(self.stream)
        v_dir = Vector3Reader.read_from(self.stream)
        return v_pos, v_dir


class CurveReader(BaseTypeReader, TypeReaderPlugin):
    target_type = 'Microsoft.Xna.Framework.Curve'
    reader_name = 'Microsoft.Xna.Framework.Content.CurveReader'

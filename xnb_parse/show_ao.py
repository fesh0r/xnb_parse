# coding=utf-8
"""
Display ArtObject
"""

from __future__ import absolute_import, division, unicode_literals, print_function

import os
import sys
import pyglet
from pyglet.gl import *  # pylint: disable-msg=W0614,W0401

from xnb_parse.trackball_camera import TrackballCamera, norm1, vec_args
from xnb_parse.type_reader import ReaderError
from xnb_parse.xnb_reader import XNBReader
from xnb_parse.type_reader_manager import TypeReaderManager
from xnb_parse.xna_types.xna_math import Vector3
from xnb_parse.xna_types.xna_graphics import Texture2D
from xnb_parse.xna_types.fez.fez_graphics import ArtObject


NORMALS = [Vector3(-1., 0., 0.), Vector3(0., -1., 0.), Vector3(0., 0., -1.),
           Vector3(1., 0., 0.), Vector3(0., 1., 0.), Vector3(0., 0., 1.)]


#noinspection PyMethodOverriding
class AOWindow(pyglet.window.Window):  # pylint: disable-msg=W0223
    wireframe = False
    lighting = True
    culling = False
    texturing = True

    def __init__(self, filename, width=1000, height=750, config=None):  # pylint: disable-msg=W0231
        #noinspection PyCallByClass,PyTypeChecker
        pyglet.window.Window.__init__(self, width=width, height=height, resizable=True, config=config)
        self.gl_setup()
        self.art_object = AO(filename)
        self.tbcam = TrackballCamera()
        self.fps_display = pyglet.clock.ClockDisplay(color=(0.5, 0.5, 0.5, 1.0))

    @staticmethod
    def gl_setup():
        glClearColor(0.3926, 0.5843, 0.9294, 1.0)
        glClearDepth(1.0)
        glColor3f(1.0, 1.0, 1.0)

        glDisable(GL_CULL_FACE)
        glFrontFace(GL_CW)

        glEnable(GL_DEPTH_TEST)

        glShadeModel(GL_SMOOTH)

        glPolygonOffset(1, 1)

        glDisable(GL_LIGHTING)

        glEnable(GL_LIGHT0)
        glLightfv(GL_LIGHT0, GL_POSITION, vec_args(0.5, 0.5, 10.0, 1.0))
        glLightfv(GL_LIGHT0, GL_AMBIENT, vec_args(0.5, 0.5, 0.5, 1.0))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, vec_args(1.0, 1.0, 1.0, 1.0))

    def on_resize(self, width, height):
        # Override the default on_resize handler to create a 3D projection
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, float(self.width) / float(self.height), 0.1, 100.0)
        self.tbcam.update_modelview()
        glMatrixMode(GL_MODELVIEW)
        return pyglet.event.EVENT_HANDLED

    def on_draw(self):  # pylint: disable-msg=W0221
        self.clear()

        if self.culling:
            glEnable(GL_CULL_FACE)
        if self.lighting:
            glEnable(GL_LIGHTING)
        if self.wireframe:
            glEnable(GL_POLYGON_OFFSET_FILL)
            glColor3f(1.0, 1.0, 1.0)
            self.art_object.draw(self.texturing)
            glDisable(GL_POLYGON_OFFSET_FILL)

            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            glColor3f(0.0, 0.0, 0.0)
            glDisable(GL_LIGHTING)
            self.art_object.draw(False)
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glColor3f(1.0, 1.0, 1.0)
            self.art_object.draw(self.texturing)
        glDisable(GL_CULL_FACE)
        glDisable(GL_LIGHTING)

    #noinspection PyUnusedLocal
    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.W:
            self.wireframe = not self.wireframe
        elif symbol == pyglet.window.key.L:
            self.lighting = not self.lighting
        elif symbol == pyglet.window.key.C:
            self.culling = not self.culling
        elif symbol == pyglet.window.key.T:
            self.texturing = not self.texturing
        elif symbol == pyglet.window.key.ESCAPE:
            self.dispatch_event('on_close')

    #noinspection PyUnresolvedReferences,PyUnusedLocal
    def on_mouse_press(self, x, y, button, modifiers):  # pylint: disable-msg=W0221,C0103
        if button == pyglet.window.mouse.LEFT:
            self.tbcam.mouse_roll(
                norm1(x, self.width),
                norm1(y, self.height),
                False)
        elif button == pyglet.window.mouse.RIGHT:
            self.tbcam.mouse_zoom(
                norm1(x, self.width),
                norm1(y, self.height),
                False)

    #noinspection PyUnresolvedReferences,PyUnusedLocal
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):  # pylint: disable-msg=W0221,C0103
        if buttons & pyglet.window.mouse.LEFT:
            self.tbcam.mouse_roll(
                norm1(x, self.width),
                norm1(y, self.height))
        elif buttons & pyglet.window.mouse.RIGHT:
            self.tbcam.mouse_zoom(
                norm1(x, self.width),
                norm1(y, self.height))


class AO(object):
    #noinspection PyUnresolvedReferences
    def __init__(self, ao_filename):
        type_reader_manager = TypeReaderManager()
        ao_filename = os.path.normpath(ao_filename)
        ao_dir = os.path.dirname(ao_filename)
        ao_xnb = read_xnb(ao_filename, expected_type=ArtObject, type_reader_manager=type_reader_manager)
        cm_filename = os.path.join(ao_dir, ao_xnb.cubemap_path.lower() + '.xnb')
        cm_xnb = read_xnb(cm_filename, expected_type=Texture2D, type_reader_manager=type_reader_manager)
        cm_image = pyglet.image.ImageData(cm_xnb.width, cm_xnb.height, 'RGBA', str(cm_xnb.full_data()))
        self.texture = cm_image.get_texture()

        indices = ao_xnb.geometry.indices
        vertices = []
        normals = []
        texture_coords = []
        for cur_vertex in ao_xnb.geometry.vertices:
            vertices.append(cur_vertex.position.x / ao_xnb.size.x)
            vertices.append(cur_vertex.position.y / ao_xnb.size.y)
            vertices.append(cur_vertex.position.z / ao_xnb.size.z)
            cur_normal = NORMALS[cur_vertex.normal]
            normals.append(cur_normal.x)
            normals.append(cur_normal.y)
            normals.append(cur_normal.z)
            texture_coords.append(cur_vertex.texture_coord.x)
            texture_coords.append(cur_vertex.texture_coord.y)
        self.vli = pyglet.graphics.vertex_list_indexed(len(vertices) // 3, indices,
                                                       ('v3f', vertices),
                                                       ('n3f', normals),
                                                       ('t2f', texture_coords))

        glDisable(self.texture.target)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, vec_args(0.6, 0.6, 0.6, 1.0))

    def draw(self, texturing=True):
        if texturing:
            glEnable(self.texture.target)
            glBindTexture(self.texture.target, self.texture.id)
        self.vli.draw(pyglet.gl.GL_TRIANGLES)
        glDisable(self.texture.target)


def read_xnb(filename, expected_type=None, type_reader_manager=None):
    with open(filename, 'rb') as handle:
        data = handle.read()
    xnb_content = XNBReader.load(data, type_reader_manager).content
    if expected_type is not None and type(xnb_content) != expected_type:
        raise ReaderError("Unexpected XNB type: %s != %s" % (type(xnb_content).__name__, expected_type.__name__))
    return xnb_content


def main():
    if len(sys.argv) == 2:
        # try and get 8x AA failing back to 4x and then none
        platform = pyglet.window.get_platform()
        display = platform.get_default_display()
        screen = display.get_default_screen()
        template = pyglet.gl.Config(sample_buffers=1, samples=8)
        try:
            config = screen.get_best_config(template)
        except pyglet.window.NoSuchConfigException:
            template = pyglet.gl.Config(sample_buffers=1, samples=4)
            try:
                config = screen.get_best_config(template)
            except pyglet.window.NoSuchConfigException:
                template = pyglet.gl.Config()
                config = screen.get_best_config(template)
        AOWindow(filename=sys.argv[1], config=config)
        pyglet.app.run()
    else:
        print('show_ao.py art_object.xnb')

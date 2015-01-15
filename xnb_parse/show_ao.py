"""
Display ArtObject
"""

from __future__ import print_function

import sys
import pyglet
from pyglet.gl import *

from xnb_parse.fez_content_manager import FezContentManager
from xnb_parse.trackball_camera import TrackballCamera, norm1, vec_args
from xnb_parse.type_reader import ReaderError
from xnb_parse.xna_content_manager import ContentManager
from xnb_parse.xna_types.xna_math import Vector3


NORMALS = [Vector3(-1.0, 0.0, 0.0), Vector3(0.0, -1.0, 0.0), Vector3(0.0, 0.0, -1.0),
           Vector3(1.0, 0.0, 0.0), Vector3(0.0, 1.0, 0.0), Vector3(0.0, 0.0, 1.0)]


class AOWindow(pyglet.window.Window):
    wireframe = False
    lighting = True
    culling = False
    texturing = True

    def __init__(self, content_manager, asset_name, width=1000, height=750, config=None):
        pyglet.window.Window.__init__(self, width=width, height=height, resizable=True, config=config)
        self.gl_setup()
        self.art_object = AO(content_manager, asset_name)
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

    def on_draw(self):
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

    def on_mouse_press(self, x, y, button, modifiers):
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

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if buttons & pyglet.window.mouse.LEFT:
            self.tbcam.mouse_roll(
                norm1(x, self.width),
                norm1(y, self.height))
        elif buttons & pyglet.window.mouse.RIGHT:
            self.tbcam.mouse_zoom(
                norm1(x, self.width),
                norm1(y, self.height))


class AO(object):
    def __init__(self, content_manager, asset_name):
        asset_name = 'art objects/' + asset_name
        art_object = content_manager.load(asset_name, expected_type='FezEngine.Structure.ArtObject')

        try:
            cubemap_name = 'art objects/' + art_object.cubemap_path
            cubemap = content_manager.load(cubemap_name, expected_type='Microsoft.Xna.Framework.Graphics.Texture2D')
        except AttributeError:
            cubemap = art_object.cubemap
        self.texture = pyglet.image.ImageData(cubemap.width, cubemap.height, 'RGBA', cubemap.full_data()).get_texture()

        indices = art_object.geometry.indices
        vertices = []
        normals = []
        texture_coords = []
        for cur_vertex in art_object.geometry.vertices:
            vertices.append(cur_vertex.position.x / art_object.size.x)
            vertices.append(cur_vertex.position.y / art_object.size.y)
            vertices.append(cur_vertex.position.z / art_object.size.z)
            cur_normal = NORMALS[cur_vertex.normal]
            normals.append(cur_normal.x)
            normals.append(cur_normal.y)
            normals.append(cur_normal.z)
            texture_coords.append(cur_vertex.texture_coord.x * self.texture.tex_coords[2 * 3 + 0])
            texture_coords.append(cur_vertex.texture_coord.y * self.texture.tex_coords[2 * 3 + 1])
        self.vli = pyglet.graphics.vertex_list_indexed(len(vertices) // 3, indices,
                                                       ('v3f', vertices),
                                                       ('n3f', normals),
                                                       ('t2f', texture_coords))

        glDisable(self.texture.target)
        glTexParameteri(self.texture.target, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(self.texture.target, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, vec_args(0.6, 0.6, 0.6, 1.0))

    def draw(self, texturing=True):
        if texturing:
            glEnable(self.texture.target)
            glBindTexture(self.texture.target, self.texture.id)
        self.vli.draw(pyglet.gl.GL_TRIANGLES)
        glDisable(self.texture.target)


def main():
    if len(sys.argv) == 3:
        # try and get config with 4x AA enabled, failing back to no AA
        platform = pyglet.window.get_platform()
        display = platform.get_default_display()
        screen = display.get_default_screen()
        template = pyglet.gl.Config(sample_buffers=1, samples=4)
        try:
            config = screen.get_best_config(template)
        except pyglet.window.NoSuchConfigException:
            template = pyglet.gl.Config()
            config = screen.get_best_config(template)
        # try and use FezContentManager if it works, failing back to directory reader
        try:
            content_manager = FezContentManager(sys.argv[1])
        except ReaderError:
            content_manager = ContentManager(sys.argv[1])
        AOWindow(content_manager=content_manager, asset_name=sys.argv[2], config=config)
        pyglet.app.run()
    else:
        print('show_ao.py Content|out objectao', file=sys.stderr)

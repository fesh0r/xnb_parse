"""trackball_camera.py - An OpenGL Trackball Camera Class for Pyglet

by Roger Allen, July 2008
roger@rogerandwendy.com

A class for simple-minded 3d example apps.

Usage:

Initialize with a radius from the center/focus point:

   tbcam = TrackballCamera(5.0)

After adjusting your projection matrix, set the modelview matrix.

   tbcam.update_modelview()

On each primary mouse click, scale the x & y to [-1,1] and call:

   tbcam.mouse_roll(x,y,False)

On each primary mouse drag, scale the x & y to [-1,1] and call:

   tbcam.mouse_roll(x,y)

Mouse movements adjust the modelview projection matrix directly.

"""

from __future__ import print_function

__version__ = "1.0"

# Code derived from the GLUT trackball.c, but now quite different and
# customized for pyglet.
#
# I simply wanted an easy-to-use trackball camera for quick-n-dirty
# opengl programs that I'd like to write.  Finding none, I grabbed
# the trackball.c code & started hacking.
#
# Originally implemented by Gavin Bell, lots of ideas from Thant Tessman
# and the August '88 issue of Siggraph's "Computer Graphics," pp. 121-129.
# and David M. Ciemiewicz, Mark Grossman, Henry Moreton, and Paul Haeberli
#
# Note: See the following for more information on quaternions:
#
# - Shoemake, K., Animating rotation with quaternion curves, Computer
#   Graphics 19, No 3 (Proc. SIGGRAPH'85), 245-254, 1985.
# - Pletinckx, D., Quaternion calculus as a basic tool in computer
#   graphics, The Visual Computer 5, 2-13, 1989.
#
# Gavin Bell's code had this copyright notice:
# (c) Copyright 1993, 1994, Silicon Graphics, Inc.
# ALL RIGHTS RESERVED
# Permission to use, copy, modify, and distribute this software for
# any purpose and without fee is hereby granted, provided that the above
# copyright notice appear in all copies and that both the copyright notice
# and this permission notice appear in supporting documentation, and that
# the name of Silicon Graphics, Inc. not be used in advertising
# or publicity pertaining to distribution of the software without specific,
# written prior permission.
#
# THE MATERIAL EMBODIED ON THIS SOFTWARE IS PROVIDED TO YOU "AS-IS"
# AND WITHOUT WARRANTY OF ANY KIND, EXPRESS, IMPLIED OR OTHERWISE,
# INCLUDING WITHOUT LIMITATION, ANY WARRANTY OF MERCHANTABILITY OR
# FITNESS FOR A PARTICULAR PURPOSE.  IN NO EVENT SHALL SILICON
# GRAPHICS, INC.  BE LIABLE TO YOU OR ANYONE ELSE FOR ANY DIRECT,
# SPECIAL, INCIDENTAL, INDIRECT OR CONSEQUENTIAL DAMAGES OF ANY
# KIND, OR ANY DAMAGES WHATSOEVER, INCLUDING WITHOUT LIMITATION,
# LOSS OF PROFIT, LOSS OF USE, SAVINGS OR REVENUE, OR THE CLAIMS OF
# THIRD PARTIES, WHETHER OR NOT SILICON GRAPHICS, INC.  HAS BEEN
# ADVISED OF THE POSSIBILITY OF SUCH LOSS, HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, ARISING OUT OF OR IN CONNECTION WITH THE
# POSSESSION, USE OR PERFORMANCE OF THIS SOFTWARE.
#
# US Government Users Restricted Rights
# Use, duplication, or disclosure by the Government is subject to
# restrictions set forth in FAR 52.227.19(c)(2) or subparagraph
# (c)(1)(ii) of the Rights in Technical Data and Computer Software
# clause at DFARS 252.227-7013 and/or in similar or successor
# clauses in the FAR or the DOD or NASA FAR Supplement.
# Unpublished-- rights reserved under the copyright laws of the
# United States.  Contractor/manufacturer is Silicon Graphics,
# Inc., 2011 N.  Shoreline Blvd., Mountain View, CA 94039-7311.

import math

from pyglet.gl import *


# a little vector library that is misused in odd ways below.

def v3add(vec1, vec2):
    return [vec1[0] + vec2[0],
            vec1[1] + vec2[1],
            vec1[2] + vec2[2]]


def v3sub(vec1, vec2):
    return [vec1[0] - vec2[0],
            vec1[1] - vec2[1],
            vec1[2] - vec2[2]]


def v3scale(vec, scale):
    return [vec[0] * scale,
            vec[1] * scale,
            vec[2] * scale]


def v3dot(vec1, vec2):
    return vec1[0] * vec2[0] + vec1[1] * vec2[1] + vec1[2] * vec2[2]


def v3cross(vec1, vec2):
    return [vec1[1] * vec2[2] - vec1[2] * vec2[1],
            vec1[2] * vec2[0] - vec1[0] * vec2[2],
            vec1[0] * vec2[1] - vec1[1] * vec2[0]]


def v3length(vec):
    return math.sqrt(vec[0] * vec[0] + vec[1] * vec[1] + vec[2] * vec[2])


def v3normalize(vec):
    try:
        return v3scale(vec, 1.0 / v3length(vec))
    except ZeroDivisionError:
        return vec


# Some quaternion routines

def q_add(quat1, quat2):
    """Given two quaternions, add them together to get a third quaternion.
    Adding quaternions to get a compound rotation is analagous to adding
    translations to get a compound translation.  When incrementally
    adding rotations, the first argument here should be the new rotation.
    """
    t1 = v3scale(quat1, quat2[3])
    t2 = v3scale(quat2, quat1[3])
    t3 = v3cross(quat2, quat1)
    tf = v3add(t1, t2)
    tf = v3add(t3, tf)
    tf.append(quat1[3] * quat2[3] - v3dot(quat1, quat2))
    return tf


def q_from_axis_angle(axis, phi):
    # axis is a 3-vector, quat is a 4-vector
    """Computes a quaternion based on an axis (defined by the given vector)
    and an angle about which to rotate.  The angle is expressed in radians.
    """
    quat = v3normalize(axis)
    quat = v3scale(quat, math.sin(phi / 2.0))
    quat.append(math.cos(phi / 2.0))
    return quat


def q_normalize(quat):
    """Return a normalized quaternion"""
    mag = quat[0] * quat[0] + quat[1] * quat[1] + quat[2] * quat[2] + quat[3] * quat[3]
    if mag != 0:
        for i in range(4):
            quat[i] /= mag
    return quat


def q_matrix(quat):
    """return the rotation matrix based on quat"""
    mat = [0.0] * 16
    mat[0 * 4 + 0] = 1.0 - 2.0 * (quat[1] * quat[1] + quat[2] * quat[2])
    mat[0 * 4 + 1] = 2.0 * (quat[0] * quat[1] - quat[2] * quat[3])
    mat[0 * 4 + 2] = 2.0 * (quat[2] * quat[0] + quat[1] * quat[3])
    mat[0 * 4 + 3] = 0.0

    mat[1 * 4 + 0] = 2.0 * (quat[0] * quat[1] + quat[2] * quat[3])
    mat[1 * 4 + 1] = 1.0 - 2.0 * (quat[2] * quat[2] + quat[0] * quat[0])
    mat[1 * 4 + 2] = 2.0 * (quat[1] * quat[2] - quat[0] * quat[3])
    mat[1 * 4 + 3] = 0.0

    mat[2 * 4 + 0] = 2.0 * (quat[2] * quat[0] - quat[1] * quat[3])
    mat[2 * 4 + 1] = 2.0 * (quat[1] * quat[2] + quat[0] * quat[3])
    mat[2 * 4 + 2] = 1.0 - 2.0 * (quat[1] * quat[1] + quat[0] * quat[0])
    mat[2 * 4 + 3] = 0.0

    mat[3 * 4 + 0] = 0.0
    mat[3 * 4 + 1] = 0.0
    mat[3 * 4 + 2] = 0.0
    mat[3 * 4 + 3] = 1.0
    return mat


def project_z(rad, x_c, y_c):
    """Project an x_c,y_c pair onto a sphere of radius rad OR a hyperbolic sheet
    if we are away from the center of the sphere.
    """
    dist = math.sqrt(x_c * x_c + y_c * y_c)
    if dist < rad * (math.sqrt(2.0) / 2.0):  # Inside sphere
        z_c = math.sqrt(rad * rad - dist * dist)
    else:                                # On hyperbola
        t = rad / math.sqrt(2.0)
        z_c = t * t / dist
    return z_c


def vec_args(*args):
    """GLfloat vector of args"""
    return (GLfloat * len(args))(*args)


def vec_mat(mat):
    """GLfloat vector of matrix"""
    return (GLfloat * len(mat))(*mat)


def norm1(val, max_val):
    """given x within [0, maxx], scale to a range [-1, 1]."""
    return (2.0 * val - float(max_val)) / float(max_val)


class TrackballCamera(object):
    """Trackball Camera Class"""

    def __init__(self, radius=2.0):
        """ initialize the camera, giving a radius from the focal point for
        the camera eye.  Update focal point & up via the update_modelview call.
        """
        # the quaternion storing the rotation
        self.rot_quat = [0.0, 0.0, 0.0, 1.0]
        # the last mouse update
        self.last_x = 0
        self.last_y = 0
        # camera vars
        self.cam_eye = [0.0, 0.0, radius]
        self.cam_focus = [0.0, 0.0, 0.0]
        self.cam_up = [0.0, 1.0, 0.0]
        # in add_quat routine, renormalize "sometimes"
        self.renorm_count = 97
        self.count = 0
        # Trackballsize should really be based on the distance from the center of
        # rotation to the point on the object underneath the mouse.  That
        # point would then track the mouse as closely as possible.  This is a
        # simple example, though, so that is left as an Exercise for the
        # Programmer.
        self.trackball_size = 1.0

    def mouse_roll(self, norm_mouse_x, norm_mouse_y, dragging=True):
        """When you click or drag the primary mouse button, scale the mouse
        x & y to the range [-1.0,1.0] and call this routine to roll the trackball
        and update the modelview matrix.

        The initial click should set dragging to False.
        """
        if dragging:
            norm_mouse_quat = self._rotate(norm_mouse_x, norm_mouse_y)
            self.rot_quat = q_add(norm_mouse_quat, self.rot_quat)
            self.count += 1
            if self.count > self.renorm_count:
                self.rot_quat = q_normalize(self.rot_quat)
                self.count = 0
            self.update_modelview()
        self.last_x = norm_mouse_x
        self.last_y = norm_mouse_y

    def mouse_zoom(self, norm_mouse_x, norm_mouse_y, dragging=True):
        """When you click or drag a secondary mouse button, scale the mouse
        x & y to the range [-1.0,1.0] and call this routine to change the
        trackball's camera radius and update the modelview matrix.

        The initial click should set dragging to False.
        """
        if self.last_x:
            d_x = norm_mouse_x - self.last_x
            d_y = norm_mouse_y - self.last_y
            norm_mouse_r_delta = 20.0 * math.sqrt(d_x * d_x + d_y * d_y)
            if d_y > 0.0:
                norm_mouse_r_delta = -norm_mouse_r_delta
            if dragging:
                self.cam_eye[2] += norm_mouse_r_delta
                if self.cam_eye[2] < 1.0:
                    self.cam_eye[2] = 1.0
                self.update_modelview()
        self.last_x = norm_mouse_x
        self.last_y = norm_mouse_y

    def update_modelview(self, cam_radius=None, cam_focus=None, cam_up=None):
        """Given a radius for the trackball camera, a focus-point 3-vector,
        another 3-vector the points 'up' combined with the current
        orientation of the trackball, update the GL_MODELVIEW matrix.
        """
        if cam_radius:
            self.cam_eye[2] = cam_radius
        if cam_focus:
            self.cam_focus = cam_focus
        if cam_up:
            self.cam_up = cam_up
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(self.cam_eye[0], self.cam_eye[1], self.cam_eye[2],
                  self.cam_focus[0], self.cam_focus[1], self.cam_focus[2],
                  self.cam_up[0], self.cam_up[1], self.cam_up[2])
        # rotate this view by the current orientation
        mat = self._matrix()
        glMultMatrixf(vec_mat(mat))

    def _matrix(self):
        """return the rotation matrix for the trackball"""
        return q_matrix(self.rot_quat)

    def _rotate(self, norm_mouse_x, norm_mouse_y):
        """Pass the x and y coordinates of the last and current positions of
        the mouse, scaled so they are in the range [-1.0,1.0].

        Simulate a track-ball.  Project the points onto the virtual
        trackball, then figure out the axis of rotation, which is the cross
        product of LAST NEW and O LAST (O is the center of the ball, 0,0,0)
        Note:  This is a deformed trackball-- is a trackball in the center,
        but is deformed into a hyperbolic sheet of rotation away from the
        center.  This particular function was chosen after trying out
        several variations.
        """
        # handle special case
        if self.last_x == norm_mouse_x and self.last_y == norm_mouse_y:
            # Zero rotation
            return [0.0, 0.0, 0.0, 1.0]

        #
        # First, figure out z-coordinates for projection of P1 and P2 to
        # deformed sphere
        #
        last = [self.last_x, self.last_y, project_z(self.trackball_size, self.last_x, self.last_y)]
        new = [norm_mouse_x, norm_mouse_y, project_z(self.trackball_size, norm_mouse_x, norm_mouse_y)]

        #
        # Now, we want the cross product of LAST and NEW
        # aka the axis of rotation
        #
        axis = v3cross(new, last)

        #
        # Figure out how much to rotate around that axis (phi)
        #
        diff = v3sub(last, new)
        t = v3length(diff) / (2.0 * self.trackball_size)
        # Avoid problems with out-of-control values...
        if t > 1.0:
            t = 1.0
        if t < -1.0:
            t = -1.0
        phi = 2.0 * math.asin(t)

        return q_from_axis_angle(axis, phi)

# CENG 487 Assignment2 by
# Bülent Arda Yılmaz
# StudentId: 270201019
# November 2022

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
from object import Object
from vec3d import Vec3d
import numpy as np

#Reference: https://gist.github.com/gyng/8939105

class Torus:

    def __init__(self, ring_r, tube_r, r_seg, c_seg, transformation_stack, position, subdivision_level):
        self.ring_r = ring_r
        self.tube_r = tube_r
        self.r_seg = r_seg
        self.c_seg = c_seg
        self.transformation_stack = transformation_stack
        self.position = position
        self.subdivision_level = subdivision_level
        self.objects = self.init_torus()
        
    def init_torus(self):
        pi = np.pi
        tau = pi * 2
        vertices = []
        for i in range(self.r_seg):
            points = np.array([])
            for j in range(self.c_seg + 1):
                for k in [0, 1]:
                    s = (i + k) % self.r_seg + 0.5
                    t = j + (self.c_seg + 1)

                    x = (self.tube_r + self.ring_r * np.cos(np.radians(s * tau / self.r_seg)) * np.cos(t * tau / self.c_seg))
                    y = self.ring_r * np.sin(np.radians(s * tau / self.r_seg))
                    z = (self.tube_r + self.ring_r * np.cos(np.radians(s * tau / self.r_seg)) * np.sin(t * tau / self.c_seg))

                    point = Vec3d(x, y, z, 1)
                    points = np.append(points, point)
            vertex = Object(points, self.transformation_stack, [[np.random.random(), np.random.random(), np.random.random()]], GL_QUADS, self.position)
            vertices.append(vertex)
        return vertices

    def re_init(self):
        pass
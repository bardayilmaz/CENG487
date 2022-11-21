# CENG 487 Assignment2 by
# Bülent Arda Yılmaz
# StudentId: 270201019
# November 2022

# Reference: https://gist.github.com/nikAizuddin/5ea402e9073f1ef76ba6
# I made some changes to draw cylinder using quads.

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
from object import Object
from vec3d import Vec3d
import numpy as np

class Cylinder:

    def __init__(self, radius, height, transformation_stack, position, side_count, subdivision_level = 1):
        self.radius = radius
        self.height = height
        self.transformation_stack = transformation_stack
        self.position = position
        self.side_count = side_count
        self.subdivision_level = subdivision_level
        self.tube = self.init_tube()

        self.lower_circle = Object(self.init_lower_circle(), self.transformation_stack, [[np.random.random(), np.random.random(), np.random.random()]], GL_POLYGON, self.position)
        self.upper_circle = Object(self.init_upper_circle(), self.transformation_stack, [[np.random.random(), np.random.random(), np.random.random()]], GL_POLYGON, self.position)
        self.objects = np.append(self.tube, [self.lower_circle, self.upper_circle])

    def init_tube(self):
        angle = 0
        angle_step_size = 360.0 / self.side_count
        quads = np.array([])
        counter = 0
        while angle <= 360:
            vertices = np.array([])
            x = self.radius * np.cos(np.radians(angle))
            z = self.radius * np.sin(np.radians(angle))
            vertices = np.append(vertices, Vec3d(x, self.height, z, 1))
            vertices = np.append(vertices, Vec3d(x, 0.0 , z, 1))
            angle += angle_step_size
            x = self.radius * np.cos(np.radians(angle))
            z = self.radius * np.sin(np.radians(angle))
            vertices = np.append(vertices, Vec3d(x, self.height, z, 1))
            vertices = np.append(vertices, Vec3d(x, 0.0 , z, 1))
            quads = np.append(quads, Object(vertices, self.transformation_stack, [[np.random.random(), np.random.random(), np.random.random()]], GL_QUAD_STRIP, self.position))

        subdivided_vertices = []
        if self.subdivision_level > 1:
            for quad in quads:
                subdivided_vertices = self.subdivide_quad(quad, self.subdivision_level, subdivided_vertices)
        else:
            subdivided_vertices = quads
        vertices = np.array([])
        vertices = np.append(vertices, Vec3d(self.radius, self.height, 0.0, 1))
        vertices = np.append(vertices, Vec3d(self.radius, 0.0, 0.0, 1))
        
        subdivided_vertices = np.append(subdivided_vertices, Object(vertices, self.transformation_stack, [[np.random.random(), np.random.random(), np.random.random()]], GL_QUAD_STRIP, self.position))
        return subdivided_vertices
        
    def init_lower_circle(self):
        x = 0
        z = 0
        angle = 0
        angle_step_size = 360.0 / self.side_count
        vertices = np.array([])
        while angle <= 360:
            x = self.radius * np.cos(np.radians(angle))
            z = self.radius * np.sin(np.radians(angle))
            vertices = np.append(vertices, Vec3d(x, 0.0, z, 1))
            angle += angle_step_size
        vertices = np.append(vertices, Vec3d(self.radius, 0.0, 0.0, 1))
        return vertices

    def init_upper_circle(self):
        x = 0
        z = 0
        angle = 0
        angle_step_size = 360.0 / self.side_count
        vertices = np.array([])
        while angle <= 360:
            x = self.radius * np.cos(np.radians(angle))
            z = self.radius * np.sin(np.radians(angle))
            vertices = np.append(vertices, Vec3d(x, self.height, z, 1))
            angle += angle_step_size
        vertices = np.append(vertices, Vec3d(self.radius, self.height, 0.0, 1))
        return vertices

    def subdivide_quad(self, obj_quad, level, new_arr = np.array([])):
        if level == 1:
            return obj_quad
        vertice = obj_quad.vertices
        v12x = 0.5 * (vertice[0].x + vertice[1].x)
        v12y = 0.5 * (vertice[0].y + vertice[1].y)
        v12z = 0.5 * (vertice[0].z + vertice[1].z)

        v24x = 0.5 * (vertice[1].x + vertice[3].x)
        v24y = 0.5 * (vertice[1].y + vertice[3].y)
        v24z = 0.5 * (vertice[1].z + vertice[3].z)

        v13x = 0.5 * (vertice[0].x + vertice[2].x)
        v13y = 0.5 * (vertice[0].y + vertice[2].y)
        v13z = 0.5 * (vertice[0].z + vertice[2].z)

        v34x = 0.5 * (vertice[2].x + vertice[3].x)
        v34y = 0.5 * (vertice[2].y + vertice[3].y)
        v34z = 0.5 * (vertice[2].z + vertice[3].z)

        midx = 0.25 * (vertice[0].x + vertice[1].x + vertice[2].x + vertice[3].x)
        midy = 0.25 * (vertice[0].y + vertice[1].y + vertice[2].y + vertice[3].y)
        midz = 0.25 * (vertice[0].z + vertice[1].z + vertice[2].z + vertice[3].z)

        new_arr = np.append(new_arr, self.subdivide_quad(Object(
            [
                Vec3d(v24x, v24y, v24z, 1),
                Vec3d(vertice[1].x, vertice[1].y, vertice[1].z, 1),
                Vec3d(midx, midy, midz, 1),
                Vec3d(v12x, v12y, v12z, 1)
            ], obj_quad.transformation_stack,
            [[np.random.random(), np.random.random(), np.random.random(), np.random.random()]],
            obj_quad.type,
            obj_quad.position), level-1))

        new_arr = np.append(new_arr, self.subdivide_quad(Object(
            [   
                Vec3d(v12x, v12y, v12z, 1),
                Vec3d(vertice[0].x, vertice[0].y, vertice[0].z, 1),
                Vec3d(midx, midy, midz, 1),
                Vec3d(v13x, v13y, v13z, 1)
            ], obj_quad.transformation_stack,
            [[np.random.random(), np.random.random(), np.random.random(), np.random.random()]],
            obj_quad.type,
            obj_quad.position), level-1))
        
        new_arr = np.append(new_arr, self.subdivide_quad(Object(
            [
                Vec3d(v13x, v13y, v13z, 1),
                Vec3d(vertice[2].x, vertice[2].y, vertice[2].z, 1),
                Vec3d(midx, midy, midz, 1),
                Vec3d(v34x, v34y, v34z, 1)
            ], obj_quad.transformation_stack,
            [[np.random.random(), np.random.random(), np.random.random(), np.random.random()]],
            obj_quad.type,
            obj_quad.position), level-1))
        
        new_arr = np.append(new_arr, self.subdivide_quad(Object(
            [
                Vec3d(v34x, v34y, v34z, 1),
                Vec3d(vertice[3].x, vertice[3].y, vertice[3].z, 1),
                Vec3d(midx, midy, midz, 1),
                Vec3d(v24x, v24y, v24z, 1)
            ], obj_quad.transformation_stack,
            [[np.random.random(), np.random.random(), np.random.random(), np.random.random()]],
            obj_quad.type,
            obj_quad.position), level-1))

        return new_arr

    def re_init(self):
        self.tube = self.init_tube()
        self.lower_circle = Object(self.init_lower_circle(), self.transformation_stack, [[np.random.random(), np.random.random(), np.random.random()]], GL_POLYGON, self.position)
        self.upper_circle = Object(self.init_upper_circle(), self.transformation_stack, [[np.random.random(), np.random.random(), np.random.random()]], GL_POLYGON, self.position)
        self.objects = np.append(self.tube, [self.lower_circle, self.upper_circle])
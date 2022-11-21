# CENG 487 Assignment2 by
# Bülent Arda Yılmaz
# StudentId: 270201019
# November 2022

# References:
# https://stackoverflow.com/questions/26790422/recursive-subdivision-on-octahedron-in-opengl

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
from mat3d import Mat3d
from object import Object
from vec3d import Vec3d
import numpy as np


class Cube:
    def __init__(self, transformation_stack, position, side_length, subdivision_level = 1):
        self.transformation_stack = transformation_stack
        self.position = position
        self.side_length = side_length
        self.subdivision_level = subdivision_level
        self.objects = self.init_cube()

    def init_cube(self):
        length = self.side_length/2.0
        points = np.array([])
        orders = [[1,5,4,0], [2,6,7,3], [0,4,6,2], [3,7,5,1], [4,5,7,6], [1,0,2,3]]
        for i in [length, -length]:
            for j in [length, -length]:
                for k in [length, -length]:
                    point = Vec3d(i, j, k, 1)
                    points = np.append(points, point)
        vertices = np.array([])
        for order in orders:
            obj = Object([points[order[0]], points[order[1]], points[order[2]], points[order[3]]], self.transformation_stack, [[np.random.random(), np.random.random(), np.random.random()]], GL_QUADS, self.position)
            vertices = np.append(vertices, obj)
        subdivided_vertices = []
        if self.subdivision_level > 1:
            for vertice in vertices:
                subdivided_vertices = self.subdivide_quad(vertice, self.subdivision_level, subdivided_vertices)
        else:
            subdivided_vertices = vertices
        return subdivided_vertices
        
    def subdivide_quad(self, obj_quad, level, new_arr = np.array([])):
        if level == 1:
            return obj_quad
        vertice = obj_quad.vertices
        v12x = 0.5 * (vertice[0].x + vertice[1].x)
        v12y = 0.5 * (vertice[0].y + vertice[1].y)
        v12z = 0.5 * (vertice[0].z + vertice[1].z)

        v23x = 0.5 * (vertice[1].x + vertice[2].x)
        v23y = 0.5 * (vertice[1].y + vertice[2].y)
        v23z = 0.5 * (vertice[1].z + vertice[2].z)

        v14x = 0.5 * (vertice[0].x + vertice[3].x)
        v14y = 0.5 * (vertice[0].y + vertice[3].y)
        v14z = 0.5 * (vertice[0].z + vertice[3].z)

        v34x = 0.5 * (vertice[2].x + vertice[3].x)
        v34y = 0.5 * (vertice[2].y + vertice[3].y)
        v34z = 0.5 * (vertice[2].z + vertice[3].z)

        midx = 0.25 * (vertice[0].x + vertice[1].x + vertice[2].x + vertice[3].x)
        midy = 0.25 * (vertice[0].y + vertice[1].y + vertice[2].y + vertice[3].y)
        midz = 0.25 * (vertice[0].z + vertice[1].z + vertice[2].z + vertice[3].z)

        new_arr = np.append(new_arr, self.subdivide_quad(Object(
            [
                Vec3d(v23x, v23y, v23z, 1),
                Vec3d(vertice[1].x, vertice[1].y, vertice[1].z, 1),
                Vec3d(v12x, v12y, v12z, 1),
                Vec3d(midx, midy, midz, 1)
            ], obj_quad.transformation_stack,
            [[np.random.random(), np.random.random(), np.random.random(), np.random.random()]],
            obj_quad.type,
            obj_quad.position), level-1))

        new_arr = np.append(new_arr, self.subdivide_quad(Object(
            [   
                Vec3d(v12x, v12y, v12z, 1),
                Vec3d(vertice[0].x, vertice[0].y, vertice[0].z, 1),
                Vec3d(v14x, v14y, v14z, 1),
                Vec3d(midx, midy, midz, 1),
            ], obj_quad.transformation_stack,
            [[np.random.random(), np.random.random(), np.random.random(), np.random.random()]],
            obj_quad.type,
            obj_quad.position), level-1))
        
        new_arr = np.append(new_arr, self.subdivide_quad(Object(
            [
                Vec3d(v23x, v23y, v23z, 1),
                Vec3d(vertice[2].x, vertice[2].y, vertice[2].z, 1),
                Vec3d(v34x, v34y, v34z, 1),
                Vec3d(midx, midy, midz, 1)
            ], obj_quad.transformation_stack,
            [[np.random.random(), np.random.random(), np.random.random(), np.random.random()]],
            obj_quad.type,
            obj_quad.position), level-1))
        
        new_arr = np.append(new_arr, self.subdivide_quad(Object(
            [
                Vec3d(v14x, v14y, v14z, 1),
                Vec3d(vertice[3].x, vertice[3].y, vertice[3].z, 1),
                Vec3d(v34x, v34y, v34z, 1),
                Vec3d(midx, midy, midz, 1)
            ], obj_quad.transformation_stack,
            [[np.random.random(), np.random.random(), np.random.random(), np.random.random()]],
            obj_quad.type,
            obj_quad.position), level-1))

        return new_arr

    def re_init(self):
        self.objects = self.init_cube()
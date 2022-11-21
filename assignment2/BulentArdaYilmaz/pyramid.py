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

class Pyramid:

    def __init__(self, transformation_stack, position, height, subdivision_level):
        self.transformation_stack = transformation_stack
        self.position = position
        self.height = height
        self.subdivision_level = subdivision_level
        self.objects = self.init_pyramid()

    def init_pyramid(self):
        points = np.array([])
        for x in [self.height, -self.height]:
            for z in [self.height, -self.height]:
                points = np.append(points, Vec3d(x, -self.height, z, 1))
        points = np.append(points, Vec3d(0, self.height, 0, 1))
        vertices = np.array([])
        orders = [[4, 1, 0], [4, 1, 3], [4, 3, 2], [4, 2, 0], [1, 0, 2, 3]]

        for order in orders:
            obj = 0
            if len(order) == 3:
                obj = Object([points[order[0]], points[order[1]], points[order[2]]], self.transformation_stack, [[np.random.random(), np.random.random(), np.random.random()]], GL_POLYGON, self.position)
            else:
                obj = Object([points[order[0]], points[order[1]], points[order[2]], points[order[3]]], self.transformation_stack,  [[np.random.random(), np.random.random(), np.random.random(), np.random.random()]], GL_QUADS, self.position)
            vertices = np.append(vertices, obj)
        # Subdivision process
        subdivided_vertices = []
        if self.subdivision_level > 1:
            for vertice in vertices:
                if len(vertice.vertices) == 3:
                    subdivided_vertices = self.subdivide_triangle(vertice, self.subdivision_level, subdivided_vertices)
                elif len(vertice.vertices) == 4:
                    subdivided_vertices = self.subdivide_quad(vertice, self.subdivision_level, subdivided_vertices)
        else:
            subdivided_vertices = vertices
        return subdivided_vertices

    def subdivide_triangle(self, obj_triangle, level, new_arr = np.array([])):
        if level == 1:
            return obj_triangle

        vertice = obj_triangle.vertices
        v12x = 0.5 * (vertice[0].x + vertice[1].x)
        v12y = 0.5 * (vertice[0].y + vertice[1].y)
        v12z = 0.5 * (vertice[0].z + vertice[1].z)

        v13x = 0.5 * (vertice[0].x + vertice[2].x)
        v13y = 0.5 * (vertice[0].y + vertice[2].y)
        v13z = 0.5 * (vertice[0].z + vertice[2].z)

        v23x = 0.5 * (vertice[1].x + vertice[2].x)
        v23y = 0.5 * (vertice[1].y + vertice[2].y)
        v23z = 0.5 * (vertice[1].z + vertice[2].z)

        
        new_arr = np.append(new_arr, self.subdivide_triangle(Object(
            [
                Vec3d(vertice[0].x, vertice[0].y, vertice[0].z, 1),
                Vec3d(v12x, v12y, v12z, 1),
                Vec3d(v13x, v13y, v13z, 1)
            ], obj_triangle.transformation_stack,
            [[np.random.random(), np.random.random(), np.random.random(), np.random.random()]],
            obj_triangle.type,
            obj_triangle.position), level-1))

        new_arr = np.append(new_arr, self.subdivide_triangle(Object(
            [   
                Vec3d(v12x, v12y, v12z, 1),
                Vec3d(vertice[1].x, vertice[1].y, vertice[1].z, 1),
                Vec3d(v23x, v23y, v23z, 1)
            ], obj_triangle.transformation_stack,
            [[np.random.random(), np.random.random(), np.random.random(), np.random.random()]],
            obj_triangle.type,
            obj_triangle.position), level-1))
        
        new_arr = np.append(new_arr, self.subdivide_triangle(Object(
            [
                Vec3d(v13x, v13y, v13z, 1),
                Vec3d(v23x, v23y, v23z, 1),
                Vec3d(vertice[2].x, vertice[2].y, vertice[2].z, 1)
            ], obj_triangle.transformation_stack,
            [[np.random.random(), np.random.random(), np.random.random(), np.random.random()]],
            obj_triangle.type,
            obj_triangle.position), level-1))
        
        new_arr = np.append(new_arr, self.subdivide_triangle(Object(
            [
                Vec3d(v12x, v12y, v12z, 1),
                Vec3d(v23x, v23y, v23z, 1),
                Vec3d(v13x, v13y, v13z, 1)
            ], obj_triangle.transformation_stack,
            [[np.random.random(), np.random.random(), np.random.random(), np.random.random()]],
            obj_triangle.type,
            obj_triangle.position), level-1))
        return new_arr

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
        self.objects = self.init_pyramid()
    

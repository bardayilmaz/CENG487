# CENG 487 Assignment2 by
# Bülent Arda Yılmaz
# StudentId: 270201019
# November 2022

from vec3d import Vec3d
from object import Object
import numpy as np

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

#References: 
# http://www.songho.ca/opengl/gl_sphere.html

class Sphere:

    def __init__(self, radius, sector_count, stack_count, transformation_stack, position, subdivision_level):
        self.radius = radius
        self.sector_count = sector_count
        self.stack_count = stack_count
        self.transformation_stack = transformation_stack
        self.position = position
        self.subdivision_level = subdivision_level
        self.objects = self.init_sphere()
        

    def init_vertices(self):
        vertices = np.array([])
        sector_step = 2 * np.pi / self.sector_count
        stack_step = 2 * np.pi / self.stack_count

        for i in range(self.stack_count + 1):
            stack_angle = (np.pi / 2) - (i * stack_step)
            xy = self.radius * np.cos(stack_angle)
            z = self.radius * np.sin(stack_angle)

            for j in range(self.sector_count + 1):
                sector_angle = j * sector_step
                x = xy * np.cos(sector_angle)
                y = xy * np.sin(sector_angle)

                vertices = np.append(vertices, Vec3d(x, y, z, 1))

        return vertices

    def init_sphere(self):
        indices = []
        vertices = self.init_vertices()

        for i in range(self.stack_count):
            k1 = i * (self.sector_count + 1)
            k2 = k1 + self.sector_count + 1

            for j in range(self.sector_count + 1):
                if i != 0:
                    indices.append([k1, k2, k1 + 1])
                if i != (self.stack_count -1):
                    indices.append([k1 + 1, k2, k2 + 1])

                k1 += 1
                k2 += 1

        triangles = np.array([])
        for i in range(len(indices)):
            triangles = np.append(triangles, Object([
                Vec3d(vertices[indices[i][0]].x, vertices[indices[i][0]].y, vertices[indices[i][0]].z, 1),
                Vec3d(vertices[indices[i][1]].x, vertices[indices[i][1]].y, vertices[indices[i][1]].z, 1),
                Vec3d(vertices[indices[i][2]].x, vertices[indices[i][2]].y, vertices[indices[i][2]].z, 1)
            ], self.transformation_stack, [[np.random.random(), np.random.random(), np.random.random()]], GL_POLYGON, self.position))

        subdivided_vertices = []
        if self.subdivision_level > 1:
            for triangle in triangles:
                subdivided_vertices = self.subdivide_triangle(triangle, self.subdivision_level, subdivided_vertices)
        else:
            subdivided_vertices = triangles
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

    def re_init(self):
        self.objects = self.init_sphere()
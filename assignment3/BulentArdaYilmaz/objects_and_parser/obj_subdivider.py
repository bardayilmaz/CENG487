# CENG 487 Assignment3 by
# Bülent Arda Yılmaz
# StudentId: 270201019
# November 2022

from object import Object
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from mat3d import Mat3d
from vec3d import Vec3d
import numpy as np

class ObjSubdivier:

    @staticmethod
    def subdivide_increase(obj_list):
        subdivided_vertices = []
        for obj in obj_list:
            vertice = obj.vertices
            v01x = 0.5 * (vertice[0].x + vertice[1].x)
            v01y = 0.5 * (vertice[0].y + vertice[1].y)
            v01z = 0.5 * (vertice[0].z + vertice[1].z)

            v12x = 0.5 * (vertice[1].x + vertice[2].x)
            v12y = 0.5 * (vertice[1].y + vertice[2].y)
            v12z = 0.5 * (vertice[1].z + vertice[2].z)

            v23x = 0.5 * (vertice[2].x + vertice[3].x)
            v23y = 0.5 * (vertice[2].y + vertice[3].y)
            v23z = 0.5 * (vertice[2].z + vertice[3].z)

            v03x = 0.5 * (vertice[0].x + vertice[3].x)
            v03y = 0.5 * (vertice[0].y + vertice[3].y)
            v03z = 0.5 * (vertice[0].z + vertice[3].z)

            midx = 0.25 * (vertice[0].x + vertice[1].x + vertice[2].x + vertice[3].x)
            midy = 0.25 * (vertice[0].y + vertice[1].y + vertice[2].y + vertice[3].y)
            midz = 0.25 * (vertice[0].z + vertice[1].z + vertice[2].z + vertice[3].z)

            subdivided_vertices.append(Object(
                [
                    Vec3d(vertice[0].x, vertice[0].y, vertice[0].z, 1),
                    Vec3d(v01x, v01y, v01z, 1),
                    Vec3d(midx, midy, midz, 1),
                    Vec3d(v03x, v03y, v03z, 1)
                ],
                obj.transformation_stack, [[np.random.random(), np.random.random(), np.random.random()]], obj.type,
                obj.position
            ))

            subdivided_vertices.append(Object(
                [
                    Vec3d(v01x, v01y, v01z, 1),
                    Vec3d(vertice[1].x, vertice[1].y, vertice[1].z, 1),
                    Vec3d(v12x, v12y, v12z, 1),
                    Vec3d(midx, midy, midz, 1)
                ],
                obj.transformation_stack, [[np.random.random(), np.random.random(), np.random.random()]], obj.type,
                obj.position
            ))

            subdivided_vertices.append(Object(
                [
                    Vec3d(midx, midy, midz, 1),
                    Vec3d(v12x, v12y, v12z, 1),
                    Vec3d(vertice[2].x, vertice[2].y, vertice[2].z, 1),
                    Vec3d(v23x, v23y, v23z, 1)
                ],
                obj.transformation_stack, [[np.random.random(), np.random.random(), np.random.random()]], obj.type,
                obj.position))

            subdivided_vertices.append(Object(
                [
                    Vec3d(v03x, v03y, v03z, 1),
                    Vec3d(midx, midy, midz, 1),
                    Vec3d(v23x, v23y, v23z, 1),
                    Vec3d(vertice[3].x, vertice[3].y, vertice[3].z, 1),
                ],
                obj.transformation_stack, [[np.random.random(), np.random.random(), np.random.random()]], obj.type,
                obj.position))

        return subdivided_vertices

    @staticmethod
    def subdivice_decrease(obj_list):
        subdivided_vertices = []
        counter = 0
        vertices = []
        for obj in obj_list:
            vertices.append(obj.vertices[counter])
            counter += 1
            if counter == 4:
                object = Object(vertices, obj.transformation_stack, [[np.random.random(), np.random.random(), np.random.random()]], obj.type, obj.position)
                subdivided_vertices.append(object)
                vertices = []
                counter = 0
        return subdivided_vertices

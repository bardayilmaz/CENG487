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

class ObjCreator:
    
    # Static method create takes
    #   vertex array
    #   index array
    #   type (not used currently)
    # and returns an array of Objects to be drawed by Scene
    # Assumes length of vertices and indices are same
    @staticmethod
    def create(vertices, indices, type, transformation_stack, position):
        objects = []
        for i in range(len(indices)):
            if len(indices[i]) == 4:
                type = GL_QUADS
            else:
                type = GL_POLYGON
            points = []
            for j in indices[i]:
                v = vertices[j]
                points.append(Vec3d(v[0], v[1], v[2], 1))
            obj = Object(points, transformation_stack, [[np.random.random(), np.random.random(), np.random.random()]], type, position)
            objects.append(obj)
        return objects
            


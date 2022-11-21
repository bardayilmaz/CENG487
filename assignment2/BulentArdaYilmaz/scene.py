# CENG 487 Assignment1 by
# Bülent Arda Yılmaz
# StudentId: 270201019
# October 2022

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
from vec3d import Vec3d
from mat3d import Mat3d
from object import Object


class Scene:

    def __init__(self, objects):
        self.objects = objects

    def draw_objects(self):
        for j in range(len(self.objects)):
            glLoadIdentity()    # Reset The View
            pos = self.objects[j].position
            glTranslatef(pos.x, pos.y, pos.z)
            glBegin(self.objects[j].type)
            for i in range(len(self.objects[j].vertices)):
                if i < len(self.objects[j].colors):
                    colors = self.objects[j].colors[i]
                    glColor3f(colors[0], colors[1], colors[2])
                vertex = self.objects[j].vertices[i]
                glVertex3f(vertex.x, vertex.y, vertex.z)
            glEnd()

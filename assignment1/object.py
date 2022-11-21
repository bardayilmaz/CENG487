# CENG 487 Assignment1 by
# Bülent Arda Yılmaz
# StudentId: 270201019
# November 2022

from vec3d import vec3d
from mat3d import mat3d
import numpy as np

class object:

    def __init__(self, vertices, transformation_stack, colors, type, position):
        self.vertices = vertices
        self.transformation_stack = transformation_stack
        self.colors = colors
        self.type = type
        self.position = position

    def apply_transformations(self):
        for j in range(len(self.transformation_stack)):
            for i in range(len(self.vertices)):
                result = (self.transformation_stack[j]).matrix_multiplication(self.vertices[i].to_array())
                self.vertices[i] = vec3d(result.matrix[0], result.matrix[1], result.matrix[2], result.matrix[3])

    def add_transformation(self, matrix):
        self.transformation_stack.add(matrix)


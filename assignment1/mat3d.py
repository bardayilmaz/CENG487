# CENG 487 Assignment1 by
# Bülent Arda Yılmaz
# StudentId: 270201019
# October 2022

import numpy as np
from vec3d import vec3d

class mat3d:

    def __init__(self, matrix):
        self.matrix = matrix

    def transform(self, matrix):
        return self.matrix_multiplication(self, matrix)

    @staticmethod
    def scale_vec3d(sx, sy, sz, vector):
        return vec3d(vector.x * sx, vector.y * sy, vector.z * sz, vector.w)

    @staticmethod
    def translate_vec3d(dx, dy, dz, vector):
        matrix = mat3d(
            np.array([
                [1, 0, 0, dx],
                [0, 1, 0, dy],
                [0, 0, 1, dz],
                [0, 0, 0, 1]]))
        result = matrix.matrix_multiplication(vector.to_array()).matrix
        return vec3d(result[0], result[1], result[2], result[3])

    @staticmethod
    def rotate_x_vec3d(angle, vector):
        matrix = mat3d(
            np.array([
                [1, 0, 0, 0],
                [0, np.cos(np.degrees(angle)), -np.sin(np.degrees(angle)), 0],
                [0, np.sin(np.degrees(angle)), np.cos(np.degrees(angle)), 0],
                [0, 0, 0, 1]]))
        result = matrix.matrix_multiplication(vector.to_array()).matrix
        return vec3d(result[0], result[1], result[2], result[3])

    @staticmethod
    def rotate_y_vec3d(angle, vector):
        matrix = mat3d(
            np.array([
                [np.cos(np.degrees(angle)), 0, np.sin(np.degrees(angle)), 0],
                [0, 1, 0, 0],
                [-np.sin(np.degrees(angle)), 0, np.cos(np.degrees(angle)), 0],
                [0, 0, 0, 1]]))
        result = matrix.matrix_multiplication(vector.to_array()).matrix
        return vec3d(result[0], result[1], result[2], result[3])

    @staticmethod
    def rotate_z_vec3d(angle, vector):
        matrix = mat3d(
            np.array([
                [np.cos(np.degrees(angle)), -np.sin(np.degrees(angle)), 0, 0],
                [np.sin(np.degrees(angle)), np.cos(np.degrees(angle)), 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1]]))
        result = matrix.matrix_multiplication(vector.to_array()).matrix
        return vec3d(result[0], result[1], result[2], result[3])

    @staticmethod
    def get_translation_matrix(dx, dy, dz):
        return mat3d(np.array([
            [1, 0, 0, dx],
            [0, 1, 0, dy],
            [0, 0, 1, dz],
            [0, 0, 0, 1]]))

    @staticmethod
    def get_scale_matrix(sx, sy, sz):
        return mat3d(np.array([
            [sx, 0, 0, 0],
            [0, sy, 0, 0],
            [0, 0, sz, 0],
            [0, 0, 0, 1]]))

    @staticmethod
    def get_rotation_x_matrix(angle):
        return mat3d(
            np.array([
            [np.cos(np.degrees(angle)), -np.sin(np.degrees(angle)), 0, 0],
            [np.sin(np.degrees(angle)), np.cos(np.degrees(angle)), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]]))

    @staticmethod
    def get_rotation_y_matrix(angle):
        return mat3d(
            np.array([
            [np.cos(np.degrees(angle)), 0, np.sin(np.degrees(angle)), 0],
            [0, 1, 0, 0],
            [-np.sin(np.degrees(angle)), 0, np.cos(np.degrees(angle)), 0],
            [0, 0, 0, 1]]))

    @staticmethod
    def get_rotation_z_matrix(angle):
        return mat3d(
            np.array([
            [np.cos(np.degrees(angle)), -np.sin(np.degrees(angle)), 0, 0],
            [np.sin(np.degrees(angle)), np.cos(np.degrees(angle)), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]]))

    def matrix_multiplication(self, matrix):
        size = 0
        result_matrix = 0
        is_vector = False
        if np.ndim(matrix) == 1: # if vector
            size = 1
            is_vector = True
            matrix = np.array([[matrix[0]], [matrix[1]], [matrix[2]], [matrix[3]]])
            result_matrix = np.zeros(4)
        else:
            size = len(matrix[0])
            result_matrix = np.array([np.zeros(4), np.zeros(4), np.zeros(4), np.zeros(4)])

        for i in range(len(self.matrix)):
            for j in range(size):
                for k in range(len(matrix)):
                    if is_vector:
                        result_matrix[i] += self.matrix[i][k] * matrix[k][0]
                    else:
                        result_matrix[i][j] += self.matrix[i][k] * matrix[k][j]
        return mat3d(result_matrix)            

    def transpose(self):
        result_matrix = np.array([np.zeros(4), np.zeros(4), np.zeros(4), np.zeros(4)])
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix)):
                result_matrix[j][i] = self.matrix[i][j]
        return result_matrix
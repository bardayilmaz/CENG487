# CENG 487 Assignment2 by
# Bülent Arda Yılmaz
# StudentId: 270201019
# November 2022

import numpy as np
from mat3d import Mat3d

class Camera:

    def __init__(self, location, target):
        self.location = location
        self.target = target
        self.inverses_of_past_transformations = None

    # Returns a matrix for scene tranformation
    def get_camera_translate(self, amountX, amountY, amountZ):
        self.location = Mat3d.translate_Vec3d(amountX, amountY, amountZ, self.location)
        return Mat3d.get_translation_matrix(-amountX, -amountY, -amountZ)

    def get_camera_rotate_y(self, angle):
        self.location = Mat3d.rotate_y_Vec3d(angle, self.location)
        return Mat3d(Mat3d.get_rotation_y_matrix(angle).transpose())

    def get_camera_rotate_x(self, angle):
        self.location = Mat3d.rotate_x_Vec3d(angle, self.location)
        return Mat3d(Mat3d.get_rotation_x_matrix(angle).transpose())

    def get_camera_rotate_z(self, angle):
        self.location = Mat3d.rotate_z_Vec3d(angle, self.location)
        return Mat3d(Mat3d.get_rotation_z_matrix(angle).transpose())

    def get_camera_scale(self, scaleX, scaleY, scaleZ):
        self.location = Mat3d.scale_Vec3d(scaleX, scaleY, scaleZ, self.location)
        return Mat3d(Mat3d.get_scale_matrix(scaleX, scaleY, scaleZ))
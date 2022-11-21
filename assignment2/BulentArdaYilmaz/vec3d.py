# CENG 487 Assignment1 by
# Bülent Arda Yılmaz
# StudentId: 270201019
# October 2022

import numpy

class Vec3d:
    def __init__(self, x, y, z, w):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def __str__(self):
        return f"[x:" + str(self.x) + ", y:" + str(self.y) + ", z:" + str(self.z) + ", w:" + str(self.w) + "]" 

    def dot_product(self, x, y, z):
        return self.x * x + self.y * y + self.z * z

    def cross_product(self, x, y, z):
        result_x = self.y * z - self.z * y
        result_y = self.z * x - self.x * z
        result_z = self.x * y - self.y * x
        return Vec3d(result_x, result_y, result_z, self.w)
    
    def angle_between(self, x, y, z):
        dot_product = self.dot_product(x, y, z)
        self_len = self.get_length()
        other_len = Vec3d(x, y, z, self.w).get_length()
        angle = numpy.arccos(dot_product / (self_len * other_len))
        return numpy.degrees(angle)

    def get_length(self):
        len_squ = self.dot_product(self.x, self.y, self.z)
        return numpy.sqrt(numpy.abs(len_squ))
    
    def scalar_multiplication(self, rate):
        new_x = rate * self.x
        new_y = rate * self.y
        new_z = rate * self.z
        return Vec3d(new_x, new_y, new_z, self.w)

    def add_vector(self, x, y, z):
        return Vec3d(self.x + x, self.y + y, self.z + z, self.w)

    def subtract_vector(self, x, y, z):
        return Vec3d(self.x - x, self.y - y, self.z - z, self.w)

    def get_unit_vector(self):
        length = self.get_length()
        return Vec3d(self.x / length, self.y / length, self.z / length, self.w)

    def projection(self, x, y, z):
        if self.x / x == self.y / y == self.z / z:
            print("can not calculate projection")
            return
        length = self.get_length()
        angle = self.angle_between(x, y, z)
        unit_vector_of_other = Vec3d(x, y, z).get_unit_vector()
        return unit_vector_of_other.scalar_multiplication(length * numpy.cos(angle))

    # Since Vec3d holds only three numbers, it needs to be converted into an array to get used in multiplications.
    def to_array(self):
        return numpy.array([self.x, self.y, self.z, self.w])
# CENG 487 Assignment3 by
# Bülent Arda Yılmaz
# StudentId: 270201019
# November 2022

from objects_and_parser.obj_subdivider import ObjSubdivier

class Obj:

    def __init__(self, transformation_stack, position, objects):
        self.transformation_stack = transformation_stack
        self.position = position
        self.objects = objects
        self.subdivision_level = 1

    def subdivide_increase(self):
        self.objects = ObjSubdivier.subdivide_increase(self.objects)
        self.subdivision_level += 1

    def subdivide_decrease(self):
        self.objects = ObjSubdivier.subdivice_decrease(self.objects)
        self.subdivision_level -= 1
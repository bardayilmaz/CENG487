# CENG 487 Assignment3 by
# Bülent Arda Yılmaz
# StudentId: 270201019
# November 2022

from objects_and_parser.obj import Obj
from objects_and_parser.obj_creator import ObjCreator
from objects_and_parser.obj_parser import Parser

class ObjFactory:

    @staticmethod
    def create(file_name, transformation_stack, position):
        vertices, faces, type = Parser.parse(file_name)
        obj_list = ObjCreator.create(vertices, faces, type, transformation_stack, position)
        object = Obj(transformation_stack, position, obj_list)
        return object


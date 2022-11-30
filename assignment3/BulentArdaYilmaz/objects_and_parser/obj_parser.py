# CENG 487 Assignment3 by
# Bülent Arda Yılmaz
# StudentId: 270201019
# November 2022

# Parser class's parse method takes a .obj file location and parses 
class Parser:
    @staticmethod
    def parse(location):
        vertices = []
        indices = []
        type = " "
        file = open(location, "rt")
        for line in file:
            if line[0] == "o":
                type = line[2:-1]
            elif line[0] == "v":
                line = line[2:-1]
                line = line.split(" ")
                vertex = []
                for v in line:
                    vertex.append(float(v))
                vertices.append(vertex)
            elif line[0] == "f":
                line = line[2:-1]
                line = line.split(" ")
                index_arr = []
                for i in line:
                    index_arr.append(int(i) - 1)
                indices.append(index_arr)
        return vertices, indices, type
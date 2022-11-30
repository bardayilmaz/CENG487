# CENG 487 Assignment3 by
# Bülent Arda Yılmaz
# StudentId: 270201019
# November 2022

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
from vec3d import Vec3d
from mat3d import Mat3d
from object import Object
from scene import Scene
import numpy as np
from camera.camera import Camera
from objects_and_parser.obj_factory import ObjFactory
from objects_and_parser.obj import Obj

# Objects
obj = ObjFactory.create(sys.argv[1], [Mat3d.get_rotation_z_matrix(15), Mat3d.get_rotation_x_matrix(60), Mat3d.get_rotation_y_matrix(90)], Vec3d(0, 0, -10, 1))
shapes = np.array([obj])
current_index = 0
scene = Scene(shapes[current_index].objects)
# Number of the glut window.
window = 0

#Camera
camera = Camera(Vec3d(0, 0, -5, 1), Vec3d(0, 0, -10, 1))

# A general OpenGL initialization function.  Sets all of the initial parameters.
def InitGL(Width, Height):				# We call this right after our OpenGL window is created.
    glClearColor(0.0, 0.0, 0.0, 0.0)	# This Will Clear The Background Color To Black
    glClearDepth(1.0)					# Enables Clearing Of The Depth Buffer
    glDepthFunc(GL_LESS)				# The Type Of Depth Test To Do
    glEnable(GL_DEPTH_TEST)				# Enables Depth Testing
    glShadeModel(GL_SMOOTH)				# Enables Smooth Color Shading
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()					# Reset The Projection Matrix
                                        # Calculate The Aspect Ratio Of The Window
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)

# The function called when our window is resized (which shouldn't happen if you enable fullscreen, below)
def ReSizeGLScene(Width, Height):
    if Height == 0:						# Prevent A Divide By Zero If The Window Is Too Small
        Height = 1

    glViewport(0, 0, Width, Height)		# Reset The Current Viewport And Perspective Transformation
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)


# The main drawing function. 
def DrawGLScene():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);	# Clear The Screen And The Depth Buffer
    global scene
    scene.draw_objects()

    #  since this is double buffered, swap the buffers to display what just got drawn.
    glutSwapBuffers()

# The function called whenever a key is pressed. Note the use of Python tuples to pass in: (key, x, y)
def keyPressed(key, x, y):
    global current_index, scene, camera
    # If escape is pressed, kill everything.
    # ord() is needed to get the keycode
    if ord(key) == 27:
        # Escape key = 27
        glutLeaveMainLoop()
        return
    if key == b'o':
        for obj in scene.objects:
            obj.apply_transformations()
    if key == b'p':
        current_index = (current_index + 1) % len(shapes)
        scene = Scene(shapes[current_index].objects)
    if key == b'+':
        shapes[current_index].subdivide_increase()
        scene = Scene(shapes[current_index].objects)
    if key == b'-' and shapes[current_index].subdivision_level > 1:
        shapes[current_index].subdivide_decrease()
        scene = Scene(shapes[current_index].objects)
    if key == b'a':
        matrix = camera.get_camera_translate(-0.5, 0.0, 0.0)
        for obj in scene.objects:
            obj.apply_single_transformation(matrix)
    if key == b'd':
        matrix = camera.get_camera_translate(0.5, 0.0, 0.0)
        for obj in scene.objects:
            obj.apply_single_transformation(matrix)
    if key == b'w':
        matrix = camera.get_camera_translate(0.0, 0.5, 0.0)
        for obj in scene.objects:
            obj.apply_single_transformation(matrix)
    if key == b's':
        matrix = camera.get_camera_translate(0.0, -0.5, 0.0)
        for obj in scene.objects:
            obj.apply_single_transformation(matrix)
    if key == b'e':
        matrix = camera.get_camera_rotate_y(5.0)
        for obj in scene.objects:
            obj.apply_single_transformation(matrix)
    if key == b'q':
        matrix = camera.get_camera_rotate_y(-5.0)
        for obj in scene.objects:
            obj.apply_single_transformation(matrix)
    if key == b'z':
        matrix = camera.get_camera_rotate_x(-5.0)
        for obj in scene.objects:
            obj.apply_single_transformation(matrix)
    if key == b'x':
        matrix = camera.get_camera_rotate_x(5.0)
        for obj in scene.objects:
            obj.apply_single_transformation(matrix)
    if key == b'f':
        matrix = camera.get_camera_rotate_z(-5.0)
        for obj in scene.objects:
            obj.apply_single_transformation(matrix)
    if key == b'g':
        matrix = camera.get_camera_rotate_z(5.0)
        for obj in scene.objects:
            obj.apply_single_transformation(matrix)
    if key == b'n':
        matrix = camera.get_camera_scale(1.5, 1.5, 1.5)
        for obj in scene.objects:
            obj.apply_single_transformation(matrix.matrix)
    if key == b'm':
        matrix = camera.get_camera_scale(0.75, 0.75, 0.75)
        for obj in scene.objects:
            obj.apply_single_transformation(matrix.matrix)
    
def main():
    global window
    glutInit(sys.argv)

    # Select type of Display mode:
    #  Double buffer
    #  RGBA color
    #  Alpha components supported
    #  Depth buffer
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)

    # get a 640 x 480 window
    glutInitWindowSize(640, 480)

    # the window starts at the upper left corner of the screen
    glutInitWindowPosition(0, 0)

    # Okay, like the C version we retain the window id to use when closing, but for those of you new
    # to Python (like myself), remember this assignment would make the variable local and not global
    # if it weren't for the global declaration at the start of main.
    window = glutCreateWindow("CENG487 Assignment 1")

       # Register the drawing function with glut, BUT in Python land, at least using PyOpenGL, we need to
    # set the function pointer and invoke a function to actually register the callback, otherwise it
    # would be very much like the C version of the code.
    glutDisplayFunc(DrawGLScene)

    # Uncomment this line to get full screen.
    # glutFullScreen()

    # When we are doing nothing, redraw the scene.
    glutIdleFunc(DrawGLScene)

    # Register the function called when our window is resized.
    glutReshapeFunc(ReSizeGLScene)

    # Register the function called when the keyboard is pressed.
    glutKeyboardFunc(keyPressed)

    # Initialize our window.
    InitGL(640, 480)

    # Start Event Processing Engine
    glutMainLoop()

# Print message to console, and kick off the main to get it rolling.
print ("Hit ESC key to quit.")
print("Hit 'O' key to transform Object")
print("Hit 'P' key to change current Object")
print("Hit 'W' key to move camera up")
print("Hit 'A' key to move camera down")
print("Hit 'S' key to move camera left")
print("Hit 'Q' key to rotate camera around +y")
print("Hit 'E' key to rotate camera arond -y")
print("Hit 'Z' key to rotate camera around +x")
print("Hit 'X' key to rotate camera around -x")
print("Hit 'F' key to move camera around +z")
print("Hit 'G' key to move camera around -z")
print("Hit 'N' key to zoom in")
print("Hit 'M' key to zoom out")
print("Hit '-' key to decrease subdivision level")
print("Hit '+' key to increase subdivision level")
main()
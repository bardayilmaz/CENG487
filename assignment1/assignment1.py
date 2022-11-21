# CENG 487 Assignment1 by
# Bülent Arda Yılmaz
# StudentId: 270201019
# November 2022

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
from vec3d import vec3d
from mat3d import mat3d
from object import object
from scene import Scene

# Objects
triangle = object(
    [ # Vertices
	vec3d(0.0, 1.0, 0.0, 1.0), 			# Top
	vec3d(1.0, -1.0, 0.0, 1.0),			# Bottom Right
	vec3d(-1.0, -1.0, 0.0, 1.0),		# Bottom Left
    ],
    [ # matrix stack
	mat3d.get_translation_matrix(0.0, -1.0, 0.0),
	mat3d.get_rotation_z_matrix(0.02),
	mat3d.get_translation_matrix(0.0, 1.0, 0.0)
    ],
	[[1.0, 0.0, 1.0]],
	GL_POLYGON,
	vec3d(-1.5,0.0,-6.0, 1))

square = object(
        # Vertices
	[vec3d(-1.0, 1.0, 0.0, 1.0),			# Top Left
	vec3d(1.0, 1.0, 0.0, 1.0),			# Top Right
	vec3d(1.0, -1.0, 0.0, 1.0),			# Bottom Right
	vec3d(-1.0, -1.0, 0.0, 1.0)],			# Bottom Left
        # matrix stack
    [
		mat3d.get_translation_matrix(-1.0, -1.0, 0.0),
		mat3d.get_rotation_z_matrix(0.02),
		mat3d.get_translation_matrix(1.0, 1.0, 0.0)],
		[[0.0, 0.0, 1.0]],
		GL_QUADS,
		vec3d(1.5, 0.0, -7.0, 1)) 

scene = Scene([triangle, square])
# Number of the glut window.
window = 0

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

	glMatrixMode(GL_MODELVIEW)

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
	
    # glLoadIdentity()    # Reset The View
    # glTranslatef(-1.5,0.0,-6.0);	# Move Left And Into The Screen

    # glBegin(GL_POLYGON)
    # glColor3f(1.0,0.0,0.0)			# Red
    # glVertex3f(triangle.vertices[0].x, triangle.vertices[0].y, triangle.vertices[0].z)
    # glColor3f(0.0,1.0,0.0)			# Green
    # glVertex3f(triangle.vertices[1].x, triangle.vertices[1].y, triangle.vertices[1].z)
    # glColor3f(0.0,0.0,1.0)			# Blue
    # glVertex3f(triangle.vertices[2].x, triangle.vertices[2].y, triangle.vertices[2].z)
    # glEnd()

    # glTranslatef(1.5, 0.0, 6.0)

    # glLoadIdentity()
    # glTranslatef(1.5,0.0,-7.0)
    # glBegin(GL_QUADS)
    # glColor3f(0.0, 0.0, 1.0)
    # glVertex3f(square.vertices[0].x, square.vertices[0].y, square.vertices[0].z)
    # glVertex3f(square.vertices[1].x, square.vertices[1].y, square.vertices[1].z)
    # glVertex3f(square.vertices[2].x, square.vertices[2].y, square.vertices[2].z)
    # glVertex3f(square.vertices[3].x, square.vertices[3].y, square.vertices[3].z)
    # glEnd()

    #  since this is double buffered, swap the buffers to display what just got drawn.
    glutSwapBuffers()

# The function called whenever a key is pressed. Note the use of Python tuples to pass in: (key, x, y)
def keyPressed(key, x, y):
    global triangle, square
	# If escape is pressed, kill everything.
	# ord() is needed to get the keycode
    if ord(key) == 27:
        # Escape key = 27
        glutLeaveMainLoop()
        return
    if key == b'x':
        triangle.apply_transformations()
    if key == b'c':
        square.apply_transformations()
    if key == b'a':
	    for obj in scene.objects:
		    obj.apply_transformations()

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
main()
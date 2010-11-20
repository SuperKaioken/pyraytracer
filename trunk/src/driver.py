#from __future__ import division
import pyglet
from pyglet.window import key
from pyglet.window import mouse
from pyglet.gl import *

# The pyglet Window
class MainWindow(pyglet.window.Window):
    def __init__(self):
        super(MainWindow, self).__init__(caption ="pyRayTracer", 
                                         width=800, height=800,
                                         resizable = True)
        
        # set the color to be used when glClear() is called
        glClearColor(1, 1, 1, 1) 
        
        glEnable(GL_DEPTH_TEST)

    def on_resize(self, w, h):
        # Set the viewport.
        glViewport(0, 0, w, h)

        # Set the projection
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity( )

        # Set-up projection matrix
        glFrustum(-0.5, 0.5, -0.5, 0.5, 0.5, 2000)
        #glOrtho(-200, 200, -200, 200, 1, 300)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        # Set-up initial camera position
        glTranslatef(0, 0, -500)
        glRotatef(-45, 1, 0, 0)
        
        # Always redisplay after projection/mapping change
        self.on_draw()
    
    def on_draw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glColor3f(1.0, 0, 0)
        quadratic = gluNewQuadric()
        gluSphere(quadratic,500,32,32) 
    
    def on_key_release(self, symbol, modifiers):
        pass
        
if __name__ == '__main__':
    window = MainWindow()
    pyglet.app.run()
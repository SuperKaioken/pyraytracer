#from __future__ import division
import pyglet
from pyglet.window import key
from pyglet.window import mouse
from pyglet.gl import *

import numpy

import scene
import rays
import objects

WIDTH = 800
HEIGHT = 800
DEPTH = 500

# The pyglet Window
class MainWindow(pyglet.window.Window):
    def __init__(self):
        super(MainWindow, self).__init__(caption ="pyRayTracer", 
                                         width=WIDTH, height=HEIGHT,
                                         resizable = True)
        
        # set the color to be used when glClear() is called
        glClearColor(1, 1, 1, 1) 
        
        glEnable(GL_DEPTH_TEST)
        
        self.scene = scene.Scene()
        self.rays = rays.Rays(WIDTH, HEIGHT, DEPTH)
        

    def on_resize(self, w, h):
#        # Set the viewport.
#        glViewport(0, 0, w, h)
#
#        # Set the projection
#        glMatrixMode(GL_PROJECTION)
#        glLoadIdentity( )
#
#        # Set-up projection matrix
#        glFrustum(-0.5, 0.5, -0.5, 0.5, 0.5, 2000)
#        #glOrtho(-200, 200, -200, 200, 1, 300)
#
#        glMatrixMode(GL_MODELVIEW)
#        glLoadIdentity()
#        
#        # Set-up initial camera position
#        glTranslatef(0, 0, -500)
#        glRotatef(-45, 1, 0, 0)
        
        # Always redisplay after projection/mapping change
        
        print 'test'
        for i in range(WIDTH):
            for j in range(HEIGHT):
                d = self.rays.get_ray_direction(i, j)
                object1 = self.scene.get_object_list()[0]
                
                if(object1.intersection_test(d, numpy.array([0, 0, 0])) > 0):
                    pyglet.graphics.draw(1, GL_POINTS, 
                                         ('v2i', (i,j)),
                                         ('c3B', (0, 1, 0)))
    
    def on_draw(self):
        #glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        pass       
        
    
    def on_key_release(self, symbol, modifiers):
        pass
        
if __name__ == '__main__':
    window = MainWindow()
    pyglet.app.run()
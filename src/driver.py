#from __future__ import division
import pyglet
from pyglet.window import key
from pyglet.window import mouse
from pyglet.gl import *

import numpy

import scene
import rays
import objects

WIDTH = 120
HEIGHT = 100
DEPTH = 100
 
IMAGE_PLANE_WIDTH = 150
IMAGE_PLANE_HEIGHT = 150
VIEWPOINT = numpy.array([0,0,-100])
IMAGE_PLANE_DISTANCE = -VIEWPOINT[2]
WINDOW_WIDTH = 150
WINDOW_HEIGHT = 150


# The pyglet Window
class MainWindow(pyglet.window.Window):
    def __init__(self):
        super(MainWindow, self).__init__(caption ="pyRayTracer", 
                                         width=WINDOW_WIDTH, height=WINDOW_HEIGHT,
                                         resizable = True)
        
        # set the color to be used when glClear() is called
        glClearColor(1, 1, 1, 1)                   
        
        self.scene = scene.Scene()
        self.rays = rays.Rays(IMAGE_PLANE_WIDTH, IMAGE_PLANE_HEIGHT, IMAGE_PLANE_DISTANCE, WINDOW_WIDTH, WINDOW_HEIGHT)        
        
        
    def on_draw(self):
        glPointSize(1)            
        for i in range(WINDOW_WIDTH):
            for j in range(WINDOW_HEIGHT):
                d = self.rays.get_ray_direction(i, j)
                object1 = self.scene.get_object_list()[0]
                #object2 = self.scene.get_object_list()[1]
                
                if(object1.intersection_test(d, VIEWPOINT) > 0):                
                    pyglet.graphics.draw(1, GL_POINTS,('v2i', (i,j)),('c3B', (0,255,0)))                
        
if __name__ == '__main__':
    window = MainWindow()
    pyglet.app.run()
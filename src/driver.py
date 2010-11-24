#from __future__ import division
import pyglet
from pyglet.window import key
from pyglet.window import mouse
from pyglet.gl import *

import numpy

import scene
import rays
import objects

import Image

WIDTH = 120
HEIGHT = 100
DEPTH = 100
 
IMAGE_PLANE_WIDTH = 150
IMAGE_PLANE_HEIGHT = 150
VIEWPOINT = numpy.array([0,0,5])
IMAGE_PLANE_DISTANCE = VIEWPOINT[2]
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
        
if __name__ == '__main__':
    scene = scene.Scene() 
    rays = rays.Rays(IMAGE_PLANE_WIDTH, IMAGE_PLANE_HEIGHT, IMAGE_PLANE_DISTANCE, WINDOW_WIDTH, WINDOW_HEIGHT)
    
    img = Image.new("RGB", (WINDOW_WIDTH, WINDOW_HEIGHT))
    
    for i in range(WINDOW_WIDTH):
        for j in range(WINDOW_HEIGHT):
            #direction = rays.get_ray_direction(i, j, VIEWPOINT)
            point = numpy.array([i,j,0])
            direction = rays.get_ray_direction(i,j)
            object1 = scene.get_object_list()[0]
            
            if(object1.intersection_test(direction, VIEWPOINT) > 0):                
                img.putpixel((i,j), (0,255,0))
            
    img.save("../test.bmp")
    print "FINISHED"

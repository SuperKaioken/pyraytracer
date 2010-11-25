#from __future__ import division
import pyglet
from pyglet.window import key
from pyglet.window import mouse
from pyglet.gl import *

import numpy

import scene
import rays
import objects
import lighting

WIDTH = 120
HEIGHT = 100
DEPTH = 100
VIEWPOINT = numpy.array([0,0,5])

# The pyglet Window
class MainWindow(pyglet.window.Window):
    def __init__(self):
        super(MainWindow, self).__init__(caption ="pyRayTracer", 
                                         width=WIDTH, height=HEIGHT,
                                         resizable = True)
        
        # set the color to be used when glClear() is called
        glClearColor(1, 1, 1, 1)  
        
        #glEnable(GL_DEPTH_TEST)
        
        self.scene = scene.Scene()
        self.rays = rays.Rays(WIDTH, HEIGHT, DEPTH, WIDTH, HEIGHT)        
        
        
    def on_draw(self):
        glPointSize(1)            
        for i in range(WIDTH):
            for j in range(HEIGHT):
                d = self.rays.get_ray_direction(i, j)
                
                object_list = scene.OBJECT_LIST
                intersections = []
                colors = []
                for object in object_list:
                    intersection_point = object.intersection_test(d, VIEWPOINT)
                    if(intersection_point > 0): 
                        intersections.append(intersection_point)                              
                        colors.append(lighting.calc_lighting(object, VIEWPOINT + intersection_point * d)) # p(t) = e + td   
                
                try:
                    assoc = zip(object_list, intersections, colors)
                    assoc.sort()
                    object_list, intersections, colors = zip(assoc)
                except(ValueError):
                    pyglet.graphics.draw(1, GL_POINTS,('v2i', (i,j)),('c3f', scene.BACKGROUND_COLOR))
                
                if len(intersections) != 0:
                    print colors[0]
                    pyglet.graphics.draw(1, GL_POINTS,('v2i', (i,j)),('c3f', colors[0]))
                        
if __name__ == '__main__':
    scene.INIT()
    window = MainWindow()
    pyglet.app.run()
    
##from __future__ import division
#import pyglet
#from pyglet.window import key
#from pyglet.window import mouse
#from pyglet.gl import *
#
#import numpy
#
#import scene, rays, objects, lighting
#
#import Image
# 
#IMAGE_PLANE_WIDTH = 150
#IMAGE_PLANE_HEIGHT = 150
#VIEWPOINT = numpy.array([0,0,5])
#IMAGE_PLANE_DISTANCE = VIEWPOINT[2]
#WINDOW_WIDTH = 150
#WINDOW_HEIGHT = 150
#
## The pyglet Window
#class MainWindow(pyglet.window.Window):
#    def __init__(self):
#        super(MainWindow, self).__init__(caption ="pyRayTracer", 
#                                         width=WINDOW_WIDTH, height=WINDOW_HEIGHT,
#                                         resizable = True)
#        
#        # set the color to be used when glClear() is called
#        glClearColor(1, 1, 1, 1)                   
#        
#        self.scene = scene.Scene()
#        self.rays = rays.Rays(IMAGE_PLANE_WIDTH, IMAGE_PLANE_HEIGHT, IMAGE_PLANE_DISTANCE, WINDOW_WIDTH, WINDOW_HEIGHT)        
#        
#        
#    def on_draw(self):
#        glPointSize(1)                           
#        
#if __name__ == '__main__':
#    scene.INIT()
#    rays = rays.Rays(IMAGE_PLANE_WIDTH, IMAGE_PLANE_HEIGHT, IMAGE_PLANE_DISTANCE, WINDOW_WIDTH, WINDOW_HEIGHT)
#    
#    img = Image.new("RGB", (WINDOW_WIDTH, WINDOW_HEIGHT))
#    
#    for i in range(WINDOW_WIDTH):
#        for j in range(WINDOW_HEIGHT):
#            #direction = rays.get_ray_direction(i, j, VIEWPOINT)
#            direction = rays.get_ray_direction(i,j)
#            object1 = scene.GET_OBJECT_LIST()[0]
#            
#            color = scene.BACKGROUND_COLOR
#            
#            intersection_point = 0
#            intersection_point = object1.intersection_test(direction, VIEWPOINT)        
#            # if ray intersects object1
#            if(intersection_point > 0):                
#                # apply lighting
#                print intersection_point
#                color = lighting.calc_lighting(object1, VIEWPOINT + intersection_point * direction) # p(t) = e + td                
#            img.putpixel((i,j), (color[0] * 255, color[1] * 255, color[2] * 255)) # since we are using floats, must convert to integer
#            
#    img.save("../../test.bmp")
#    print "FINISHED"
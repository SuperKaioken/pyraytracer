import numpy
import math
import scene, rays, objects

#print numpy.array([0,0,2])
#
#VIEWPOINT = numpy.array([0,0,5])
#
#def normalize(vector):
#    distance = numpy.sqrt((vector[0] ** 2) + (vector[1] ** 2) + (vector[2] ** 2))
#    
#    try:   
#        return numpy.array([vector[0] / distance, vector[1] / distance, vector[2] / distance]) 
#    except(ZeroDivisionError):
#        return numpy.array([0, 0, 0])  
#
#scene = scene.Scene() 
#rays = rays.Rays(150, 150, VIEWPOINT[2], 150, 150)
#object1 = objects.Sphere(numpy.array([0, 8, -10]), 8, [1.0, 0.0, 0.0])
#
#image_point = numpy.array([0,0,0])
#direction = normalize(image_point - VIEWPOINT)
#
#t = object1.intersection_test(direction, VIEWPOINT)
#print VIEWPOINT + t * direction

a = [2,1,3]
b = ['b','a','c']

c = zip(a,b)

c.sort()

a,b = zip(*c)

print a
print b
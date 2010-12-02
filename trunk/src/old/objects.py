import numpy
import math

import scene

def normalize(vector):
    distance = numpy.sqrt((vector[0] ** 2) + (vector[1] ** 2) + (vector[2] ** 2))
    
    try:   
        return numpy.array([vector[0] / distance, vector[1] / distance, vector[2] / distance]) 
    except(ZeroDivisionError):
        return numpy.array([0, 0, 0]) 

def in_shadow(point, rays, id):
    d = numpy.array(normalize(point - scene.GET_LIGHT_LIST()[0].position))
    
    object, intersection_point = rays.shoot_ray(point, d, id)
    
    if object == None:
        return False
    else:
        return True 
            
class Light():
    
    def __init__(self, position, color, spectral_color):
        self.position = position
        self.color = color
        self.spectral_color = spectral_color
        
        
class Sphere():
    '''
    classdocs
    '''

    def __init__(self, center, radius, color, spectral_color, shininess, timestamp):
        '''
        Constructor 
        '''
        self.c = center
        self.R = radius 
        self.color = color
        self.spectral_color = spectral_color
        self.shininess = shininess
        self.id = timestamp
        
    def intersection_test(self, d, e):
        discriminant = self.discriminant_test(d, e)        
        if discriminant < 0:
            return 0
        elif discriminant == 0:
            return (numpy.dot(-d, e - self.c)) / numpy.dot(d, d)
        elif discriminant > 0:
            return min([(numpy.dot(-d, e - self.c) + numpy.sqrt(discriminant)) / numpy.dot(d, d) , (numpy.dot(-d, e - self.c) - numpy.sqrt(discriminant)) / numpy.dot(d, d)])
      
    def discriminant_test(self, d, e):
        result = (numpy.dot(d, (e - self.c)) ** 2 - numpy.dot(d, d) * ((numpy.dot(e - self.c, e - self.c)) - (self.R ** 2)))        
        
        return result 

    def calc_normal(self, point):
        
        return (point - self.c) / self.R
    
class Plane():
    
    def __init__(self, normal, point_on_plane, color, spectral_color, shininess, id):
        self.normal = normal
        self.point_on_plane = point_on_plane
        self.color = color
        self.spectral_color = spectral_color
        self.shininess = shininess
        self.id = id
        
    def intersection_test(self, d, e):
        denom = numpy.dot(normalize(d), normalize(self.normal))
        if denom == 0:
            return 0
        else:
            t = numpy.dot(normalize(self.normal), normalize((self.point_on_plane - e))) / denom
            if t < 0:
                return t
            else:
                return t
            
    def calc_normal(self, point):
        return self.normal
            
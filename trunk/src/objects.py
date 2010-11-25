import numpy
import math

def normalize(self, vector):
    distance = numpy.sqrt((vector[0] ** 2) + (vector[1] ** 2) + (vector[2] ** 2))
    
    try:   
        return numpy.array([vector[0] / distance, vector[1] / distance, vector[2] / distance]) 
    except(ZeroDivisionError):
        return numpy.array([0, 0, 0]) 
        
class Light():
    
    def __init__(self, position, color, spectral_color):
        self.position = position
        self.color = color
        self.spectral_color = spectral_color
        
        
class Sphere():
    '''
    classdocs
    '''

    def __init__(self, center, radius, color, spectral_color, shininess):
        '''
        Constructor 
        '''
        self.c = center
        self.R = radius 
        self.color = color
        self.spectral_color = spectral_color
        self.shininess = shininess
        
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
    
    def __init__(self, normal, point_on_plane, color, spectral_color, shininess):
        self.normal = normal
        self.point_on_plane = point_on_plane
        self.color = color
        self.spectral_color = spectral_color
        self.shininess = shininess
        
    def intersection_test(self, d, e):
        denom = numpy.dot(d,self.normal)
        if denom == 0:
            return 0
        else:
            t = numpy.dot(self.normal, (self.point_on_plane - e)) / denom
            print t
            if t < 0:
                return t
            else:
                return t
            
    def calc_normal(self, point):
        return self.normal
            
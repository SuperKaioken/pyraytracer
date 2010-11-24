import numpy
import math

class Sphere():
    '''
    classdocs
    '''

    def __init__(self, center, radius, color):
        '''
        Constructor 
        '''
        self.c = center
        self.R = radius 
        self.color = color
        
    def intersection_test(self, d, e):
        discriminant = self.discriminant_test(d, e)        
        if discriminant < 0:
            return 0
        elif discriminant == 0:
            return (numpy.dot(-d, e - self.c)) / numpy.dot(d, d)
        elif discriminant > 0:
            return min([(numpy.dot(-d, e - self.c) + numpy.sqrt(discriminant)) / numpy.dot(d, d) , (numpy.dot(-d, e - self.c) - numpy.sqrt(discriminant)) / numpy.dot(d, d)])

#        elif discriminant == 0:    
#            return 1
#        elif discriminant > 0:
#            return 2
    
    
    def discriminant_test(self, d, e):
        result = (numpy.dot(d, (e - self.c)) ** 2 - numpy.dot(d, d) * ((numpy.dot(e - self.c, e - self.c)) - (self.R ** 2)))        
        
        return result 
        
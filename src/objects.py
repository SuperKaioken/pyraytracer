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
            return [-d * (e - self.c)]
        elif discriminant > 0:
            return [-d * (e - self.c + discriminant), -d * (e - self.c - discriminant)]
    
    def discriminant_test(self, d, e):
        result = math.sqrt((d * (e - self.c)) ** 2 - (d * d)((e - self.c) * (e - self.c) - self.R ** 2))  
    
        return result  
        
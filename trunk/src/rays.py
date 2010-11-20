import numpy

import math

class Rays():
    '''
    classdocs
    '''


    def __init__(self, width, height, depth):
        '''
        Constructor
        '''
        self.width = width # width of the image plane
        self.height = height # height of the image plane
        self.d = depth
        
        self.waxis = numpy.array([0,0,1])
        self.uaxis = numpy.array([1,0,0])
        self.vaxis = numpy.array([0,1,0])

        
        self.l = 0
        self.r = width
        self.b = 0
        self.t = height
        
        self.nx = 800
        self.ny = 800
        
    
    def shoot_rays(self):
        pass    
    
    def get_ray_direction(self, i, j):
        u = self.l + (self.r - self.l)*(i + 0.5) / self.nx
        v = self.b + (self.t - self.b)*(j + 0.5) / self.ny
        
        direction = numpy.array((self.waxis * -self.d) + (self.uaxis * u) + (self.vaxis * v))
        
        return self.normalize(direction)
                 
    def normalize(self, vector):
        distance = numpy.sqrt((vector[0] ** 2) + (vector[1] ** 2) + (vector[2] ** 2))
        
        try:   
            return numpy.array([vector[0] / distance, vector[1] / distance, vector[2] / distance]) 
        except(ZeroDivisionError):
            return numpy.array([0, 0, 0])      
                
                
        
        
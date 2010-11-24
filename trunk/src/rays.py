import numpy
import math

class Rays():
    '''
    classdocs
    '''


    def __init__(self, image_plane_width, image_plane_height, image_plane_distance, window_width, window_height):
        '''
        Constructor
        '''
        self.image_plane_width = image_plane_width
        self.image_plane_height = image_plane_height
        self.image_plane_distance = image_plane_distance
        
        self.waxis = numpy.array([0,0,1])
        self.uaxis = numpy.array([1,0,0])
        self.vaxis = numpy.array([0,1,0])
 
        self.l = -(image_plane_width / 2)
        self.r = image_plane_width / 2
        self.b = -(image_plane_height / 2)
        self.t = image_plane_height / 2
        
        self.nx = window_width
        self.ny = window_height
    
    def get_ray_direction(self, i, j):
        u = self.l + (self.r - self.l)*(i + 0.5) / self.nx
        v = self.b + (self.t - self.b)*(j + 0.5) / self.ny
        
        direction = numpy.array((self.waxis * -self.image_plane_distance) + (self.uaxis * u) + (self.vaxis * v))
        
        return self.normalize(direction)
                 
    def normalize(self, vector):
        distance = numpy.sqrt((vector[0] ** 2) + (vector[1] ** 2) + (vector[2] ** 2))
        
        try:   
            return numpy.array([vector[0] / distance, vector[1] / distance, vector[2] / distance]) 
        except(ZeroDivisionError):
            return numpy.array([0, 0, 0])      
                
                
        
        
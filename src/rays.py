import math

class Rays():
    '''
    classdocs
    '''


    def __init__(self, width, height):
        '''
        Constructor
        '''
        self.width = width # width of the image plane
        self.height = height # height of the image plane
        
        self.waxis = [0,0,1]
        self.uaxis = [1,0,0]
        self.S = [0,1,0]
        
        self.l = 0
        self.r = width
        self.b = 0
        self.t = height
        
        self.nx = 800
        self.ny = 800
        
    
    def shoot_rays(self):
        pass    
    
    def get_ray_direction(self, i, j):
        u = self.l + (self.r - self.l)(i + 0.5) / self.nx
        v = self.b + (self.t - self.b)(j + 0.5) / self.ny
                
        direction = [x * -self.d for x in self.waxis] + [x * u for x in self.uaxis] + [x * v for x in self.vaxis]
        direction = self.normalize(direction)
                 
    def normalize(self, vector):
        distance = math.sqrt((vector[0] ** 2) + (vector[1] ** 2) + (vector[1] ** 2))
        
        return [vector[0] / distance, vector[1] / distance, vector[2] / distance]       
                
                
        
        
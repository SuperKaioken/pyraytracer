import numpy

import objects

class Scene(object):
    '''
    classdocs
    '''
    
    def __init__(self):
        '''
        Constructor
        '''
        self.object_list = [] 
        
        object1 = objects.Sphere(numpy.array([0, 0, -1]), 5, [1.0, 0.0, 0.0])

        self.object_list.append(object1)
    
    def get_object_list(self):
        return self.object_list   
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
        
        object1 = objects.Sphere(numpy.array([1, 0, -50]), 10, [1.0, 0.0, 0.0])
        object2 = objects.Sphere(numpy.array([3, 0, -30]), 10, [1.0, 0.0, 0.0])
        self.object_list.append(object1)
        self.object_list.append(object2)
    
    def get_object_list(self):
        return self.object_list   
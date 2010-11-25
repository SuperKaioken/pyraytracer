import numpy
import objects
    
BACKGROUND_COLOR = numpy.array([0,0,0])
AMBIENT = numpy.array([0.1, 0.1, 0.2])
OBJECT_LIST = [] 
LIGHT_LIST = []

def INIT():
    object1 = objects.Sphere(numpy.array([0, 0, -80]), 75, [1.0, 0.0, 0.0], [0.8, 0.8, 0.8], 32)
    OBJECT_LIST.append(object1)
    
    light1 = objects.Light(numpy.array([1,1,1]), numpy.array([1,1,1]), numpy.array([0.5,0.5,0.5]))
    LIGHT_LIST.append(light1)
        
def GET_OBJECT_LIST():
    return OBJECT_LIST  

def GET_LIGHT_LIST():
    return LIGHT_LIST
    
class Scene(object):
    '''
    classdocs
    '''
    
    def __init__(self):
        '''
        Constructor
        '''   

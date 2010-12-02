import numpy
import objects
import time
    
BACKGROUND_COLOR = numpy.array([0,0,0])
AMBIENT = numpy.array([0.1, 0.1, 0.2])
OBJECT_LIST = [] 
LIGHT_LIST = []

def INIT():
    # center, radius, color, spectral_color, shininess
    object1 = objects.Sphere(numpy.array([-30, 10, -80]), 10, numpy.array([1.0, 0.0, 0.0]), numpy.array([0.8, 0.8, 0.8]), 32, int(time.time()))
    object2 = objects.Sphere(numpy.array([0, 10, -80]), 10, numpy.array([0.0, 0.0, 1.0]), numpy.array([0.8, 0.8, 0.8]), 32, int(time.time()))
    object3 = objects.Sphere(numpy.array([-15, 10, -85]), 20, numpy.array([0.0, 1.0, 0.0]), numpy.array([0.8, 0.8, 0.8]), 32, int(time.time()))
    object4 = objects.Sphere(numpy.array([30, 10, -85]), 20, numpy.array([1.0, 1.0, 0.0]), numpy.array([0.8, 0.8, 0.8]), 32, int(time.time()))

    plane = objects.Plane(numpy.array([0,1,0]), numpy.array([0,-1,-5]), numpy.array([1.0, 0.0, 1.0]), numpy.array([0.8, 0.8, 0.8]), 32, int(time.time()))

    OBJECT_LIST.append(object1)
    OBJECT_LIST.append(object2)
    OBJECT_LIST.append(object3)
    OBJECT_LIST.append(object4)
    OBJECT_LIST.append(plane)
    
    # position, color, spectral_color
    light1 = objects.Light(numpy.array([0, 50, -20]), numpy.array([1,1,1]), numpy.array([0.5,0.5,0.5]))
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

import numpy
import scene, objects, driver

def calc_lighting(object, point):
    light_position = scene.GET_LIGHT_LIST()[0].position
    light_color = scene.GET_LIGHT_LIST()[0].color
    light_spectral_color = scene.GET_LIGHT_LIST()[0].spectral_color
    
    n = normalize(object.calc_normal(point))          
    v = normalize(driver.VIEWPOINT - point) # direction TO camera FROM surface                  
    li = normalize(light_position - point) # direction to given light i
    h = normalize(li + v) 
                     
    Ia = calc_Ia(object.color, scene.AMBIENT)
    Id = calc_Id(object.color, li, n, light_color)
    Is = calc_Is(object.spectral_color, n, h, object.shininess, light_spectral_color)
                    
    return Ia + Id + Is
        

def calc_Ia(ka, Iaglobal):
    
    return ka * Iaglobal

def calc_Id(kd, li, n, Idi):
    
    return kd * numpy.dot(li, n) * Idi

def calc_Is(ks, n, h, s, Isi):
        
    return Isi * (numpy.dot(n, h) ** s)

def normalize(vector):
    magnitude = numpy.sqrt((vector[0] ** 2) + (vector[1] ** 2) + (vector[2] ** 2))
    
    try:   
        return numpy.array([vector[0] / magnitude, vector[1] / magnitude, vector[2] / magnitude]) 
    except(ZeroDivisionError):
        return numpy.array([0, 0, 0]) 
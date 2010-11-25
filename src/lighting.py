import numpy
import scene
import objects
import driver

def calc_lighting(object, point):
    n = normalize(object.calc_normal(point))          

    v = normalize(driver.VIEWPOINT - point)
                    
    #v = self.normalize([-vertex_eye[0], -vertex_eye[1], -vertex_eye[2]]) # 0 - the vertex

                        
    light_position = scene.GET_LIGHT_LIST()[0].position
    light_color = scene.GET_LIGHT_LIST()[0].color
    light_spectral_color = scene.GET_LIGHT_LIST()[0].spectral_color
                    
    li = normalize(light_position - point)
    
    h = normalize(li + v)
                     
    Ia = calc_Ia(object.color, scene.AMBIENT)
    Id = calc_Id(object.color, li, n, light_color)
    Is = calc_Is(object.spectral_color, n, h, object.shininess, light_spectral_color)
                    
    return Ia + Id + Is
        

def calc_Ia(ka, Iaglobal):
    
    return ka * Iaglobal

def calc_Id(kd, li, n, Idi):
    
    return Idi * numpy.dot(li, n)

def calc_Is(ks, n, h, s, Isi):
        
    return Isi * (numpy.dot(n, h) ** s)

def normalize(vector):
    distance = numpy.sqrt((vector[0] ** 2) + (vector[1] ** 2) + (vector[2] ** 2))
    
    try:   
        return numpy.array([vector[0] / distance, vector[1] / distance, vector[2] / distance]) 
    except(ZeroDivisionError):
        return numpy.array([0, 0, 0]) 
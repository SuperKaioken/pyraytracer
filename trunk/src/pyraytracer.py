from __future__ import division
import pyglet
from pyglet.window import key
from pyglet.window import mouse
from pyglet.gl import *
import numpy

image_plane_width = 150
image_plane_height = 150
window_width = 150
window_height = 150
viewpoint = numpy.array([0,0,20])

x_axis = numpy.array([1,0,0])
y_axis = numpy.array([0,1,0])
z_axis = numpy.array([0,0,1])

def normalize(vector):
    magnitude = numpy.sqrt((vector[0] ** 2) + (vector[1] ** 2) + (vector[2] ** 2))
    
    try:   
        return numpy.array([vector[0] / magnitude, vector[1] / magnitude, vector[2] / magnitude]) 
    except(ZeroDivisionError):
        return numpy.array([0, 0, 0]) 
    
class Scene():
    def __init__(self):
        self.viewpoint = viewpoint
        self.image_plane_width = image_plane_width
        self.image_plane_height = image_plane_height
        self.objects = []
        self.lights = []
        self.background_color = numpy.array([0,0,0])
        self.ambient_color = numpy.array([0.5,0.5,0.5])
        
        # populate with object(s) and light(s)
        self.add_object(Sphere(numpy.array([0,15,-20]), 19, numpy.array([1.0,0.0,0.0]), numpy.array([0.8,0.8,0.8]), 32))
        self.add_object(Plane(numpy.array([0,-1,-10]), numpy.array([0,1,0]), numpy.array([1.0,0.0,1.0]), numpy.array([0.8,0.8,0.8]), 32))
        self.add_light(Light(numpy.array([0,25,-30]), numpy.array([1,1,1]), numpy.array([0.5,0.5,0.5])))
        
    def add_object(self, object):
        self.objects.append(object)

    def add_light(self, light):
        self.lights.append(light)
        
    def shoot_ray(self, origin, dir):
        intersections = []
        hit_objects = []
        color = self.background_color
        
        # see which objects the ray hits
        for object in self.objects:
            intersection_value = object.hit_test(origin, dir)
            if(intersection_value > 0): 
                intersections.append(intersection_value)                              
                hit_objects.append(object)
                
        # sort to find the closest object
        try:
            assoc = zip(intersections, hit_objects)
            assoc.sort()
            intersections, hit_objects = zip(*assoc)
        # if a ValueError is thrown then no objects were hit
        except(ValueError):
            return color
        color = hit_objects[0].color
        
        # calculate lighting effects
        color = self.__calc_lighting(hit_objects[0], origin + intersections[0] * dir)
        
        # determine if in shadow
        if (self.shoot_shadow_ray(origin + intersections[0] * dir, normalize(self.lights[0].position - (origin + intersections[0] * dir)), 2)) == True:
            color = self.ambient_color * hit_objects[0].color
            
        return color
    
    def shoot_shadow_ray(self, origin, dir, offset):
        intersections = []
        hit_objects = []
        
        # see which objects the ray hits
        for object in self.objects:
            intersection_value = object.hit_test(origin, dir)
            if(intersection_value > offset): 
                intersections.append(intersection_value)                              
                hit_objects.append(object)
                
        if len(hit_objects) > 0:
            return True
        else:
            return False

    def __calc_lighting(self, object, point):
        light_position = self.lights[0].position
        light_color = self.lights[0].color
        light_spectral_color = self.lights[0].spectral_color
        
        n = normalize(object.calc_normal(point))          
        v = normalize(viewpoint - point) # direction TO camera FROM surface                  
        li = normalize(light_position - point) # direction to given light i
        h = normalize(li + v) 
                         
        Ia = self.__calc_Ia(object.color, self.ambient_color)
        Id = self.__calc_Id(object.color, li, n, light_color)
        Is = self.__calc_Is(object.spectral_color, n, h, object.shininess, light_spectral_color)
                        
        return Ia + Id + Is
            
    
    def __calc_Ia(self, ka, Iaglobal):
        
        return ka * Iaglobal
    
    def __calc_Id(self, kd, li, n, Idi):
        
        return kd * numpy.dot(li, n) * Idi
    
    def __calc_Is(self, ks, n, h, s, Isi):
            
        return Isi * (numpy.dot(n, h) ** s)
                   
class Surface():
    def __init__(self, color, spectral_color, shininess):
        self.color = color
        self.spectral_color = spectral_color
        self.shininess = shininess
    
    def hit_test(self):
        pass
    
    def calc_normal(self):
        pass
    
class Sphere(Surface):
    def __init__(self, center, radius, color, spectral_color, shininess):
        Surface.__init__(self, color, spectral_color, shininess)
        self.center = center
        self.radius = radius 
        
    def hit_test(self, origin, dir):
        # first test the discriminant
        discriminant = (numpy.dot(dir, (origin - self.center)) ** 2 - numpy.dot(dir, dir) * ((numpy.dot(origin - self.center, origin - self.center)) - (self.radius ** 2))) 
        
        # if the discriminant is less than one then the sqrt will yield an imaginary number and thus there is no intersection
        if discriminant < 0:
            return -1
        # if the discriminant is equal to zero then the ray hit one point, i.e the very top or bottom of the sphere
        elif discriminant == 0:
            return numpy.dot(-dir, origin - self.center) / numpy.dot(dir, dir)
        # if the discriminant is greater than zero then the ray went in one side and out the other
        elif discriminant > 0:
            # take the value of where the ray went in
            return min([(numpy.dot(-dir, origin - self.center) + numpy.sqrt(discriminant)) / numpy.dot(dir, dir) , (numpy.dot(-dir, origin - self.center) - numpy.sqrt(discriminant)) / numpy.dot(dir, dir)])
      
    def calc_normal(self, point):
        return (point - self.center) / self.radius
    
class Plane(Surface):
    def __init__(self, point, normal, color, spectral_color, shininess):
        Surface.__init__(self, color, spectral_color, shininess)
        self.point = point
        self.normal = normal
        
    def hit_test(self, origin, dir):
        denom = numpy.dot(normalize(dir), normalize(self.normal))
        if denom == 0:
            return 0
        else:
            t = numpy.dot(normalize(self.normal), normalize((self.point - origin))) / denom
            if t < 0:
                return t
            else:
                return t
            
    def calc_normal(self, point):
        return self.normal

class Light():
    def __init__(self, position, color, spectral_color):
        self.position = position  
        self.color = color
        self.spectral_color = spectral_color
         
class Ray():
    def __init__(self, origin, dir):
        self.origin = origin
        self.dir = dir
       
class MainWindow(pyglet.window.Window):
    def __init__(self):
        
        super(MainWindow, self).__init__(caption ="pyRayTracer", width=window_width, height=window_height, resizable = False)

        self.scene = Scene()

    def on_draw(self):
        pass
             
    def on_key_release(self, symbol, modifiers):
        if symbol == key.Q:
            self.render_basic()
        elif symbol == key.W:
            self.render_lighting()
        elif symbol == key.E:
            self.render_lighting_shadowing()

    def render_basic(self):
        left = -(image_plane_width / 2)
        right = image_plane_width / 2
        bottom = -(image_plane_height / 2)
        top = image_plane_height / 2
        
        for i in range(window_width):
            # periodically print the percent completed
            if (i % 10) == 0:
                print str((float(i) / float(window_width)) * 100) + " %"
                
            for j in range(window_height):
                x = left + (((right - left)*(i + 0.5)) / window_width)
                y = bottom + (((top - bottom)*(j + 0.5)) / window_height)
                
                dir = normalize(numpy.array((x_axis * x) + (y_axis * y) + (z_axis * -viewpoint[2])))
                                
                ray_color = self.scene.shoot_ray(viewpoint, dir)
                
                pyglet.graphics.draw(1, GL_POINTS,('v2i', (i,j)),('c3f', ray_color))
    
    def render_lighting(self):
        pass
    
    def render_lighting_shadowing(self):
        pass
    
if __name__ == '__main__':
    window = MainWindow()
    pyglet.app.run()
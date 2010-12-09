from __future__ import division
import random
import pyglet
from pyglet.window import key
from pyglet.window import mouse
from pyglet.gl import *
import numpy
import Image

image_plane_width = 200
image_plane_height = 200
window_width = 500
window_height = 500

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

def distance(a, b):
    return numpy.abs(numpy.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2 + (a[2] - b[2])**2))

# 2d test
def point_inside_polygon(x,y,poly):
    n = len(poly)
    inside =False
    
    p1x,p1y,p1z = poly[0]
    for i in range(n+1):
        p2x,p2y,p2z = poly[i % n]
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x,p1y = p2x,p2y
    
    return inside
    
class Scene():
    def __init__(self):
        self.viewpoint = viewpoint
        self.image_plane_width = image_plane_width
        self.image_plane_height = image_plane_height
        self.objects = []
        self.lights = []
        self.background_color = numpy.array([0,0,0])
        self.ambient_color = numpy.array([0.2,0.2,0.2])
        
        # populate with object(s) and light(s)
        #self.add_object(Sphere(numpy.array([0,0, -305]), 100, numpy.array([1.0,0.0,0.0]), numpy.array([0.8,0.8,0.8]), 32, 0, True, random.random()))
        #self.add_object(Ellipsoid(1, 2, 1, numpy.array([0,0, -305]), 50, numpy.array([1.0,0.0,0.0]), numpy.array([0.8,0.8,0.8]), 32, 0, True, random.random()))
        self.add_object(Hyperboloid(1, 2, 1, numpy.array([0,0, -305]), 50, numpy.array([1.0,0.0,0.0]), numpy.array([0.8,0.8,0.8]), 32, 0, True, random.random()))
        #self.add_object(Sphere(numpy.array([30,0, -20]), 19, numpy.array([0.0,0.0,1.0]), numpy.array([0.8,0.8,0.8]), 32, 1.51, False, random.random()))
        self.add_object(Sphere(numpy.array([5,0, -20]), 19, numpy.array([0.0,0.0,1.0]), numpy.array([0.8,0.8,0.8]), 32, 1.51, False, random.random()))
        #self.add_object(Plane(numpy.array([-1000,0,-10]), numpy.array([1,0,0]), numpy.array([1.0,0.0,1.0]), numpy.array([0.8,0.8,0.8]), 32, True, random.random()))
        self.add_light(Light(numpy.array([200,50,50]), numpy.array([1,1,1]), numpy.array([0.5,0.5,0.5])))


        # scene 1
        self.add_object(Ellipsoid(1, 2, 1, numpy.array([-50, 0, -100]), 50, numpy.array([1.0,0.0,0.0]), numpy.array([0.8,0.8,0.8]), 32, 0, True, random.random()))
        self.add_object(Sphere(numpy.array([50,0, -50]), 40, numpy.array([0.0,0.0,1.0]), numpy.array([0.8,0.8,0.8]), 32, 20, False, random.random()))
        self.add_object(Sphere(numpy.array([50,30, -70]), 40, numpy.array([0,1.0,0.0]), numpy.array([0.8,0.8,0.8]), 32, 0, False, random.random()))
        self.add_object(Square(numpy.array([numpy.array([-20,20,-30]), numpy.array([20,20,-10]), numpy.array([20,0,-20]), numpy.array([-20,0,-20])]), numpy.array([1.0,0.0,1.0]), numpy.array([0.8,0.8,0.8]), 32, 0, False, random.random()))
        self.add_light(Light(numpy.array([10,10,0]), numpy.array([1,1,1]), numpy.array([0.5,0.5,0.5])))
        
    def add_object(self, object):
        self.objects.append(object)

    def add_light(self, light):
        self.lights.append(light)
        
    def shoot_ray(self, origin, dir, options):
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
        
        # if we get to here then at least one object was hit
        object = hit_objects[0]
        color = object.color
        point = origin + intersections[0] * dir
        
        # calculate lighting effects
        if options.find('l') != -1:
            color = self.__calc_lighting(object, point)

        # calculate transparency
        if options.find('t') != -1:            
            if object.transparency >= 1:
                color = self.shoot_transparency_ray(object, point, dir, object.calc_normal(point), id)                                

        # calculate reflection
        if options.find('r') != -1:
            if object.reflective == True:
                temp_color = self.shoot_reflection_ray(point, dir, object.calc_normal(point), id)
                if temp_color != None:
                    color = temp_color
         
        # determine if in shadow
        if options.find('s') != -1:
            if self.shoot_shadow_ray(point, normalize(self.lights[0].position - point), object.id) == True:
                color = self.ambient_color * object.color
                    
        return color
    
    def shoot_shadow_ray(self, origin, dir, id):
        hit_objects = []
        
        # see which objects the ray hits, other than the object the ray originated from
        for object in self.objects:
            if object.id != id:
                intersection_value = object.hit_test(origin, dir)
                if(intersection_value > 0):                              
                    hit_objects.append(object)
                
        if len(hit_objects) > 0:
            return True
        else:
            return False
        
    def shoot_transparency_ray(self, OrigObject, origin, dir, normal, id):
        n = 1.00 # refractive index of air
        nt = 1.50  # refractive index of flint glass
        
        dir = normalize(dir)        
        
        
        #book's way
        sqrt = 1 - (n**2 * (1-(numpy.dot(dir,normal)**2))) / nt**2                
        if(sqrt < 0):     
            print 'wrong'       
            return numpy.array([0,0,0]) #All energy REFLECTED, no refracted ray, should absorb reflected ray
        else:
            #from powerpoint
            #Nr = n/nt
            Nr = 1/nt
            dotNI = numpy.dot(normal, -dir)
            tVector = normalize((Nr*dotNI - numpy.sqrt(1 - Nr**2 * (1-dotNI**2))) * normal - (Nr*-dir))
                  
            
            intersections = []
            hit_objects = []
            color = self.background_color
            
            # see which objects the ray hits
            for object in self.objects: 
                if object.id != id:               
                    intersection_value = object.hit_test(origin, tVector)
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
                print "didn't hit anything"
                return numpy.array([0,0,0])                                     
                #return OrigObject.color
            
            # if we get to here then at least one object was hit
            object = hit_objects[0]
            color = object.color            
            point = origin + intersections[0] * dir
            
            # calculate lighting effects
            color = self.__calc_lighting(object, point)
            
            c = numpy.dot(tVector, -normal)
            
            
            R0 = ((nt-1)**2) / ((nt+1)**2)
            R = R0 + (((1-R0)*(1-c))**5)
            
            newColor = (((R) * OrigObject.color) + ((1-R) * color))
                        
            return newColor
                            
    def shoot_reflection_ray(self, origin, incident, normal, id):
        c1 = -numpy.dot(incident, normal)
        Rl = incident + (2 * normal * c1 ) 
        
        intersections = []
        hit_objects = []
        
        # see which objects the ray hits
        for object in self.objects:
            intersection_value = object.hit_test(origin, Rl)
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
            return None
        
        # if we get to here then at least one object was hit
        object = hit_objects[0]
        point = origin + intersections[0] * Rl
        
        color = self.__calc_lighting(object, point)

        print 'reflection hit'
        return color

    # remember that not taking the abs value causes weird problems
    
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
        test = numpy.dot(li, n)
        if test < 0:
            return numpy.array([0,0,0])
        else:
            return kd * test * Idi
    
    def __calc_Is(self, ks, n, h, s, Isi):
            
        return Isi * (numpy.abs(numpy.dot(n, h)) ** s)
                   
class Surface():
    def __init__(self, color, spectral_color, shininess, transparency, reflective, id):
        self.color = color
        self.spectral_color = spectral_color
        self.shininess = shininess
        self.reflective = reflective
        self.transparency = transparency
        self.id = id
        
    
    def hit_test(self):
        pass
    
    def calc_normal(self):
        pass
    
class Sphere(Surface):
    def __init__(self, center, radius, color, spectral_color, shininess, transparency, reflective, id):
        Surface.__init__(self, color, spectral_color, shininess, transparency, reflective, id)
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

class Ellipsoid(Surface):
    def __init__(self, A, B, C, center, radius, color, spectral_color, shininess, transparency, reflective, id):
        Surface.__init__(self, color, spectral_color, shininess, transparency, reflective, id)
        self.center = center
        self.radius = radius 
        self.A = A
        self.B = B
        self.C = C
        
    def hit_test(self, origin, dir):
        origin = ([origin[0]/self.A, origin[1]/self.B, origin[2]/self.C])
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

class Hyperboloid(Surface):
    def __init__(self, A, B, C, center, radius, color, spectral_color, shininess, transparency, reflective, id):
        Surface.__init__(self, color, spectral_color, shininess, transparency, reflective, id)
        self.center = center
        self.radius = radius 
        self.A = A
        self.B = B
        self.C = C
        
    def hit_test(self, origin, dir):
        origin = ([origin[0]/self.A, origin[1]/self.B, -origin[2]/self.C])
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
    def __init__(self, point, normal, color, spectral_color, shininess, reflective, id):
        Surface.__init__(self, color, spectral_color, shininess, reflective, id)
        self.point = point
        self.normal = normal

    def hit_test(self, origin, dir):
        denom = numpy.dot(normalize(dir), normalize(self.normal))
        if denom == 0:
            return -1
        else:
            return numpy.dot(normalize(self.normal), normalize((self.point - origin))) / denom
            
    def calc_normal(self, point):
        return self.normal

class Triangle(Surface):
    def __init__(self, points, color, spectral_color, shininess, transparency, reflective, id):
        Surface.__init__(self, color, spectral_color, shininess, transparency, reflective, id)
        self.points = points
        self.v1 = normalize(points[1] - points[0])
        self.v2 = normalize(points[2] - points[1])
        self.v3 = normalize(points[1] - points[2])
        self.normal = numpy.cross(self.v1, self.v2)
        
    def hit_test(self, origin, dir):
        # first, do a ray / plane intersection test
        denom = numpy.dot(normalize(dir), normalize(self.normal))

        if denom == 0:
            return -1
        else: # the ray does intersect the plane
            intersection = numpy.dot(self.points[0] - origin, self.normal) / denom
            point = origin + (intersection * dir)
            
            if point_inside_polygon(point[0], point[1], self.points) == True:
                return intersection
            else:
                return -1
                    
    def calc_normal(self, point):
        return self.normal 
       
class Square(Surface):
    def __init__(self, points, color, spectral_color, shininess, transparency, reflective, id):
        Surface.__init__(self, color, spectral_color, shininess, transparency, reflective, id)
        self.points = points
        self.v1 = normalize(points[1] - points[0])
        self.v2 = normalize(points[2] - points[1])
        self.v3 = normalize(points[3] - points[2])
        self.v4 = normalize(points[0] - points[3])
        self.normal = -numpy.cross(self.v1, self.v2)

    def hit_test(self, origin, dir):
        # first, do a ray / plane intersection test
        denom = numpy.dot(normalize(dir), normalize(self.normal))
        
        if denom == 0:
            return -1
        else: # the ray does intersect the plane
            intersection = numpy.dot(self.points[0] - origin, self.normal) / denom
            point = origin + (intersection * dir)

            a1 = normalize(point - self.points[0])
            a2 = normalize(point - self.points[1])
            a3 = normalize(point - self.points[2])
            a4 = normalize(point - self.points[3]) 
            
            dot1 = numpy.dot(self.v1, a1)
            dot2 = numpy.dot(self.v2, a2)
            dot3 = numpy.dot(self.v3, a3)
            dot4 = numpy.dot(self.v4, a4)
            
            
            if (dot1 > 0) and (dot2 > 0) and (dot3 > 0) and (dot4 > 0):
                return intersection
            else:
                return -1
            
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
        elif symbol == key.R:
            self.render_lighting_reflection()
        elif symbol == key.T:
            self.render_lighting_transparency()

    def render_basic(self):
        left = -(image_plane_width / 2)
        right = image_plane_width / 2
        bottom = -(image_plane_height / 2)
        top = image_plane_height / 2
        
        pixels = []
        colors = []
        for i in range(window_width):
            # periodically print the percent completed
            if (i % 10) == 0:
                print str((float(i) / float(window_width)) * 100) + " %"
                
            for j in range(window_height):
                x = left + (((right - left)*(i + 0.5)) / window_width)
                y = bottom + (((top - bottom)*(j + 0.5)) / window_height)
                
#                dir = normalize(numpy.array((x_axis * x) + (y_axis * y) + (z_axis * -viewpoint[2])))            
#                ray_color = self.scene.shoot_ray(viewpoint, dir, '')
            
                dir = normalize(numpy.array([0,0,-1]))
                ortho_origin = numpy.array([x,y,0])
                ray_color = self.scene.shoot_ray(ortho_origin, dir, '')
                
                # it is much faster to create the list of pixels and colors, then call pyglet.graphics.draw once at the end
                pixels.append(i)
                pixels.append(j)
                colors.append(ray_color[0])
                colors.append(ray_color[1])
                colors.append(ray_color[2])
                
        pyglet.graphics.draw(int(len(pixels)/2), GL_POINTS,('v2i', pixels),('c3f', colors))
        
    def render_lighting(self):
        left = -(image_plane_width / 2)
        right = image_plane_width / 2
        bottom = -(image_plane_height / 2)
        top = image_plane_height / 2
        
        pixels = []
        colors = []
        for i in range(window_width):
            # periodically print the percent completed
            if (i % 10) == 0:
                print str((float(i) / float(window_width)) * 100) + " %"
                
            for j in range(window_height):
                x = left + (((right - left)*(i + 0.5)) / window_width)
                y = bottom + (((top - bottom)*(j + 0.5)) / window_height)
                
#                dir = normalize(numpy.array((x_axis * x) + (y_axis * y) + (z_axis * -viewpoint[2])))            
#                ray_color = self.scene.shoot_ray(viewpoint, dir, 'l')
            
                dir = normalize(numpy.array([0,0,-1]))
                ortho_origin = numpy.array([x,y,0])
                ray_color = self.scene.shoot_ray(ortho_origin, dir, 'l')
                
                # it is much faster to create the list of pixels and colors, then call pyglet.graphics.draw once at the end
                pixels.append(i)
                pixels.append(j)
                colors.append(ray_color[0])
                colors.append(ray_color[1])
                colors.append(ray_color[2])
                
        pyglet.graphics.draw(int(len(pixels)/2), GL_POINTS,('v2i', pixels),('c3f', colors))
    
    def render_lighting_shadowing(self):
        left = -(image_plane_width / 2)
        right = image_plane_width / 2
        bottom = -(image_plane_height / 2)
        top = image_plane_height / 2
        
        pixels = []
        colors = []
        for i in range(window_width):
            # periodically print the percent completed
            if (i % 10) == 0:
                print str((float(i) / float(window_width)) * 100) + " %"
                
            for j in range(window_height):
                x = left + (((right - left)*(i + 0.5)) / window_width)
                y = bottom + (((top - bottom)*(j + 0.5)) / window_height)
                
#                dir = normalize(numpy.array((x_axis * x) + (y_axis * y) + (z_axis * -viewpoint[2])))            
#                ray_color = self.scene.shoot_ray(viewpoint, dir, 'ls')
            
                dir = normalize(numpy.array([0,0,-1]))
                ortho_origin = numpy.array([x,y,0])
                ray_color = self.scene.shoot_ray(ortho_origin, dir, 'ls')
                
                # it is much faster to create the list of pixels and colors, then call pyglet.graphics.draw once at the end
                pixels.append(i)
                pixels.append(j)
                colors.append(ray_color[0])
                colors.append(ray_color[1])
                colors.append(ray_color[2])
                
        pyglet.graphics.draw(int(len(pixels)/2), GL_POINTS,('v2i', pixels),('c3f', colors))

    def render_lighting_reflection(self):
        left = -(image_plane_width / 2)
        right = image_plane_width / 2
        bottom = -(image_plane_height / 2)
        top = image_plane_height / 2
        
        pixels = []
        colors = []
        for i in range(window_width):
            # periodically print the percent completed
            if (i % 10) == 0:
                print str((float(i) / float(window_width)) * 100) + " %"
                
            for j in range(window_height):
                x = left + (((right - left)*(i + 0.5)) / window_width)
                y = bottom + (((top - bottom)*(j + 0.5)) / window_height)
                
                #dir = normalize(numpy.array((x_axis * x) + (y_axis * y) + (z_axis * -viewpoint[2])))            
                #ray_color = scene.shoot_ray(viewpoint, dir)
            
                dir = normalize(numpy.array([0,0,-1]))
                ortho_origin = numpy.array([x,y,0])
                ray_color = self.scene.shoot_ray(ortho_origin, dir, 'lr')
                
                # it is much faster to create the list of pixels and colors, then call pyglet.graphics.draw once at the end
                pixels.append(i)
                pixels.append(j)
                colors.append(ray_color[0])
                colors.append(ray_color[1])
                colors.append(ray_color[2])
                
        pyglet.graphics.draw(int(len(pixels)/2), GL_POINTS,('v2i', pixels),('c3f', colors))
        
    def render_lighting_transparency(self):
        left = -(image_plane_width / 2)
        right = image_plane_width / 2
        bottom = -(image_plane_height / 2)
        top = image_plane_height / 2
        
        pixels = []
        colors = []
        for i in range(window_width):
            # periodically print the percent completed
            if (i % 10) == 0:
                print str((float(i) / float(window_width)) * 100) + " %"
                
            for j in range(window_height):
                x = left + (((right - left)*(i + 0.5)) / window_width)
                y = bottom + (((top - bottom)*(j + 0.5)) / window_height)
                
                #dir = normalize(numpy.array((x_axis * x) + (y_axis * y) + (z_axis * -viewpoint[2])))            
                #ray_color = scene.shoot_ray(viewpoint, dir)
            
                dir = normalize(numpy.array([0,0,-1]))
                ortho_origin = numpy.array([x,y,0])
                ray_color = self.scene.shoot_ray(ortho_origin, dir, 'lt')
                
                # it is much faster to create the list of pixels and colors, then call pyglet.graphics.draw once at the end
                pixels.append(i)
                pixels.append(j)                                      
                colors.append(ray_color[0])
                colors.append(ray_color[1])
                colors.append(ray_color[2])
                
        pyglet.graphics.draw(int(len(pixels)/2), GL_POINTS,('v2i', pixels),('c3f', colors))  

    def render_all(self):
        left = -(image_plane_width / 2)
        right = image_plane_width / 2
        bottom = -(image_plane_height / 2)
        top = image_plane_height / 2
        
        pixels = []
        colors = []
        for i in range(window_width):
            # periodically print the percent completed
            if (i % 10) == 0:
                print str((float(i) / float(window_width)) * 100) + " %"
                
            for j in range(window_height):
                x = left + (((right - left)*(i + 0.5)) / window_width)
                y = bottom + (((top - bottom)*(j + 0.5)) / window_height)
                
                #dir = normalize(numpy.array((x_axis * x) + (y_axis * y) + (z_axis * -viewpoint[2])))            
                #ray_color = scene.shoot_ray(viewpoint, dir)
            
                dir = normalize(numpy.array([0,0,-1]))
                ortho_origin = numpy.array([x,y,0])
                ray_color = self.scene.shoot_ray(ortho_origin, dir, 'lsrt')
                
                # it is much faster to create the list of pixels and colors, then call pyglet.graphics.draw once at the end
                pixels.append(i)
                pixels.append(j)                                      
                colors.append(ray_color[0])
                colors.append(ray_color[1])
                colors.append(ray_color[2])
                
        pyglet.graphics.draw(int(len(pixels)/2), GL_POINTS,('v2i', pixels),('c3f', colors)) 
        
def render_PIL(scene):
    img = Image.new("RGB", (window_width, window_height))
    img_pix = img.load()
     
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
            
            #dir = normalize(numpy.array((x_axis * x) + (y_axis * y) + (z_axis * -viewpoint[2])))            
            #ray_color = scene.shoot_ray(viewpoint, dir)
        
            dir = normalize(numpy.array([0,0,-1]))
            ortho_origin = numpy.array([x,y,0])
            ray_color = scene.shoot_ray(ortho_origin, dir)
            
            #img.putpixel((i,j), (ray_color[0] * 255, ray_color[1] * 255, ray_color[2] * 255)) # since we are using floats, must convert to integer
            img_pix[i,j] = (ray_color[0] * 255, ray_color[1] * 255, ray_color[2] * 255)
     
    img.save("../../test.bmp")
    print "Finished"
        
if __name__ == '__main__':
    window = MainWindow()
    pyglet.app.run()
    
#    scene = Scene()
#    render_PIL(scene)
    

    
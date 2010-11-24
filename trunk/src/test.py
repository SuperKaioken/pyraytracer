import numpy
import math

import scene, rays, objects
VIEWPOINT = [0,0,5]

scene = scene.Scene() 
rays = rays.Rays(150, 150, -VIEWPOINT[2], 150, 150)
object1 = objects.Sphere(numpy.array([0, 0, -1]), 5, [1.0, 0.0, 0.0])

direction = rays.get_ray_direction()
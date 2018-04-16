# This file contains objects which can collide with the puck

# Each coll_time() function returns how many seconds it'll take before
# the puck collides with the object

# Each collide_velocity() returns the velocity of the puck after the next 
# collision with the object

import math

# Fraction of velocity puck retains in a collision with a wall
wall_coll_const = .95

# Returns velocity of object with velocity v after collision with wall
# with collision constant coll_const
def collide_horz(v, coll_const):
    return Vector(-coll_Const*v.x, v.y)

# Left facing infinite vertical wall
class Wall_Vert_Left_Inf:

    def __init__(self, x):
        self.x = x
        
    def coll_time(self, puck):

        if puck.velocity.x <= 0 or puck.location.x > self.x:
            # There will be no collision
            return None

        return (self.x - (puck.location.x + puck.radius)) / puck.velocity.x

    def collide_velocity(self, puck, coll_point):
        
        return collide_horz(puck.velocity, wall_coll_const)

# Right facing infinite vertical wall
class Wall_Vert_Right_Inf:

    def __init__(self, x):
        self.x = x
        
    def coll_time(self, puck):

        if puck.velocity.x >= 0 or puck.location.x < self.x:
            # There will be no collision
            return None

        return ((puck.location.x - puck.radius) - self.x) / -puck.velocity.x

    def collide_velocity(self, puck, coll_point):
        
        return puck.velocity.flip_horz() * wall_coll_const

# Up facing infinite horizontal wall
class Wall_Horz_Up_Inf:

    def __init__(self, y):
        self.y = y
        
    def coll_time(self, puck):

        if puck.velocity.y <= 0 or puck.location.y > self.y:
            # There will be no collision
            return None

        return (self.y - (puck.location.y + puck.radius)) / puck.velocity.y

    def collide_velocity(self, puck, coll_point):
        
        return puck.velocity.flip_vert() * wall_coll_const

# Down facing infinite horizontal wall
class Wall_Horz_Down_Inf:

    def __init__(self, y):
        self.y = y
        
    def coll_time(self, puck):

        if puck.velocity.y >= 0 or puck.location.y < self.y:
            # There will be no collision
            return None

        return ((puck.location.y - puck.radius) - self.y) / -puck.velocity.y

    def collide_velocity(self, puck, coll_point):
        
        return puck.velocity.flip_vert() * wall_coll_const

# Left facing finite vertical wall
class Wall_Vert_Left:

    def __init__(self, x, y_1, y_2):
        self.x = x
        self.y_low = min(y_1, y_2)
        self.y_high = max(y_1, y_2)
        
    def coll_time(self, puck):

        if puck.velocity.x <= 0 or puck.location.x + puck.radius > self.x:
            # There will be no collision
            return None

        coll_time = (self.x - (puck.location.x + puck.radius)) / puck.velocity.x
        coll_y = puck.location.y + coll_time * puck.velocity.y

        # Collisions only happen when the center of the puck is in the horizontal 
        # region along the wall
        if coll_y < self.y_low or coll_y > self.y_high: 
            return None

        return coll_time

    def collide_velocity(self, puck, coll_point):
        
        return puck.velocity.flip_horz() * wall_coll_const

# Left facing finite vertical wall
class Wall_Vert_Right:

    def __init__(self, x, y_1, y_2):
        self.x = x
        self.y_low = min(y_1, y_2)
        self.y_high = max(y_1, y_2)
        
    def coll_time(self, puck):

        if puck.velocity.x >= 0 or puck.location.x - puck.radius < self.x:
            # There will be no collision
            return None

        coll_time = ((puck.location.x - puck.radius) - self.x) / -puck.velocity.x
        coll_y = puck.location.y + coll_time * puck.velocity.y

        # Collisions only happen when the center of the puck is in the horizontal 
        # region along the wall
        if coll_y < self.y_low or coll_y > self.y_high: 
            return None

        return coll_time

    def collide_velocity(self, puck, coll_point):
        
        return puck.velocity.flip_horz() * wall_coll_const

# Up facing finite horizontal wall
class Wall_Horz_Up:

    def __init__(self, x_1, x_2, y):
        self.x_low = min(x_1, x_2)
        self.x_high = max(x_1, x_2)
        self.y = y
        
    def coll_time(self, puck):

        if puck.velocity.y <= 0 or puck.location.y + puck.radius > self.y:
            # There will be no collision
            return None

        coll_time = (self.y - (puck.location.y + puck.radius)) / puck.velocity.y
        coll_x = puck.location.x + coll_time * puck.velocity.x

        # Collisions only happen when the center of the puck is in the horizontal 
        # region along the wall
        if coll_x < self.x_low or coll_x > self.x_high: 
            return None

        return coll_time

    def collide_velocity(self, puck, coll_point):
        
        return puck.velocity.flip_vert() * wall_coll_const

# Down facing finite horizontal wall
class Wall_Horz_Down:

    def __init__(self, x_1, x_2, y):
        self.x_low = min(x_1, x_2)
        self.x_high = max(x_1, x_2)
        self.y = y
        
    def coll_time(self, puck):

        if puck.velocity.y >= 0 or puck.location.y - puck.radius < self.y:
            # There will be no collision
            return None

        coll_time = ((puck.location.y - puck.radius) - self.y) / -puck.velocity.y
        coll_x = puck.location.x + coll_time * puck.velocity.x

        # Collisions only happen when the center of the puck is in the horizontal 
        # region along the wall
        if coll_x < self.x_low or coll_x > self.x_high: 
            return None

        return coll_time

    def collide_velocity(self, puck, coll_point):
        
        return puck.velocity.flip_vert() * wall_coll_const

class Circle:

    def __init__(self, location, radius):
        self.location = location 
        self.radius = radius
        # Object can't collide 
        self.ghost = False

    # Note: the following webpage was helpful when working out the math of 
    # this function. Reading it may help when following this algorithm
    #   https://math.stackexchange.com/questions/913350/
    #   how-to-find-the-intersection-point-of-two-moving-circles
    def coll_time(self, obj2):

        if self.ghost:
            return None

        # Static pucks can't collide with other objects
        if obj2.velocity.mag() == 0:
            return None

        # Prevent divisions by zero
        if self.location == obj2.location:
            return None

        # First find the closest distance that will occur between 
        # the circle centers
        v_diff = self.location - obj2.location 

        # No collision if obj2 is moving away from circle
        if v_diff * obj2.velocity < 0:
            return None

        # Angle between obj2 path and initial vector to circle
        path_ang = obj2.velocity.ang() - v_diff.ang()
        # Simple trig application:
        d_min = v_diff.mag() * abs(math.sin(path_ang))

        if self.radius + obj2.radius <= d_min:
            # There will be no collision 
            return None

        # Distance from the start position of the obj2 to the point of 
        # minimum distance to the circle
        d_s_m = v_diff.mag() * abs(math.cos(path_ang))
        # Distance from the collision point to the point of minimum distance
        # to the circle
        d_c_m = math.sqrt((self.radius + obj2.radius) * (self.radius + obj2.radius)
                          - d_min * d_min)
        d_s_c = d_s_m - d_c_m
        return d_s_c / obj2.velocity.mag()

    def collide_velocity(self, obj2, coll_point):

        reflection_axis = self.location - coll_point

        return obj2.velocity.flip(reflection_axis) * self.coll_const

    # Is the obj2 passing through this circle?
    def intersecting(self, c2):
        
        return (c2.location - self.location).mag() < c2.radius + self.radius

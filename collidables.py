# This file contains objects which can collide with the puck

# Each coll_time() function returns how many seconds it'll take before
# the puck collides with the object

# Each collide_velocity() returns the velocity of the puck after the next 
# collision with the object

# Left facing infinite vertical wall
class Wall_Vert_Left_Inf:

    def __init__(self, x):
        self.x = x
        
    def coll_time(self, puck):

        if puck.velocity.x <= 0 or puck.location.x > self.x:
            # There will be no collision
            return None

        return (self.x - (puck.location.x + puck.radius)) / puck.velocity.x

    def collide_velocity(self, puck):
        
        return puck.velocity.flip_horz()

# Right facing infinite vertical wall
class Wall_Vert_Right_Inf:

    def __init__(self, x):
        self.x = x
        
    def coll_time(self, puck):

        if puck.velocity.x >= 0 or puck.location.x < self.x:
            # There will be no collision
            return None

        return ((puck.location.x - puck.radius) - self.x) / -puck.velocity.x

    def collide_velocity(self, puck):
        
        return puck.velocity.flip_horz()

# Up facing infinite horizontal wall
class Wall_Horz_Up_Inf:

    def __init__(self, y):
        self.y = y
        
    def coll_time(self, puck):

        if puck.velocity.y <= 0 or puck.location.y > self.y:
            # There will be no collision
            return None

        return (self.y - (puck.location.y + puck.radius)) / puck.velocity.y

    def collide_velocity(self, puck):
        
        return puck.velocity.flip_vert()

# Down facing infinite horizontal wall
class Wall_Horz_Down_Inf:

    def __init__(self, y):
        self.y = y
        
    def coll_time(self, puck):

        if puck.velocity.y >= 0 or puck.location.y < self.y:
            # There will be no collision
            return None

        return ((puck.location.y - puck.radius) - self.y) / -puck.velocity.y

    def collide_velocity(self, puck):
        
        return puck.velocity.flip_vert()

class Circle:

    def __init__(self, location, radius):
        self.location = location 
        self.radius = radius

    # Note: the following webpage was helpful when working out the math of 
    # this function. Reading it may help when following this algorithm
    #   https://math.stackexchange.com/questions/913350/
    #   how-to-find-the-intersection-point-of-two-moving-circles
    def coll_time(self, puck):

        # First find the closest distance that will occur between 
        # the circle centers
        v_diff = self.location - puck.location 
        # Angle between puck path and intial vector to circle
        path_ang = abs(puck.velocity.ang() - v_diff.ang())
        # Simple trig application:
        d_min = v_diff.mag() * math.sin(path_ang) 

        if self.radius + puck.radius < d_min:
            # There will be no collision 
            return None

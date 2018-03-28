# This file contains objects which can collide with the puck

# Each coll_time() function returns how many seconds it'll take before
# the puck collides with the object

# Each collide() function returns the tuple (new_loc, new_vel),
# Where new_loc is the location of the puck after the collision and
# new_vel is its velocity

# Left facing infinite vertical wall
class Wall_Vert_Left_Inf:

    def __init__(self, x):
        self.x = x
        
    def coll_time(self, puck):

        if puck.velocity.x <= 0 or puck.location.x > self.x:
            # There will be no collision
            return None

        return (self.x - (puck.location.x + puck.radius)) / puck.velocity.x

    def collide(self, puck):
        
        coll_time = self.coll_time(puck)
        new_loc = puck.location + puck.velocity * coll_time
        new_vel = puck.velocity.flip_horz()

        return (new_loc, new_vel)

# Right facing infinite vertical wall
class Wall_Vert_Right_Inf:

    def __init__(self, x):
        self.x = x
        
    def coll_time(self, puck):

        if puck.velocity.x >= 0 or puck.location.x < self.x:
            # There will be no collision
            return None

        return ((puck.location.x - puck.radius) - self.x) / -puck.velocity.x

    def collide(self, puck):
        
        coll_time = self.coll_time(puck)
        new_loc = puck.location + puck.velocity * coll_time
        new_vel = puck.velocity.flip_horz()

        return (new_loc, new_vel)

# Up facing infinite horizontal wall
class Wall_Horz_Up_Inf:

    def __init__(self, y):
        self.y = y
        
    def coll_time(self, puck):

        if puck.velocity.y <= 0 or puck.location.y > self.y:
            # There will be no collision
            return None

        return (self.y - (puck.location.y + puck.radius)) / puck.velocity.y

    def collide(self, puck):
        
        coll_time = self.coll_time(puck)
        new_loc = puck.location + puck.velocity * coll_time
        new_vel = puck.velocity.flip_vert()

        return (new_loc, new_vel)

# Down facing infinite horizontial wall
class Wall_Horz_Down_Inf:

    def __init__(self, y):
        self.y = y
        
    def coll_time(self, puck):

        if puck.velocity.y >= 0 or puck.location.y < self.y:
            # There will be no collision
            return None

        return ((puck.location.y - puck.radius) - self.y) / -puck.velocity.y

    def collide(self, puck):
        
        coll_time = self.coll_time(puck)
        new_loc = puck.location + puck.velocity * coll_time
        new_vel = puck.velocity.flip_vert()

        return (new_loc, new_vel)

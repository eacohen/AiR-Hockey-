# Simple class for vector operations

import math

class Vector:                                                                                    

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "<" + str(self.x) + ", " + str(self.y) + ">" 

    def __add__(self, v2):
        return Vector(self.x + v2.x, self.y + v2.y)

    def __sub__(self, v2):
        return Vector(self.x - v2.x, self.y - v2.y)

    def __eq__(self, v2):
        return self.x == v2.x and self.y == v2.y

    def polar(mag, ang):
        return Vector(mag * math.cos(ang), mag * math.sin(ang))

    # Return the magnitude squared (Cheaper than finding the magnitude first)
    def mag_sq(self):
        return self.x * self.x + self.y * self.y

    # Return the magnitude 
    def mag(self):
        return math.sqrt(self.mag_sq())

    # Return the angle
    def ang(self):
        return atan(self.y, self.x) 

    # Both scaler multiplication and dot product
    def __mul__(self, arg2):

        # Dot product
        if isinstance(arg2, Vector):
            return self.x * arg2.x + self.y * arg2.y
        # Scalar multiplication
        else:
            return Vector(self.x * arg2, self.y * arg2)

    # Support scalar multiplication in both directions
    __rmul__ = __mul__

    def __truediv__(self, scaler):
        return Vector(self.x / scaler, self.y / scaler)

    # Return the unit vector (magnitude of one) corresponding to this vector
    def normalize(self):

        mag = self.mag()

        if mag == 0:
            # Zero length vectors have no normal
            return None

        return self / mag

    def flip_horz(self):
        return Vector(-self.x, self.y)

    def flip_vert(self):
        return Vector(self.x, -self.y)

    # Flip a vector across a "flip axis" vector so that the vector's value in 
    # the axis of the flip is negated but in the axis perpendicular to the flip
    # stays the same
    # This can model a puck reflecting off a wall, where the normal vector to the wall
    # is the flip axis
    # Diagram:
    #
    # \ <- self
    #  \
    #   *
    # --------  <- direction of flip axis
    #   /
    #  /
    # * <- result
    #
    def flip(self, flip_axis):
        normal = flip_axis.normalize()
        return self - 2 * (self * normal) * normal


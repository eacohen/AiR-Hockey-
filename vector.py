# Simple class for vector operations
class Vector:                                                                                    

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, v2):
        return Vector(self.x + v2.x, self.y + v2.y)

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

    def flip_horz(self):
        return Vector(-self.x, self.y)

    def flip_vert(self):
        return Vector(self.x, -self.y)


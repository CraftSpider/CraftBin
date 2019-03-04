
import math
import numbers


class Vector:

    __slots__ = ("x", "y", "z")

    x: numbers.Real
    y: numbers.Real
    z: numbers.Real

    def __init__(self, x, y=None, z=None):
        if not isinstance(x, numbers.Real):
            raise TypeError("Vector arguments must be a number or vector")
        self.x = x
        if z is None:
            self.y = x
            self.z = x
        else:
            self.y = y
            self.z = z

    def __str__(self):
        return f"Vector(x={self.x}, y={self.y}, z={self.z})"

    def __int__(self):
        raise TypeError("Vectors cannot be implicitly converted to an integer")

    def __float__(self):
        return self.flatten()

    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y, self.z + other.z)
        else:
            return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x - other.x, self.y - other.y, self.z - other.z)
        else:
            return NotImplemented

    def __mul__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x * other.x, self.y * other.y, self.z * other.z)
        else:
            return NotImplemented

    def __matmul__(self, other):
        return self.cross(other)

    def __truediv__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x / other.x, self.y / other.y, self.z / other.z)
        else:
            return NotImplemented

    def __floordiv__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x // other.x, self.y / other.y, self.z / other.z)
        else:
            return NotImplemented

    def __neg__(self):
        return Vector(-self.x, -self.y, -self.z)

    def __abs__(self):
        return self.flatten()

    def __round__(self, n=None):
        return Vector(round(self.x, n), round(self.y, n), round(self.z, n))

    def __trunc__(self):
        return Vector(math.trunc(self.x), math.trunc(self.y), math.trunc(self.z))

    def __floor__(self):
        return Vector(math.floor(self.x), math.floor(self.y), math.floor(self.z))

    def __ceil__(self):
        return Vector(math.ceil(self.x), math.ceil(self.y), math.ceil(self.z))

    def flatten(self):
        return (self.x**2 + self.y**2 + self.z**2)**.5

    def cross(self, other):
        if not isinstance(other, Vector):
            raise TypeError("Attempt to cross vector with invalid type")
        x = self.y * other.z - self.z * other.y
        y = self.z * other.x - self.x * other.z
        z = self.x * other.y - self.y * other.x
        return Vector(x, y, z)


Vector.Unit = Vector(1)
Vector.Zero = Vector(0)
Vector.UnitX = Vector(1, 0, 0)
Vector.UnitY = Vector(0, 1, 0)
Vector.UnitZ = Vector(0, 0, 1)


if __name__ == "__main__":
    vec = Vector(1, 0, 0)
    vec2 = Vector(0, 1, 0)
    print(math.trunc(vec))
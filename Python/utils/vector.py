
import math
import numbers


class Vector2:

    __slots__ = ("x", "y")

    def __init__(self, x, y=None):
        if not isinstance(x, numbers.Real):
            raise TypeError("Vector2 arguments must be a number or vector")
        self.x = x
        if y is None:
            self.y = x
        else:
            self.y = y

    def __repr__(self):
        return f"Vector2(x={self.x}, y={self.y})"

    def __int__(self):
        raise TypeError("Vectors cannot be implicitly converted to an integer. Use abs() or .flatten")

    def __float__(self):
        return self.flatten()

    def __add__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x + other.x, self.y + other.y)
        else:
            return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x + other.x, self.y + other.y)
        else:
            return NotImplemented

    def __mul__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x * other.x, self.y * other.y)
        else:
            return NotImplemented

    def __truediv__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x / other.x, self.y / other.y)
        else:
            return NotImplemented

    def __floordiv__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x // other.x, self.y // other.y)
        else:
            return NotImplemented

    def __neg__(self):
        return Vector2(-self.x, -self.y)

    def __abs__(self):
        return self.flatten()

    def __round__(self, n=None):
        return Vector2(round(self.x, n), round(self.y, y))

    def __trunc__(self):
        return Vector2(math.trunc(self.x), math.trunc(self.y))

    def __floor__(self):
        return Vector2(math.floor(self.x), math.floor(self.y))

    def __ceil__(self):
        return Vector2(math.ceil(self.x), math.ceil(self.y))

    def flatten(self):
        return (self.x**2 + self.y**2)**.5

    def to_3d(self):
        return Vector(self.x, self.y, 0)


class Vector:

    __slots__ = ("x", "y", "z")

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

    def __repr__(self):
        return f"Vector(x={self.x}, y={self.y}, z={self.z})"

    def __int__(self):
        raise TypeError("Vectors cannot be implicitly converted to an integer. Use abs() or .flatten")

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
        elif isinstance(other, numbers.Real):
            return Vector(self.x - other, self.y - other, self.z - other)
        else:
            return NotImplemented

    def __mul__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x * other.x, self.y * other.y, self.z * other.z)
        elif isinstance(other, numbers.Real):
            return Vector(self.x * other, self.y * other, self.z * other)
        else:
            return NotImplemented

    def __rmul__(self, other):
        return self.__mul__(other)

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

    def to_2d(self):
        return Vector2(self.x, self.y)


UnitX = Vector(1, 0, 0)
UnitY = Vector(0, 1, 0)
UnitZ = Vector(0, 0, 1)

Vector.Unit = Vector(1)
Vector.Zero = Vector(0)
Vector.UnitX = UnitX
Vector.UnitY = UnitY
Vector.UnitZ = UnitZ

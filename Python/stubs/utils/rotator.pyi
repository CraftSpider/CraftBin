
import numbers

from .vector import Vector

class Rotator:

    __slots__ = ("x", "y", "z")

    x: numbers.Real
    y: numbers.Real
    z: numbers.Real

    def __init__(self, x: numbers.Real, y: numbers.Real = ..., z: numbers.Real = ..., radians: bool = ...) -> None: ...

    def __repr__(self) -> str: ...

    def __mul__(self, other: Vector) -> Vector: ...

    def __rmul__(self, other: Vector) -> Vector: ...


import enum


class Side(enum.Enum):

    def __new__(cls, tl, tr, axis):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._top_left = tl
        obj._bottom_right = tr
        obj._axis = axis
        obj._value_ = value
        return obj

    UP = (0, 3, "y")
    DOWN = (7, 4, "-y")
    NORTH = (1, 4, "-z")
    SOUTH = (2, 7, "z")
    EAST = (3, 5, "x")
    WEST = (0, 6, "-x")

    @property
    def tl(self):
        return self._top_left

    @property
    def br(self):
        return self._bottom_right

    @property
    def ids(self):
        return self._top_left, self._bottom_right

    @property
    def axis(self):
        return self._axis

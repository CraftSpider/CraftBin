
from typing import Tuple
import enum

class Side(enum.Enum):

    def __new__(cls, tl, tr, axis) -> Side: ...

    UP = ()
    DOWN = ()
    NORTH = ()
    SOUTH = ()
    EAST = ()
    WEST = ()

    @property
    def tl(self) -> int: ...

    @property
    def tr(self) -> int: ...

    @property
    def ids(self) -> Tuple[int, int]: ...

    @property
    def axis(self) -> str: ...


import enum


class Direction(enum.Enum):
    UP = enum.auto()
    DOWN = enum.auto()
    LEFT = enum.auto()
    RIGHT = enum.auto()

    def reverse(self):
        return self[self.value() + 2 % 4]


class BlockType(enum.Enum):
    FUNCTION = enum.auto()
    CLASS = enum.auto()
    EXTERN = enum.auto()


class TokenType:
    STRING = enum.auto()
    NUM = enum.auto()
    VAR = enum.auto()
    REF = enum.auto()

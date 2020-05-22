"""Enumerations used in path finding."""
from enum import Enum
import random


class Field(Enum):
    """Field enum based on the type of input data."""
    NORMAL = 0
    WALL = 1
    AGENT = 5
    EXIT = 8


def U(point):
    """Move up in the maze."""
    return (point[0]-1, point[1])


def D(point):
    """Move down in the maze."""
    return (point[0]+1, point[1])


def L(point):
    """Move left in the maze."""
    return (point[0], point[1]-1)


def R(point):
    """Move right in the maze."""
    return (point[0], point[1]+1)


class Directions(bytes, Enum):
    """Directions enum with self function assignment."""
    def __new__(cls, value, function):
        obj = bytes.__new__(cls, [value])
        obj._value_ = value
        obj.move = function
        return obj

    UP = (0, U)
    LEFT = (1, L)
    DOWN = (2, D)
    RIGHT = (3, R)


def turn(direction):
    """Turn randomly left or right."""
    return Directions(random.choice([(direction.value + 1), (direction.value + 3)]) % 4)


def opposite_dir(direction):
    """Turn to opposite direction."""
    return Directions((direction.value + 2) % 4)

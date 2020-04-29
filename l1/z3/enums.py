from enum import Enum
import random

class Field(Enum):
    NORMAL = 0
    WALL = 1
    AGENT = 5
    EXIT = 8

def U(point):
    return (point[0]-1, point[1])


def D(point):
    return (point[0]+1, point[1])


def L(point):
    return (point[0], point[1]-1)


def R(point):
    return (point[0], point[1]+1)

class Directions(bytes, Enum):
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
    return Directions(random.choice([(direction.value + 1), (direction.value + 3)]) % 4)

def opposite_dir(direction):
    return Directions((direction.value + 2) % 4)

from enum import Enum


class Level(Enum):
    EASY = 0
    MEDIUM = 1
    HARD = 2


class Color(Enum):
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)

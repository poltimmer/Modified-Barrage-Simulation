from enum import Enum

class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    def get_dx(self) -> int:
        if (self == RIGHT):
            return 1
        elif (self == LEFT):
            return -1
        else:
            return 0

    def get_dy(self) -> int:
        if (self == UP):
            return 1
        elif (self == DOWN):
            return -1
        else:
            return 0
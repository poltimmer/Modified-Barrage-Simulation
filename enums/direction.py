from enum import Enum


class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    def get_dx(self) -> int:
        # if-statement is faster than branchless
        if self == Direction.RIGHT:
            return 1
        elif self == Direction.LEFT:
            return -1
        else:
            return 0

    def get_dy(self) -> int:
        # if-statement is faster than branchless
        if self == Direction.UP:
            return 1
        elif self == Direction.DOWN:
            return -1
        else:
            return 0

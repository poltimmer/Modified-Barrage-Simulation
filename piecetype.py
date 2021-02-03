from enum import Enum

class PieceType(Enum):
    FLAG = 0
    BOMB = 1
    SPY = 2
    SCOUT = 3
    MINER = 4
    GENERAL = 5
    MARSHALL = 6

    def can_move(self) -> bool:
        if (self == FLAG or self == BOMB):
            return False
        else:
            return True
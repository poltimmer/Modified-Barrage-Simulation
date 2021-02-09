from __future__ import annotations
from enum import Enum
from typing import Optional


class Player(Enum):
    RED = 0
    BLUE = 1

    def opposite(self):
        if self == Player.RED:
            return Player.BLUE
        else:
            return Player.RED

    @staticmethod
    def get_from_character(character: str) -> Optional[Player]:
        if character == 'R':
            return Player.RED
        elif character == 'B':
            return Player.BLUE
        else:
            return None

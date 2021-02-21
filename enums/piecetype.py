from __future__ import annotations
from typing import Optional
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
        return self != PieceType.FLAG and self != PieceType.BOMB

    def get_survivor_if_hits(self, opponent: PieceType) -> Optional[PieceType]:
        """
        Determine the piecetype that survives when a piece of this type hits another piece, or none if neither survive
        """
        both = [self, opponent]
        if PieceType.FLAG in both:
            return PieceType.FLAG
        elif PieceType.BOMB in both:
            return PieceType.MINER if PieceType.MINER in both else PieceType.BOMB
        elif self == opponent:
            return None
        elif PieceType.MARSHALL in both:
            return PieceType.SPY if self == PieceType.SPY else PieceType.MARSHALL
        elif PieceType.GENERAL in both:
            return PieceType.GENERAL
        elif PieceType.MINER in both:
            return PieceType.MINER
        elif PieceType.SCOUT in both:
            return PieceType.SCOUT
        else:
            raise Exception("Can't determine winner of " + str(self) + " and " + str(opponent) + ".")

    @staticmethod
    def get_from_character(character: str) -> PieceType:
        if character == 'F':
            return PieceType.FLAG
        elif character == '3':
            return PieceType.MINER
        elif character == 'B':
            return PieceType.BOMB
        elif character == '2':
            return PieceType.SCOUT
        elif character == '10':
            return PieceType.MARSHALL
        elif character == '9':
            return PieceType.GENERAL
        elif character == '1':
            return PieceType.SPY
        else:
            raise Exception("Invalid typechar: " + character)

    def __str__(self):
        return self._name_

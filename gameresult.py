from typing import Optional

from enums.player import Player


class GameResult:
    def __init__(self, winner: Optional[Player], steps: int, both_spies_alive: bool):
        self.winner = winner
        self.steps = steps
        self.both_spies_alive = both_spies_alive

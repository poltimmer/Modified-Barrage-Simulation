from board import Board
from move import Move

class Game:
    def __init__(self, board: Board, nextToMove: Player):
        self.board = board
        self.nextToMove = nextToMove

    def do_move(self, move: Move) -> None:
        pass
        # Perform the move
        # Switch which player is next

    def get_winner(self) -> Optional[Player]:
        pass

    def play_game(self) -> Optional[Player]:
        # Play until someone won (or draw)
        # Somehow record some statistics like first move
        pass
        
import piece
from enums.player import Player

Piece = lambda: piece.Piece


class Move:
    def __init__(self, piece: Piece, new_pos_x: int, new_pos_y: int):
        self.piece = piece
        self.new_pos_x = new_pos_x
        self.new_pos_y = new_pos_y

    def __str__(self):
        return f"Move: {'R' if self.piece.player == Player.RED else 'B'}.{str(self.piece.piece_type)[:3]} " \
               f"from ({self.piece.x}, {self.piece.y}) " \
               f"to ({self.new_pos_x}, {self.new_pos_y})."

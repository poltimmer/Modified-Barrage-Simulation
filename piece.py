from piecetype import PieceType
from board import Board
from direction import Direction
from player import Player
from move import Move

class Piece:
    def __init__(self, board: Board, player: Player, piece_type: PieceType, x: int, y: int):
        self.board = board
        self.player = player
        self.piece_type = piece_type
        self.x = x
        self.y = y

    def get_available_moves(self) -> [Move]:
        """
        Return an array of all moves that can be done, taking into account
        - Its ability to move
        - Not moving out of bounds
        - Not moving into a piece of the same player
        """
        if not self.piece_type.can_move():
            return []
        else:
            directions = [Direction.UP, Direction.DOWN]
            if self.player == Player.RED:
                directions.append(Direction.RIGHT)
            else:
                directions.append(Direction.LEFT)
            moves = []
            for direction in directions:
                new_x = self.x + direction.get_dx()
                new_y = self.y + direction.get_dy()
                if new_x >= 0 and new_x < self.board.width and new_y >= 0 and new_y < self.board.height:
                    piece_on_new_pos = self.board.get_piece_on_square(new_x, new_y)
                    if (piece_on_new_pos is None or piece_on_new_pos.player is not self.player):
                        moves.append(Move(self, new_x, new_y))
            return moves


    def get_surviving_piece_if_hits(self, piece: Piece) -> Piece:
        """
        Determine the piece that survives when this piece hits another piece, or none if neither survive
        """
        pass

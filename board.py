from piece import Piece
from player import Player
from move import Move

class Board:
    def __init__(self, width: int = 6, height: int = 4):
        self.width = width
        self.height = height
        self.positions: [[Optional[Piece]]] = [[0,0,0]]
        pass

    def get_player_moves(self, player: Player) -> [Move]:
        moves: [Move] = []

        for row in self.positions:
            for piece in row:
                for move in piece.get_available_moves():
                    moves.append(move)
        return moves

    def get_piece_on_square(self, x: int, y: int) -> Optional[Piece]:
        '''
        Returns Piece at position (x,y)
        '''
        return self.positions[x][y]

    def set_piece(self, piece: Piece, x: int, y: int) -> None:
        pass




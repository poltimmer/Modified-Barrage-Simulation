from typing import Optional

from enums.player import Player
from enums.piecetype import PieceType
import piece
import move

Piece = lambda: piece.Piece
Move = lambda: move.Move


class Board:
    def __init__(self, positions: list):
        self.width = len(positions)
        self.height = len(positions[0])
        self.positions = positions
        self.pieces = [set()] * 2

        # Construct the pieces sets and fill their board variable
        for column in positions:
            for piece in column:
                if piece:
                    piece.board = self
                    self.pieces[piece.player.value].add(piece)

    def get_player_moves(self, player: Player) -> [Move]:
        moves: [Move] = []

        for piece in self.pieces[player.value]:
            moves += piece.get_available_moves()
        return moves

    def get_piece(self, x: int, y: int) -> Optional[Piece]:
        '''
        Returns Piece at position (x,y)
        '''
        return self.positions[x][y]

    def set_piece(self, piece: Piece, x: int, y: int) -> bool:
        """
        Update the board for the action where piece moves to (x, y).
        Returns whether a flag has been found
        """
        self.positions[piece.x][piece.y] = None
        opponent = self.positions[x][y]

        if opponent is None:
            # Safely advance
            piece.x = x
            piece.y = y
            self.positions[x][y] = piece
        else:
            # There is an opponent, determine survivors
            winning_type = piece.piece_type.get_survivor_if_hits(opponent.piece_type)
            piece_survives = piece.piece_type == winning_type
            opponent_survives = opponent.piece_type == winning_type

            if not opponent_survives:
                # Remove opponent from the game
                opponent.x = None
                opponent.y = None
                self.positions[x][y] = None
                self.pieces[opponent.player.value].remove(opponent)

            if not piece_survives:
                # Remove the moved piece from the game
                piece.x = None
                piece.y = None
                self.pieces[piece.player.value].remove(piece)
            else:
                # Advance the moved piece
                piece.x = x
                piece.y = y
                self.positions[x][y] = piece

        # Return whether a flag was captured
        return opponent is not None and opponent.piece_type == PieceType.FLAG

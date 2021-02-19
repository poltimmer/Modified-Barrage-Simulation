from copy import deepcopy
from typing import Optional

from tqdm.contrib.concurrent import process_map

import move
import piece
from board import Board
from enums.piecetype import PieceType
from enums.player import Player
from game import Game
from gameresult import GameResult

Move = lambda: move.Move
Piece = lambda *args: piece.Piece(*args)


class Simulator:
    def __init__(self):
        pass

    @staticmethod
    def play_game(positions: [[Optional[Piece]]]) -> GameResult:
        """
        Play one game and extract the results
        """
        # Play a game
        board = Board(deepcopy(positions))
        game = Game(board, next_to_move=Player.RED)
        game.play_game()

        # Extract interesting results
        winner = game.get_winner()
        steps = game.steps
        spies_alive = 0
        for pieces in board.pieces:
            for piece in pieces:
                if piece.piece_type == PieceType.SPY:
                    spies_alive += 1
        both_spies_alive = spies_alive == 2
        return GameResult(winner, steps, both_spies_alive)

    @staticmethod
    def get_positions_from_file(path: str) -> [[Optional[Piece]]]:
        """
        Returns 2d array of pieces read in from file 'path'
        """
        positions = [[None] * 4 for _ in range(6)]

        f = open(path, "r")
        for y, line in enumerate(f):
            pieces = line.rstrip("\n").split(" ")
            for x, piece_chars in enumerate(pieces):
                color = piece_chars[:1]
                piece_chars = piece_chars[1:]

                # Detemine player
                player = Player.get_from_character(color)

                # If no player was set, no piece is present.
                if player:
                    piece_type = PieceType.get_from_character(piece_chars)
                    # print(board, player, piece_type, j, i)
                    piece = Piece(player, piece_type, x, y)
                    positions[x][y] = piece
        return positions

    @staticmethod
    def play_games(num_games: int, positions: [[Optional[Piece]]], multithreaded: bool = True) -> [GameResult]:
        if multithreaded:
            positions_list = [positions] * num_games
            return process_map(Simulator.play_game, positions_list, chunksize=100)
        else:
            results = []
            sim: Simulator = Simulator()
            for _ in range(num_games):
                result = sim.play_game(positions)
                results.append(result)
            return results

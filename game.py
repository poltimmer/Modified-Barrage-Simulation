import pprint
import random

from typing import Optional
from enums.player import Player
from board import Board
import move

Move = lambda: move.Move


class Game:
    def __init__(self, board: Board, next_to_move: Player):
        self.board = board
        self.next_to_move = next_to_move
        self.winner = None
        self.done = False
        self.steps = 0

    def do_move(self, move: Move) -> None:
        """
        Execute a move and switch who may move next
        """
        self.steps += 1
        done = self.board.set_piece(move.piece, move.new_pos_x, move.new_pos_y)
        if done:
            self.winner = self.next_to_move
            self.done = True
        else:
            self.next_to_move = self.next_to_move.opposite()

    def get_winner(self) -> Optional[Player]:
        return self.winner

    def play_game(self, step_by_step=False) -> Optional[Player]:
        """
        Play the game until the end by making random moves
        """
        while not self.done:
            # Determine all possible moves
            available_moves: [Move] = self.board.get_player_moves(self.next_to_move)
            if step_by_step:
                print("=" * 5, "Step information", "=" * 5)
                print("- Available moves:")
                pprint.pprint([str(move) for move in available_moves])

            # Catch end conditions where one or both have no moves available
            if len(available_moves) == 0:
                if len(self.board.get_player_moves(self.next_to_move.opposite())) == 0:
                    # Both can't make any moves anymore
                    self.winner = None
                else:
                    # Only the current player can't move anymore
                    self.winner = self.next_to_move.opposite()
                self.done = True
                return self.winner
            else:
                # Make a random move out of all available moves
                move = random.choice(available_moves)
                self.do_move(move)

                if step_by_step:
                    print("= Played", move)
                    print("= Result:")
                    print(self.board)
                    input("Press enter to continue\n")

from enums.piecetype import PieceType
from enums.player import Player
from simulator import Simulator
from itertools import permutations
from pprint import pprint
from piece import Piece
import math


def print_results(results, n):
     # Inspect winner results
    n_red = len([result for result in results if result.winner == Player.RED])
    n_blue = len([result for result in results if result.winner == Player.BLUE])
    n_draw = len([result for result in results if result.winner is None])
    print(f"Winners: Red {n_red}, Blue {n_blue}, Draw: {n_draw}")

    # Inspect average number of moves
    steps_avg = sum([result.steps for result in results]) / n
    print(f"Average #steps: {steps_avg}")

    # Inspect whether both spies stayed alive
    n_spies_alive = len([result for result in results if result.both_spies_alive])
    n_spies_not_alive = len([result for result in results if not result.both_spies_alive])
    print(f"Both spies alive: Yes {n_spies_alive}, No {n_spies_not_alive}")

def q1():
    sim = Simulator()
    n = 38415  # TODO Determine how many games to play
    n = 100  # TODO Determine how many games to play

    # Use default starting positions
    positions = sim.get_positions_from_file('./input.txt')

    # Play the games
    results = sim.play_games(n, positions)
    print_results(results, n)


def q3():
    sim = Simulator()
    positions = sim.get_positions_from_file('./input.txt')
    options = [PieceType.MARSHALL, PieceType.GENERAL, PieceType.MINER, PieceType.SCOUT, PieceType.SCOUT, PieceType.SPY, PieceType.BOMB]
    piece_permutations = list(set(permutations(options)))
    for permutation in piece_permutations[:1]: # limited to first permutation
        for flagpos in range(4):
            permcopy = list(permutation)
            permcopy.insert(flagpos, PieceType.FLAG)
            # piece_list.append(permcopy)
            finalpos = list(positions)
            piecelist = [Piece(player=Player.RED, piece_type=piecetype, x=int(math.floor(i/4)), y=i%4) for (i, piecetype) in enumerate(permcopy)]
            # pprint([(piece.x, piece.y, piece.piece_type) for piece in piecelist])
            finalpos[0] = piecelist[:4]
            finalpos[1] = piecelist[4:]
            # pprint([[piece for piece in row] for row in finalpos])
            results = sim.play_games(100, finalpos)
            print_results(results, 100)




    # TODO Condition on whether Red wins and whether Blue wins


if __name__ == "__main__":
    q3()

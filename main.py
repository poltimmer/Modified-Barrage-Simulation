import functools
import math
import time
from copy import deepcopy
from itertools import permutations
from pprint import pprint
from statistics import mean

from tqdm import tqdm
from tqdm.contrib.concurrent import process_map, cpu_count

from board import Board
from enums.piecetype import PieceType
from enums.player import Player
from gameresult import GameResult
from move import Move
from piece import Piece
from simulator import Simulator


def print_results(results):
    print("===== Results =====")

    # Inspect winner results
    n_red = len([result for result in results if result.winner == Player.RED])
    n_blue = len([result for result in results if result.winner == Player.BLUE])
    n_draw = len([result for result in results if result.winner is None])
    print(f"Winners: Red {n_red}, Blue {n_blue}, Draw: {n_draw}")

    # Inspect average number of moves
    steps_avg = mean([result.steps for result in results])
    print(f"Average #steps: {steps_avg}")

    # Inspect whether both spies stayed alive
    n_spies_alive = len([result for result in results if result.both_spies_alive])
    n_spies_not_alive = len([result for result in results if not result.both_spies_alive])
    print(f"Both spies alive: Yes {n_spies_alive}, No {n_spies_not_alive}")


def q1():
    n = 38416

    # Use default starting positions
    positions = Simulator.get_positions_from_file('./input.txt')

    # Play the games
    time_start = time.time()
    results = Simulator.play_games(n, positions, multithreaded=False, step_by_step=False)
    time_end = time.time()
    print("Done running", n, "simulations. That took", time_end - time_start, "seconds.")

    # General results
    print_results(results)

    # Results where Red wins
    print_results([result for result in results if result.winner == Player.RED])

    # Results where Blue wins
    print_results([result for result in results if result.winner == Player.BLUE])

    # Results where neither wins (not asked by Q1 but still interesting)
    print_results([result for result in results if result.winner is None])


def q2():
    n = 38415

    # Use default starting positions
    positions = Simulator.get_positions_from_file('./input.txt')

    # Determine available moves for red
    board: Board = Board(positions)
    red_moves: [Move] = board.get_player_moves(Player.RED)

    # Determine win rate of each first move
    print(f"Determining win rates of each of the {len(red_moves)} first possible moves of RED.")
    win_rates = []
    for red_move in red_moves:
        # Calculate the board position after RED's first move
        # To do this, a new board is generated, and the same position's piece instance is found on this new board
        board: Board = Board(deepcopy(positions))
        piece: Piece = board.get_piece(red_move.piece.x, red_move.piece.y)
        board.set_piece(piece, red_move.new_pos_x, red_move.new_pos_y)
        positions_after_move = board.positions

        # Play n games from this position where BLUE is next to play
        results = Simulator.play_games(n, positions_after_move, start_player=Player.BLUE)

        # Determine the win rate of RED
        win_rate = mean([(result.winner == Player.RED) for result in results])
        win_rates.append(win_rate)

    for red_move, win_rate in zip(red_moves, win_rates):
        print("==== Available move ====")
        print(f"Piece player: {red_move.piece.player}")
        print(f"Piece type: {red_move.piece.piece_type}")
        print(f"From: ({red_move.piece.x}, {red_move.piece.y})")
        print(f"To: ({red_move.new_pos_x}, {red_move.new_pos_y})")
        print(f"Winrate: {win_rate} ({win_rate * 100})%")


def get_positions_from_permutation(perm, pos_orig):
    positions = list(pos_orig)
    piecelist = [Piece(player=Player.RED, piece_type=piecetype, x=int(math.floor(i / 4)), y=i % 4) for (i, piecetype) in
                 enumerate(perm)]
    positions[0] = piecelist[:4]
    positions[1] = piecelist[4:]
    return positions


def q3():
    # Prepare permutations of staring positions
    positions_original = Simulator.get_positions_from_file('./input.txt')
    options = [PieceType.MARSHALL, PieceType.GENERAL, PieceType.MINER, PieceType.SCOUT, PieceType.SCOUT, PieceType.SPY,
               PieceType.BOMB]
    piece_permutations = [list(permutation) for permutation in set(permutations(options)) for _ in range(4)]
    piece_permutations = [permutation.insert(i % 4, PieceType.FLAG) or permutation for i, permutation in
                          enumerate(piece_permutations)]
    positions = [get_positions_from_permutation(permutation, positions_original) for permutation in piece_permutations]

    # Run runs reducing the size of the position set each time
    runs = [
        # Reduce to this many positions | Run this many of each position
        [1000, 100],
        [100, 1000],
        [10, 10000],
        [1, 38415]
    ]
    time_start = time.time()
    for run in runs:
        reduce_to = run[0]
        n_runs_per_perm = run[1]
        print("Reducing", len(positions), "positions to", reduce_to,
              "positions by running", n_runs_per_perm, "of each.")
        results2d = q3_run_permutations(positions, n_runs_per_perm)
        red_winrates = [mean([(result.winner == Player.RED) for result in results]) for results in results2d]
        sorted_winrates = sorted(zip(positions, red_winrates), key=lambda entry: entry[1], reverse=True)
        positions = [pos[0] for pos in sorted_winrates[:reduce_to]]
    time_end = time.time()

    top_position = positions[0]
    print("Top position:")
    pprint(top_position)
    pprint([[piece.piece_type if hasattr(piece, 'piece_type') else None for piece in row] for row in top_position])

    print("Calculation took", time_end - time_start, "seconds.")

    results_final = Simulator.play_games(38415, top_position)

    print_results(results_final)
    print(mean([(result.winner == Player.RED) for result in results_final]))

    # TODO Condition on whether Red wins and whether Blue wins


def q3_run_permutations(positions, n_runs_per_position, multithreaded=True) -> [[GameResult]]:
    # True iff multithreading is applied separately per position/permutation (so in the simulator)
    multithread_sim = multithreaded and len(positions) < 20

    if multithreaded and not multithread_sim:
        partial_func = functools.partial(Simulator.play_games, n_runs_per_position, multithreaded=multithread_sim)
        return process_map(partial_func, positions, chunksize=1, max_workers=cpu_count() - 1)
    else:
        results2d: [[GameResult]] = []
        for position in tqdm(positions):
            results2d.append(Simulator.play_games(n_runs_per_position, position, multithreaded=multithread_sim))
        return results2d


def get_variance(mean, samples):
    return sum([(sample - mean) ** 2 for sample in samples]) / (len(samples) - 1)


if __name__ == "__main__":
    q1()

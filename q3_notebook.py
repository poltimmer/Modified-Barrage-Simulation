# %%
from enums.piecetype import PieceType
from enums.player import Player
from simulator import Simulator
from itertools import permutations
from pprint import pprint
from piece import Piece
from gameresult import GameResult
import math
from statistics import mean
from tqdm.notebook import tqdm
from tqdm.contrib.concurrent import process_map
from main import get_positions_from_permutation
from multiprocessing import Pool
from functools import partial
from p_tqdm import p_map

# %%
sim = Simulator()
n_runs_all = 50
n_runs_1k = 500
n_runs_100 = 5000
n_runs_10 = 38415


positions_original = sim.get_positions_from_file('./input.txt')
options = [PieceType.MARSHALL, PieceType.GENERAL, PieceType.MINER, PieceType.SCOUT, PieceType.SCOUT, PieceType.SPY, PieceType.BOMB]
piece_permutations = [list(permutation) for permutation in set(permutations(options)) for _ in range(4)]
piece_permutations = [permutation.insert(i%4, PieceType.FLAG) or permutation for i, permutation in enumerate(piece_permutations)]

# %%
def get_top_permutations(permutation_list, n_runs, top_amount):
    positions_list = [get_positions_from_permutation(permutation, positions_original) for permutation in piece_permutations]
    play_games_partial = partial(Simulator.play_games, n_runs)

    results_list = p_map(play_games_partial, positions_list)
    red_winrates = [mean([(result.winner == Player.RED) for result in results]) for results in results_list]
    sorted_winrates = sorted(zip(permutation_list, red_winrates), key=lambda entry: entry[1], reverse=True)
    top_results = sorted_winrates[:top_amount]
    top_perms = [entry[0] for entry in top_results]
    return top_perms

# %%
top_1k = get_top_permutations(piece_permutations, 50, 1000)

# %%
results_list = []
for permutation in tqdm(piece_permutations): # limited to first few permutations
    positions = get_positions_from_permutation(permutation, positions_original)
    results_list.append(sim.play_games(n_runs_all, positions))

red_winrates = [mean([(result.winner == Player.RED) for result in results]) for results in results_list]
sorted_winrates = sorted(zip(piece_permutations, red_winrates), key=lambda entry: entry[1], reverse=True)
top_1k = sorted_winrates[:1000]
top_1k_perms = [entry[0] for entry in top_1k]

# %%
results_list_1k = []
for permutation in tqdm(top_1k_perms):
    positions = get_positions_from_permutation(permutation, positions_original)
    results_list_1k.append(sim.play_games(n_runs_1k, positions))

red_winrates = [mean([(result.winner == Player.RED) for result in results]) for results in results_list]
sorted_winrates = sorted(zip(piece_permutations, red_winrates), key=lambda entry: entry[1], reverse=True)
top_100 = sorted_winrates[:100]
top_100_perms = [entry[0] for entry in top_100]

# %%
results_list_100 = []
for permutation in tqdm(top_100_perms):
    positions = get_positions_from_permutation(permutation, positions_original)
    results_list_100.append(sim.play_games(n_runs_100, positions))

red_winrates = [mean([(result.winner == Player.RED) for result in results]) for results in results_list]
sorted_winrates = sorted(zip(piece_permutations, red_winrates), key=lambda entry: entry[1], reverse=True)
top_10 = sorted_winrates[:10]

pprint(top_10)
# %%
best_perm = top_10[0][0]
positions = get_positions_from_permutation(best_perm, positions_original)
final_stats = sim.play_games(38415, positions)
print(mean([(result.winner == Player.RED) for result in final_stats]))
# %%

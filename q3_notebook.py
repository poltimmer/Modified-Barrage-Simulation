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
from main import get_positions_from_permutation

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
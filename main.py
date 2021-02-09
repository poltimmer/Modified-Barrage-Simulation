from enums.player import Player
from simulator import Simulator


def q1():
    sim = Simulator()
    n = 1000  # TODO Determine how many games to play

    # Use default starting positions
    positions = sim.get_positions_from_file('./input.txt')

    # Play the games
    results = sim.play_games(n, positions)

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

    # TODO Condition on whether Red wins and whether Blue wins


if __name__ == "__main__":
    q1()

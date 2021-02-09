from simulator import Simulator

if __name__ == "__main__":
    sim = Simulator()

    positions = sim.get_positions_from_file('./input.txt')
    sim.start(positions)

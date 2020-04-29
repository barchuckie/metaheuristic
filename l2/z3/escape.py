"""L2/Z3.

Find the shortest path to an exit in a maze using Simulated Annealing.
Author: Patryk Barczak
"""
from enums import *
from maze import *
from simulated_annealing import *
import sys


def print_path(path, file=sys.stderr):
    """Print path in a proper format."""
    print(''.join(map(lambda f: f.move.__name__, path)), file=file)


def main():
    """Perform simulated annealing on a maze from the input data."""
    i = input().split()
    time_limit = int(i[0])
    n = int(i[1])
    m = int(i[2])

    grid = []
    start_field = -1
    exit_field = -1
    for i in range(n):
        row = list(map(lambda u: Field(int(u)), input().replace('\r', '')))
        if Field.AGENT in row:
            start_field = (i, row.index(Field.AGENT))
        if Field.EXIT in row:
            exit_field = (i, row.index(Field.EXIT))
        grid.append(row)

    maze = Maze(grid, start_field, exit_field)
    sim_annealing = SimulatedAnnealing(maze)
    path = sim_annealing.run(time_limit)

    print(maze.cost(path))
    print_path(path)


if __name__ == '__main__':
    main()

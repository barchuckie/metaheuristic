"""L3/Z3.

Find the shortest path to an exit in a maze using Genetic Algorithm.

Author: Patryk Barczak
"""
import sys

from enums import *
from maze import Maze
from genetic import GeneticAlgorithm


def print_path(path, file=sys.stderr):
    """Print path in a proper format."""
    print(''.join(map(lambda f: f.move.__name__, path)), file=file)


def path_from_string(str_path):
    """Create and return a path from string.

    Path is a list of Directions."""
    return list(map(path_map, str_path))


def path_map(s):
    """Map char 's' to the Direction."""
    for d in Directions:
        if s == d.move.__name__:
            return d


def escape():
    """Perform genetic algorithm on a maze from the input data."""
    i = list(map(int, input().split()))
    time_limit = i[0]
    n = i[1]
    m = i[2]
    initial_size = i[3]
    population_size = i[4]

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

    initial_paths = []
    for i in range(initial_size):
        initial_paths.append(path_from_string(input().replace('\r', '')))

    genetic = GeneticAlgorithm(maze, population_size)
    unchanged_iterations = 10*(n*m)
    result = genetic.search(time_limit, initial_paths, unchanged_iterations)

    print(result[1])
    print_path(result[0])


if __name__ == '__main__':
    escape()

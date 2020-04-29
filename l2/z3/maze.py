"""Maze implementation."""
import random
from enums import *


class WallException(Exception):
    """Wall exception raised when agent walks into maze wall."""
    def __init__(self):
        """Initialize new instance of exception with proper value."""
        self.value = 'Path goes through a wall'

    def __str__(self):
        return repr(self.value)


def reduce_path(path):
    """Reduce path by removing walking in the opposite directions."""
    i = 0
    while i < len(path)-1:
        while i + 2 < len(path) and path[i] == path[i+1]:
            i += 1
        while i > 0 and i + 2 < len(path) and path[i] == opposite_dir(path[i+1]):
            del path[i+1]
            del path[i]
            i -= 1
        i += 1
    return path


class Maze:
    """Maze escape solver with Simulated Annealing algorithm."""

    def __init__(self, grid, start, exit):
        """Initialize maze with the grid and positions of start and exit"""
        self.grid = grid
        self.start = start
        self.exit = exit

    def get_point(self, i, j):
        """Get field type on the (i,j)"""
        return self.grid[i][j]

    def cost(self, path):
        """Calculate cost of the path"""
        if path is None or self.get_point(*self.walk(path)[0]) != Field.EXIT:
            return float('inf')
        return len(path)

    def walk(self, path):
        """Walk the path from the start point"""
        point = self.start
        walked = []
        for move in path:
            point = move.move(point)
            if self.get_point(*point) == Field.WALL:
                raise WallException
            walked.append(move)
            if self.get_point(*point) == Field.EXIT:
                break
        return point, walked

    def can_exit(self, point):
        """Check if exit is next to a point"""
        for move in Directions:
            if self.get_point(*move.move(point)) == Field.EXIT:
                return move
        return None

    def create_first(self):
        """Create first correct path to exit.

        Path is found by walking in random direction until agent meets wall or randomly (with 5% chance) turns."""
        point = self.start
        path = []
        direction = random.choice(list(Directions))
        while self.can_exit(point) is None:
            if self.get_point(*direction.move(point)) == Field.WALL or random.random() < 0.05:
                direction = turn(direction)
            else:
                path.append(direction)
                point = direction.move(point)
        path.append(self.can_exit(point))
        reduce_path(path)
        return path

    def get_random_neighbor(self, path):
        """Calculate a random neighbor of the path"""
        if len(path) < 3:
            return None
        first_seq_start = random.randrange(len(path)-2)
        first_seq_end = random.randrange(first_seq_start+1, len(path)-1)
        second_seq_start = random.randrange(first_seq_end, len(path)-1)
        second_seq_end = random.randrange(second_seq_start+1, len(path))
        new_path = path[:first_seq_start] + path[second_seq_start:second_seq_end] + path[first_seq_start:first_seq_end] + path[second_seq_end:]
        reduce_path(new_path)
        try:
            res = self.walk(new_path)
            if self.get_point(*res[0]) == Field.EXIT:
                return res[1]
        except WallException:
            pass

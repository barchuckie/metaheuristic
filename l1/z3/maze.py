from time import time
import random
import sys
from enums import *


class WallException(Exception):
   def __init__(self):
      self.value = 'Path goes through a wall'
   def __str__(self):
      return(repr(self.value))


def print_path(path, file=sys.stderr):
    '''Print path in a proper format'''
    print(''.join(map(lambda f: f.move.__name__, path)), file=file)


def reduce_path(path):
    '''Reduce path by removing walking in the opposite directions'''
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
    '''Maze escape solver with Tabu Search'''

    def __init__(self, grid, start, exit):
        '''Initialize maze with the grid and positions of start and exit'''
        self.grid = grid
        self.start = start
        self.exit = exit


    def getpoint(self, i, j):
        '''Get field type on the (i,j)'''
        return self.grid[i][j]


    def cost(self, path):
        '''Calculate cost of the path'''
        if path is None or self.getpoint(*self.walk(path)) != Field.EXIT:
            return float('inf')
        return len(path)


    def walk(self, path):
        '''Walk the path from the start point'''
        point = self.start
        for move in path:
            point = move.move(point)
            if self.getpoint(*point) == Field.WALL:
                raise WallException
        return point


    def can_exit(self, point):
        '''Check if exit is next to a point'''
        for move in Directions:
            if self.getpoint(*move.move(point)) == Field.EXIT:
                return move
        return None


    def createfirst(self):
        '''Create first correct path to exit by walking by the wall'''
        point = self.start
        path = []
        direction = random.choice(list(Directions))
        while self.can_exit(point) == None:
            if self.getpoint(*direction.move(point)) != Field.WALL:
                path.append(direction)
                point = direction.move(point)
            else:
                direction = turn(direction)
        path.append(self.can_exit(point))
        reduce_path(path)
        return path


    def tabusearch(self, t, tabu_limit, unchanged_limit = 1):
        '''Run Tabu Search for maze escape
        t -- max time to run
        tabu_limit -- max number of elements in tabu list
        unchanged_limit -- number of trials to stop when result is unchanged'''
        endtime = time() + t
        n = len(self.grid)
        best = self.createfirst()
        tabu_list = []
        unchanged = 0

        while time() <= endtime:
            while len(tabu_list) > tabu_limit:
                tabu_list.pop(0)
            neighborhood = self.getneighbors(best)
            best_candidate = None
            for candidate in neighborhood:
                if candidate not in tabu_list:
                    if self.cost(candidate) < self.cost(best_candidate):
                        best_candidate = candidate.copy()
                        tabu_list.append(best_candidate)
            if self.cost(best_candidate) < self.cost(best):
                best = best_candidate.copy()
                unchanged = 0
            else:
                unchanged += 1
            if unchanged > unchanged_limit:
                break

        print(self.cost(best))
        print_path(best)


    def getneighbors(self, path):
        '''Calculate neighbors of the path'''
        neighborhood = []
        i = 0
        while i < len(path) - 1:
            start_first = i
            while i + 2 < len(path) and path[i] == path[i+1]:
                i += 1
            i += 1
            start_second = i
            while i + 2 < len(path) and path[i] == path[i+1]:
                i += 1
            end_second = i + 1
            if i + 1 >= len(path):
                break
            new_path = path[:start_first] + path[start_second:end_second] + path[start_first:start_second] + path[end_second:]
            reduce_path(new_path)
            try:
                if self.getpoint(*self.walk(new_path)) == Field.EXIT:
                    neighborhood.append(new_path)
            except WallException as e:
                pass
            i = start_second

        return neighborhood

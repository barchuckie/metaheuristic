import random
import sys
from time import time

def swap(route, i, j):
    '''Swap elements between i-th and j-th place'''
    if i >= len(route) or j >= len(route):
        return None
    mod_route = route.copy()
    x = mod_route[i]
    mod_route[i] = mod_route[j]
    mod_route[j] = x
    return mod_route

def inverse(route, i, j):
    '''Inverse a subseries from i to j'''
    if i >= len(route) or j >= len(route):
        return None
    slice = route[i:j]
    slice.reverse()
    mod_route = route[:i] + slice + route[j:]
    return mod_route

class TSP:
    '''Travelling Salesman Problem solver with Tabu Search'''
    def __init__(self, grid):
        '''Initialize with grid of distances between cities'''
        self.grid = grid

    def cost(self, route):
        '''Calculate cost of the route'''
        if route is None:
            return float('inf')

        cost = 0
        for i in range(len(route)-1):
            cost += self.grid[route[i]][route[i+1]]
        return cost


    def createfirst(self):
        '''Create first instance of the route. Use greedy method.'''
        result = [0]
        tmp_grid = self.grid
        for i in range(len(tmp_grid)-1):
            city = result[i]
            distances = tmp_grid[city]
            min = float('inf')
            min_idx = None
            for j in range(1, len(distances)):
                if j not in result and distances[j] < min:
                    min = distances[j]
                    min_idx = j
            next_city = min_idx
            result.append(next_city)
        result.append(0)
        return result


    def tabusearch(self, t, tabu_limit):
        '''Run Tabu Search for TSP instance'''
        endtime = time() + t
        n = len(self.grid)
        best = self.createfirst()
        tabu_list = [best]
        unchanged = 0
        very_best = best

        while time() <= endtime:
            if unchanged > 100:
                unchanged = 0
                best = [0] + random.sample(range(1,n), n-1) + [0]
                neighborhood = self.getneighbors(best)
            elif unchanged > 0:
                neighborhood = self.getneighbors_inv(best)
            else:
                neighborhood = self.getneighbors(best)
            best_candidate = None
            for candidate in neighborhood:
                if candidate not in tabu_list and self.cost(candidate) < self.cost(best_candidate):
                    best_candidate = candidate.copy()
            if best_candidate is None:
                tabu_list.pop(0)
            else:
                tabu_list.append(best_candidate)

            if self.cost(best_candidate) < self.cost(best):
                best = best_candidate.copy()
                unchanged = 0
            else:
                unchanged += 1
            if self.cost(best) < self.cost(very_best):
                very_best = best

        print(self.cost(very_best))
        print(' '.join(list(map(lambda u: str(u+1), very_best))), file=sys.stderr)


    def getneighbors(self, route):
        '''Calculate neighbors of the route'''
        neighborhood = []
        for i in range(1, len(route)-2):
            for j in range(i+1, len(route)-1):
                neighborhood.append(swap(route, i, j))
        return neighborhood

    def getneighbors_inv(self, route):
        '''Calculate neighbors of the route'''
        neighborhood = []
        for i in range(1, len(route)-3):
            for j in range(i+3, len(route)-1):
                neighborhood.append(inverse(route, i, j))
        return neighborhood

def main():
    '''Main function of the package'''
    i = input().split()
    t = int(i[0])
    n = int(i[1])

    grid = []
    for i in range(n):
        grid.append(list(map(int, input().split())))

    tsp = TSP(grid)
    tsp.tabusearch(t, n)


if __name__ == '__main__':
    main()

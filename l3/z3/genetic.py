"""Genetic algorithm.

Implementation of genetic algorithm for finding the shortest path to escape from a maze.
"""
import time
import random


class GeneticAlgorithm:
    """Class implementation of genetic algorithm."""

    def __init__(self, maze, population_size):
        """Create new instance which consist of matcher and population size.

        - maze -- object of the maze to escape from
        - population_size -- maximum possible size of the population
        """
        self.maze = maze
        self.population_size = population_size

    def cost_function(self, element):
        """Cost function to optimize (find its minimum)."""
        return self.maze.cost(element)

    def get_best(self, population):
        """Return the best element from the current population."""
        best = min(population, key=self.cost_function)
        return best, self.cost_function(best)

    def get_global_best(self, b1, b2):
        """Return the better element which is global best.

        Compare two elements between each other and return the better one.
        If they are equal, return b1.
        """
        if b2[1] < b1[1]:
            return b2
        return b1

    def select_parents(self, population):
        """Select parents for reproduction from the population.

        - population -- population to chose parents from
        """
        random.shuffle(population)
        return population

    def crossover(self, parent1, parent2):
        """Crossover parents and return their child.

        - parent1, parent2 -- parents to crossover
        - crossover_prob -- probability of crossover
        """
        return self.maze.get_crossover_path(parent1, parent2)

    def mutation(self, element):
        """Return mutated element."""
        mutation = self.maze.get_random_neighbor(element)
        return mutation if mutation is not None else element

    def reproduce(self, parents):
        """Reproduce parents.

        - parents -- set of parents to be chosen for reproduction
        - crossover_prob -- probability of crossover between two parents
        """
        children = []
        for i, parent in enumerate(parents):
            if i == len(parents)-1:
                parent2 = parents[0]
            else:
                parent2 = parents[i+1] if i % 2 == 0 else parents[i-1]
            child = self.crossover(parent, parent2)
            child = self.mutation(child)
            children.append(child)
        return children

    def search(self, time_limit, initial_population, max_unchanged_it):
        """Search for the shortest path.

        Search by optimization of the objective function (minimising cost function)
        using genetic algorithm.
        """
        population = []
        for e in initial_population:
            w = self.maze.walk(e)[1]
            population.append(w)
        end_time = time.time() + time_limit
        best = self.get_best(population)
        it = 0

        while time.time() < end_time:
            parents = self.select_parents(population)
            children = self.reproduce(parents)
            population = children
            current_best = best
            best = self.get_global_best(best, self.get_best(population))
            if current_best == best:
                it += 1
                if it >= max_unchanged_it:
                    break
            else:
                it = 0

        return best

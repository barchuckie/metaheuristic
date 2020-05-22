"""Genetic algorithm.

Implementation of genetic algorithm for finding best matching word.
"""
import time
import random


CROSSOVER_PROB = 0.98
POPULATION_SIZE = 10


class GeneticAlgorithm:
    """Class implementation of genetic algorithm."""

    def __init__(self, matcher, population_size=POPULATION_SIZE):
        """Create new instance which consist of matcher and population size.

        - matcher -- object to calculate fitness and manipulate words
        - population_size -- maximum possible size of the population
        """
        self.matcher = matcher
        self.population_size = population_size

    def objective_function(self, element):
        """Objective function to optimize (find its maximum)."""
        return self.matcher.fitness(element)

    def get_population_best(self, population):
        """Return the best element from the current population."""
        return max(population, key=self.objective_function)

    def get_better(self, dominant, recessive):
        """Return the better element.

        Compare two elements between each other and return the better one.
        If they are equal, return dominant.
        """
        if self.objective_function(recessive) > self.objective_function(dominant):
            return recessive
        return dominant

    def direct_tournament(self, population):
        """Select element by direct comparison.

        Pick up two random elements from the population
        and return the better one.
        """
        player1 = random.choice(population)
        player2 = random.choice(population)
        return self.get_better(player1, player2)

    def select_parents(self, population, best_count):
        """Select parents for reproduction from the population.

        - population -- population to chose parents from
        - best_count -- number of the best elements from the population to pick up
        """
        parents = []
        sorted(population, key=self.objective_function)
        while len(parents) <= self.population_size:
            parents.append(self.direct_tournament(population[:best_count]))
        return population

    def crossover(self, parent1, parent2, crossover_prob):
        """Crossover parents and return their child.

        - parent1, parent2 -- parents to crossover
        - crossover_prob -- probability of crossover
        """
        if random.random() > crossover_prob:
            return parent1
        return self.matcher.recombine(parent1, parent2)

    def mutation(self, element):
        """Return mutated element."""
        return self.matcher.mutate(element)

    def reproduce(self, parents, crossover_prob=CROSSOVER_PROB):
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
            child = self.crossover(parent, parent2, crossover_prob)
            child = self.mutation(child)
            children.append(child)
        return children

    def search(self, time_limit, initial_population):
        """Search for the best matching element.

        Search by optimization of the objective function using
        genetic algorithm.
        """
        population = initial_population
        end_time = time.time() + time_limit
        best = self.get_population_best(population)

        while time.time() < end_time:
            parents = self.select_parents(population, self.population_size)
            children = self.reproduce(parents)
            population = children
            best = self.get_better(best, self.get_population_best(population))

        return best

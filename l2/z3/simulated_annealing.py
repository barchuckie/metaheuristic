"""Simulated Anneling implementation for finding the shortest way to exit from a maze."""


import time
import math
import random
from enums import *

START_TEMP = 10**10
COOLING_CONST = 0.99
END_TEMP = 0.1  # 1e-10
PROBABILITY_CONST = 1
UNCHANGED_RESULT_ITERATIONS = 50


def get_probability(delta, temp):
    """Calculate probability based on delta and temperature.

    Acceptance function in SA algorithm.
    """
    if delta < 0:
        return 1
    return math.exp(-delta/temp)


class SimulatedAnnealing:
    """Implementation of SA algorithm to find the shortest path to the exit."""

    def __init__(self, maze):
        """Initialize new instance with a maze to search in."""
        self.maze = maze

    def get_delta(self, current, candidate):
        """Calculate delta end return it.

        Delta is a difference in function value between candidate arguments and
        current arguments.
        """
        return self.maze.cost(candidate) - self.maze.cost(current)

    def cooling_schedule(self, temp):
        """Update temperature in SA algorithm."""
        return COOLING_CONST*temp

    def run(self, time_limit):
        """Run Simulated Annealing for maze escape.

        Return shortest path found during algorithm run.
        time_limit -- max time to run
        """
        end_time = time.time() + time_limit
        current = self.maze.create_first()
        result = current
        temp = len(self.maze.grid)*len(self.maze.grid[0])
        result_it = 0

        while time.time() <= end_time:
            candidate = self.maze.get_random_neighbor(current)
            delta = self.get_delta(current, candidate)
            if get_probability(delta, temp) > random.random():
                current = candidate
            if self.maze.cost(result) > self.maze.cost(current):
                result = current
                result_it = 0
            temp = self.cooling_schedule(temp)
            if temp <= END_TEMP:
                result_it += 1
                if result_it >= UNCHANGED_RESULT_ITERATIONS:
                    break
                current = self.maze.create_first()
                temp = START_TEMP

        return result

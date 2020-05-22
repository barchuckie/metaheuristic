"""L3/Z1.

Finding minimum of X. S. Yang function with Particle Swarm Optimization algorithm.

Author: Patryk Barczak
"""
import random
import time
from dataclasses import dataclass

import numpy as np


POPULATION_SIZE = 100
DIMENSION = 5
BOUNDARY = 5
BRAKE_COEF = 0.7
PARTICLE_BEST_COEF = 0.3
GLOBAL_BEST_COEF = 1.5


def yang(coefs, args):
    """Calculate X. S. Yang function value in point x = (args) with given coefficients."""
    return sum(coefs*abs(args))


@dataclass
class Particle:
    """Class representing single particle in the PSO algorithm."""
    id: int
    position: np.ndarray
    cost: int
    velocity: np.ndarray
    best_position: np.ndarray
    best_cost: int
    objective_fn: callable

    def __init__(self, position, velocity, objective_fn):
        """Create new instance of a particle.

        The particle is set on the given position and with velocity.
        Objective function is used for calculating cost of the particle.
        """
        self.position = position
        self.velocity = velocity
        self.objective_fn = objective_fn
        self.cost = self.objective_fn(self.position)
        self.best_cost = self.cost
        self.best_position = np.array(self.position)

    def update_cost(self):
        """Update cost of the particle and check whether it is the best yet."""
        self.cost = self.objective_fn(self.position)
        if self.cost < self.best_cost:
            self.best_cost = self.cost
            self.best_position = np.array(self.position)


def create_vector(boundary=BOUNDARY, dimension=DIMENSION):
    """Create vector of random values.

    - boundary -- boundary for randomizing values
    - dimensions -- size of the returned vector
    """
    return np.array([random.uniform(-boundary, boundary) for _ in range(dimension)])


def get_global_best(population, current_best=None):
    """Return particle with global minimum."""
    best = sorted(population, key=lambda p: p.cost)[0]
    if current_best is None or best.cost < current_best.best_cost:
        return best
    return current_best


def check_stop_condition(population):
    """Check for stopping conditions of PSO algorithm.

    Algorithm should stop when all particles in the population are
    in the same position or all their velocities are 0.
    """
    velocity_cond = True
    position_cond = True
    position = population[0].position
    for particle in population:
        if not np.allclose(particle.velocity, 0, atol=1e-320):
            velocity_cond = False
            if not position_cond:
                return False
        if not np.allclose(particle.position, position, atol=1e-320):
            position_cond = False
            if not velocity_cond:
                return False

    return True


class PSO:
    """Particle Swarm Optimization class."""
    def __init__(self,
                 objective_fn,
                 brake_coef=BRAKE_COEF,
                 particle_best_coef=PARTICLE_BEST_COEF,
                 global_best_coef=GLOBAL_BEST_COEF
                 ):
        """Create new instance of PSO algorithm class with given properties.

        - objective_fn -- objective function to minimize
        - brake_coef, particle_best_coef, global_best_coef -- coefficients
            for recalculating particles' velocities
        """
        self.objective_fn = objective_fn
        self.brake_coef = brake_coef
        self.particle_best_coef = particle_best_coef
        self.global_best_coef = global_best_coef

    def generate_population(self, population_size=POPULATION_SIZE):
        """Generate population for PSO algorithm of a given size."""
        return np.array([Particle(create_vector(), create_vector(), self.objective_fn) for _ in range(population_size)])

    def update_velocity(self, particle, global_best_position):
        """Update velocity of the particle.

        New velocity is calculated on current velocity
        and distances from global best and self best.
        """
        pbc = random.uniform(0, self.particle_best_coef)
        gbc = random.uniform(0, self.global_best_coef)
        v1 = self.brake_coef*particle.velocity
        v2 = pbc*(particle.best_position - particle.position)
        v3 = gbc*(global_best_position - particle.position)
        particle.velocity = v1 + v2 + v3

    def update_position(self, particle, boundary=BOUNDARY):
        """Update position of the particle.

        Position is updated and corrected if it exceeds boundary.
        After this, particle's cost is recalculated, too.
        """
        particle.position = particle.position + particle.velocity
        for i in range(len(particle.position)):
            if particle.position[i] > boundary:
                particle.position[i] = boundary
                particle.velocity[i] *= -1
            if particle.position[i] < -boundary:
                particle.position[i] = -boundary
                particle.velocity[i] *= -1
        particle.update_cost()

    def update_population(self, population, global_best_position):
        """Update all particles in population.

        There is updated velocity and position of a particle.
        - population -- population to update
        - global_best_position -- position of the globally best particle
        """
        for particle in population:
            self.update_velocity(particle, global_best_position)
            self.update_position(particle)

    def search(self, time_limit):
        """Search for global minimum using PSO algorithm.

        - time_limit -- time limit for algorithm in seconds
        """
        end_time = time.time() + time_limit
        population = self.generate_population()
        global_best = get_global_best(population)

        while time.time() < end_time:
            self.update_population(population, global_best.best_position)
            global_best = get_global_best(population, global_best)

            if check_stop_condition(population):
                break

        return global_best.best_position, global_best.best_cost


def find_minimum():
    """Find minimum of Yang function with input data."""
    i = input().split()
    time_limit = int(i[0])
    coefs = np.array(tuple(map(float, i[6:])))

    def defined_yang(args):
        return yang(coefs, args)

    pso = PSO(defined_yang)

    result = pso.search(time_limit)
    print(' '.join(list(map(str, result[0]))), result[1])


if __name__ == '__main__':
    find_minimum()

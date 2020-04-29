"""L2/Z1.

Finding minimum of Salomon function with simulated annealing.
Author: Patryk Barczak
"""
import math
import random
import time


START_TEMP = 10*10
END_TEMP = 1e-10
COOLING_CONST = 0.6
PROBABILITY_CONST = 1


def salomon(*args):
    """Calculate Salomon function value in point x = (args)."""
    norm = math.sqrt(sum(map(lambda u: u*u, args)))
    result = 1 - math.cos(2*math.pi*norm) + 0.1*norm
    return result


def get_probability(delta, temp):
    """Calculate probability based on delta and temperature.

    Acceptance function in SA algorithm.
    """
    if delta < 0:
        return 1
    return math.exp(-delta/temp)


def geometric_change(temp):
    """Return geometric change of temperature."""
    return temp*COOLING_CONST


def cooling_schedule(temp):
    """Update temperature value."""
    return temp/(COOLING_CONST*temp+1)


def random_direction(dimensions):
    """Find new function arguments to check."""
    vector = [random.gauss(0, 0.5) for _ in range(dimensions)]
    mag = math.sqrt(sum(map(lambda u: u*u, vector)))
    return tuple(x/mag for x in vector)


def get_delta(function, current_args, candidate_args):
    """Calculate delta end return it.

    Delta is a difference in function value between check_args and
    current_args.
    """
    return function(*candidate_args) - function(*current_args)


def get_step(args):
    """Calculate step length.

    Step is calculated on the distance from global minimum.
    """
    return abs(random.gauss(0, 1))


def new_candidate(args):
    """Find new function arguments to check."""
    direction = random_direction(len(args))
    step = get_step(args)
    vector = [step*x for x in direction]
    result = tuple(map(sum, zip(args, vector)))
    return result


def simulated_annealing(function, time_limit, *start_args):
    """Perform simulated annealing algorithm to find function's minimum.

    -- function - function to find minimum in
    -- time_limit - limit of time to stop searching in seconds
    -- *start_args - coordinates of the starting point
    """
    temp = START_TEMP
    result_args = start_args
    current = start_args
    current_val = function(*current)
    result_val = current_val
    end_time = time.time() + time_limit

    while time.time() < end_time:
        candidate = new_candidate(current)
        candidate_val = function(*candidate)
        delta = candidate_val - current_val
        if get_probability(delta, temp) > random.random():
            current, current_val = candidate, candidate_val
        temp = cooling_schedule(temp)
        if function(*current) < function(*result_args):
            result_args, result_val = current, current_val
        if temp <= END_TEMP:
            break

    return (*result_args, result_val)


def main():
    """Find min of Salomon function with input data."""
    i = input().split()
    time_limit = int(i[0])
    start_args = tuple(map(int, i[1:]))

    result = simulated_annealing(salomon, time_limit, *start_args)
    print(' '.join(map(str, result)))


if __name__ == '__main__':
    main()

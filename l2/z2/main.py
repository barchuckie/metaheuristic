"""L2/Z2.

Find the closest matrix M', which fulfils some conditions, to a given matrix M.
Author: Patryk Barczak
"""
import sys
import numpy as np

from matrix import ClosestMatrixFinder


def print_matrix(matrix, out=sys.stderr):
    """Print matrix to the given output (out)."""
    for row in matrix:
        print(' '.join(map(str, row)), file=out)


def main():
    """Find the closest matrix M' to matrix M from the input data."""
    i = input().split()
    time_limit = int(i[0])
    n = int(i[1])
    m = int(i[2])
    k = int(i[3])

    matrix = []
    for i in range(n):
        matrix.append(list(map(int, input().split())))

    matrix_finder = ClosestMatrixFinder(np.array(matrix, dtype=np.uint8), k)
    result = matrix_finder.simulated_annealing(time_limit)

    print_matrix(result.matrix)
    print(matrix_finder.distance_from_original(result.matrix))


if __name__ == '__main__':
    main()

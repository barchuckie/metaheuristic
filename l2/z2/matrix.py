"""Implementation of Simulated Annealing for finding closest matrix."""


import time
import random
import math
from dataclasses import dataclass
import numpy as np
import copy


START_TEMP = 10**20
END_TEMP = 1e-10
COOLING_A = 0.99

MATCH_VALS = [0, 32, 64, 128, 160, 192, 223, 255]


@dataclass
class MatrixBlock:
    """Data representation of single block in matrix.

    All elements in the block have the same value."""
    row: int
    col: int
    height: int
    width: int
    value: np.uint8
    content: np.ndarray

    @property
    def start_point(self) -> tuple:
        """Starting point coordinates of the block in matrix.

        It is a point in left upper corner of the block."""
        return self.row, self.col

    def change_value(self, value):
        """Change values in the block.

        -- value - new value
        """
        self.value = value
        self.fill_content()

    def fill_content(self):
        """Fill the matrix block with its value."""
        self.content[:, :] = np.full((self.height, self.width), self.value)


class MatrixException(Exception):
    """Matrix exception raised when met problem with matrix, especially with its block-build."""

    def __init__(self, val='Matrix is invalid.'):
        self.value = val

    def __str__(self):
        return repr(self.value)


def get_probability(delta, temp):
    """Calculate probability based on delta and temperature.

    Acceptance function in SA algorithm.
    """
    if delta < 0:
        return 1
    return math.exp(-delta / temp)


def geometric_cooling(temp):
    """Geometric function for temperature update."""
    return temp * COOLING_A


def distance(matrix1, matrix2):
    """Calculate and return the distance between matrix1 and matrix2."""
    rows = len(matrix1)
    cols = len(matrix1[0])
    s = 0
    if not rows == len(matrix2) != 0 or not cols == len(matrix2[0]) != 0:
        raise MatrixException('Different matrix sizes.')

    for i in range(rows):
        for j in range(cols):
            s += (matrix1[i][j] - matrix2[i][j]) ** 2
    return s / (rows * cols)


def change_block_intensity(block: MatrixBlock, original_matrix):
    """Change block value to be nearest to original_matrix."""
    original_matrix_block = original_matrix[block.row:block.row + block.height, block.col:block.col + block.width]
    best = distance(block.content, original_matrix_block)
    best_val = block.value
    for val in MATCH_VALS:
        if distance(np.full((block.height, block.width), val), original_matrix_block) < best:
            best_val = val
    block.change_value(best_val)


class BlockMatrix:
    """Representation of matrix made of blocks."""

    def __init__(self, rows, cols, k, init: np.uint8 = 0):
        """Initialize new instance with given parameters.

        Build up a matrix with init values, choose proper neighbor creator and divide matrix into stored blocks.

        -- rows - matrix row number
        -- cols - matrix columns number
        -- k - minimum size of the block (side length)
        -- init - initial value to fill matrix with
        """
        self.rows = rows
        self.cols = cols
        self.k = k
        self.structure = []
        self.matrix = np.full((rows, cols), init)
        self.new_neighbor = self._set_neighborhood()
        self.create_blocks()

    def _set_neighborhood(self):
        """Set proper neighborhood picking."""
        if self.rows % self.k == 0 and self.cols % self.k == 0:
            return self._simple_neighbor
        else:
            return self._complex_neighbor

    def create_blocks(self):
        """Create blocks of size kxk or bigger."""
        i = 0
        while i + 2 * self.k <= self.rows:
            self.create_row(i, i + self.k)
            i += self.k
        self.create_row(i, None)

    def create_row(self, start, end):
        """Create row of blocks with size (end-start) and at least k."""
        i = 0
        while i + 2 * self.k <= self.cols:
            block = self.matrix[start:end, i:i + self.k]
            self.structure.append(MatrixBlock(start, i, len(block), len(block[0]), self.matrix[start, i], block))
            i += self.k
        block = self.matrix[start:end, i:]
        self.structure.append(MatrixBlock(start, i, len(block), len(block[0]), self.matrix[start, i], block))

    def _simple_neighbor(self, original_matrix):
        """Create neighbor matrix.

        Deepcopy itself and change intensity of randomly chosen block.
        Function is called when sides of matrix are multiplies of k,
        since change of block sizes is nonsense in this case.
        """
        neighbor = copy.deepcopy(self)
        block = random.choice(list(neighbor.structure))
        change_block_intensity(block, original_matrix)
        return neighbor

    def _complex_neighbor(self, original_matrix):
        """Create neighbor matrix.

        Get all direct neighbors of the block. Randomly pick up the way of creating a new neighbor.
        However, if such neighborhood is empty, just change block intensity."""
        neighbor = copy.deepcopy(self)
        block: MatrixBlock = random.choice(list(neighbor.structure))
        neighborhood = neighbor.get_block_direct_neighborhood(block)
        if neighborhood:
            if random.random() < 0.5:
                neighbor.resize_block(block, neighborhood, original_matrix)
            else:
                neighbor.swap_block(block, neighborhood, original_matrix)
        else:
            change_block_intensity(block, original_matrix)
        return neighbor

    def rebuild_content(self, block):
        """Rebuild block in the matrix.

        Usually called after block size change.
        """
        block.content = self.matrix[block.row:block.row + block.height, block.col:block.col + block.width]
        block.fill_content()

    def resize_block(self, block: MatrixBlock, neighborhood, original_matrix):
        """Reduce block size and expand his random neighbor size by moving side between them.

        -- block - block to reduce size
        -- neighborhood - block's direct neighbor blocks
        -- original_matrix - original matrix for changing intensity in case of reducing failure
        """
        neighbor = random.choice(neighborhood)
        if neighbor.row == block.row and block.width > self.k:
            reduce_size = random.randrange(1, block.width - self.k + 1)
            if neighbor.col < block.col:
                neighbor.width += reduce_size
                block.col += reduce_size
                block.width -= reduce_size
            else:
                neighbor.width += reduce_size
                neighbor.col -= reduce_size
                block.width -= reduce_size
            self.rebuild_content(neighbor)
            self.rebuild_content(block)
        elif neighbor.col == block.col and block.height > self.k:
            reduce_size = random.randrange(1, block.height - self.k + 1)
            if neighbor.row < block.row:
                neighbor.height += reduce_size
                block.row += reduce_size
                block.height -= reduce_size
            else:
                neighbor.height += reduce_size
                neighbor.row -= reduce_size
                block.height -= reduce_size
            self.rebuild_content(neighbor)
            self.rebuild_content(block)
        else:
            change_block_intensity(block, original_matrix)

    def swap_block(self, block: MatrixBlock, neighborhood, original_matrix):
        """Swap block size with his random neighbor.

        -- block - block to swap size with
        -- neighborhood - block's direct neighbor blocks
        -- original_matrix - original matrix for changing intensity in case of swapping failure
        """
        swap_neighborhood = []
        for neighbor in neighborhood:
            if not (block.height == neighbor.height and block.width == neighbor.width):
                swap_neighborhood.append(neighbor)

        if not swap_neighborhood:
            change_block_intensity(block, original_matrix)
            return

        swap_neighbor = random.choice(list(swap_neighborhood))

        if swap_neighbor.row == block.row:
            if swap_neighbor.col < block.col:
                swap_neighbor.width, block.width = block.width, swap_neighbor.width
                block.col = swap_neighbor.col + swap_neighbor.width
            else:
                swap_neighbor.width, block.width = block.width, swap_neighbor.width
                swap_neighbor.col = block.col + block.width
        elif swap_neighbor.col == block.col:
            if swap_neighbor.row < block.row:
                swap_neighbor.height, block.height = block.height, swap_neighbor.height
                block.row = swap_neighbor.row + swap_neighbor.height
            else:
                swap_neighbor.height, block.height = block.height, swap_neighbor.height
                swap_neighbor.row = block.row + block.height
        self.rebuild_content(swap_neighbor)
        self.rebuild_content(block)

    def get_block_direct_neighborhood(self, block: MatrixBlock):
        """Find all direct neighbors of the block.

        Direct neighbors are these which have the same length of the common side with the block."""
        neighborhood = []
        for b in self.structure:
            if (b.row + b.height, b.col) == block.start_point and b.width == block.width:
                neighborhood.append(b)
            elif (b.row, b.col + b.width) == block.start_point and b.height == block.height:
                neighborhood.append(b)
            elif b.start_point == (block.row, block.col + block.width) and b.height == block.height:
                neighborhood.append(b)
            elif b.start_point == (block.row + block.height, block.col) and b.width == block.width:
                neighborhood.append(b)
            if len(neighborhood) >= 4:
                break
        return neighborhood

    def __deepcopy__(self, memodict={}):
        new = type(self)(self.rows, self.cols, self.k)
        new.structure = []
        new.matrix = copy.deepcopy(self.matrix)
        for block in self.structure:
            new.structure.append(MatrixBlock(block.row, block.col, block.height, block.width, block.value, new.matrix[block.row:block.row + block.height, block.col:block.col + block.width]))
        new.new_neighbor = new._set_neighborhood()
        return new


class ClosestMatrixFinder:
    """Implementation of finding closest matrix using simulated annealing."""

    def __init__(self, matrix, min_block_size):
        """Initialize new instance of finder with given size of matrix."""
        self.rows = len(matrix)
        self.cols = len(matrix[0])
        self.original_matrix = matrix
        self.min_block_size = min_block_size

    def distance_from_original(self, matrix):
        """Calculate and return the distance between matrix1 and matrix2."""
        return distance(self.original_matrix, matrix)

    def get_start_matrix(self):
        """Create first instance of candidate matrix."""
        return BlockMatrix(self.rows, self.cols, self.min_block_size)

    def new_candidate(self, matrix):
        """Create new candidate to consider in SA."""
        return matrix.new_neighbor(self.original_matrix)

    def cooling_schedule(self, temp):
        """Update temperature value."""
        return geometric_cooling(temp)

    def simulated_annealing(self, time_limit):
        """Perform simulated annealing algorithm to find closest matrix.

        -- time_limit - limit of time to stop searching in seconds
        """
        temp = START_TEMP
        current = self.get_start_matrix()
        current_score = self.distance_from_original(current.matrix)
        result_matrix = current
        result_score = current_score
        end_time = time.time() + time_limit
        it = 0

        while temp > END_TEMP and time.time() < end_time:
            candidate_matrix = self.new_candidate(current)
            candidate_score = self.distance_from_original(candidate_matrix.matrix)
            if get_probability(candidate_score-current_score, temp) > random.random():
                current = candidate_matrix
                current_score = candidate_score
            temp = self.cooling_schedule(temp)
            if current_score < result_score:
                result_matrix = current
                result_score = current_score
            it += 1

        return result_matrix

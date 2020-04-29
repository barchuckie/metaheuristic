from enums import *
from maze import *


def main():
    '''Main function of the package'''
    i = input().split()
    t = int(i[0])
    n = int(i[1])
    m = int(i[2])

    grid = []
    start = -1
    exit = -1
    for i in range(n):
        row = list(map(lambda u: Field(int(u)), input().replace('\r', '')))
        if Field.AGENT in row:
            start = (i, row.index(Field.AGENT))
        if Field.EXIT in row:
            exit = (i, row.index(Field.EXIT))
        grid.append(row)

    maze = Maze(grid, start, exit)
    maze.tabusearch(t, n+m)


if __name__ == '__main__':
    main()

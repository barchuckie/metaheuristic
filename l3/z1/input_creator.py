import random


TIME = 10
INITIAL_ARGS = [1, 5, -2, 2, -2]


def write_input():
    print(TIME, ' '.join(list(map(str, INITIAL_ARGS))), end='')
    for _ in range(5):
        print('', random.random(), end='')
    print()


if __name__ == '__main__':
    write_input()

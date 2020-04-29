import math
import random
from time import time


def happycat(x1, x2, x3, x4):
    args = [x1, x2, x3, x4]
    x = sum(map(lambda u: u*u, args))
    return 0.5 + ((x - 4)**2)**(1/8) + (x/2 + sum(args))/4


def griewank(x1, x2, x3, x4):
    args = [x1, x2, x3, x4]
    s = 0
    prod = 1
    for i, x in enumerate(args):
        s += x**2/4000
        prod *= math.cos(x/math.sqrt(i+1))
    return 1 + s - prod


def localsearch(f, t, r = 10, a = 100, b = -100, candidates = 100):
    #best = (0,0,0,0)
    #best = tuple([3.10299516e-12, 1.47052138e-08, 6.88552228e-09, 4.14543269e-13] )
    best = [random.uniform(a,b), random.uniform(a,b), random.uniform(a,b), random.uniform(a,b)]
    endtime = time() + t

    while time() <= endtime:
        candidate = tuple(map(lambda u: u*random.gauss(1, 0.5), best))
        for i in range(candidates):
            cur_candidate = tuple(map(lambda u: u*random.gauss(1, 0.5), best))
            if f(*cur_candidate) < f(*candidate):
                candidate = cur_candidate
        if f(*candidate) < f(*best):
            best = candidate


    print('{0} {1} {2} {3}'.format(*best), f(*best))


def main():
    '''Main function of the package'''
    i = input().split()
    t = int(i[0])
    b = int(i[1])

    if b == 0:
        localsearch(happycat, t, r = 0.2)
    else:
        localsearch(griewank, t, r = 12)


if __name__ == '__main__':
    main()

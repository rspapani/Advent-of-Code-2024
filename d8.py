from collections import defaultdict as ddict, Counter as count
from functools import reduce,  cmp_to_key, partial as par
from math import prod, sqrt as root, lcm as lcm, gcd as gcd
from operator import itemgetter as ig
from re import findall as rall

import math
import re

from aoc import *

file = open("d8.txt")
raws = file.read().splitlines()
file.close()

rawss = """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............""".splitlines()

def proc(li):
    posses = ddict(lambda: list())

    for x, row in enumerate(li):
        for y, ch in enumerate(row):
            if ch != '.':
                posses[ch].append(x + (y*1j))

    return posses, len(li), len(li[0])
    

inpt = proc(raws)

def f1(posses, mx, my):
    bounded = lambda p: 0 <= p.real < mx and 0 <= p.imag < my

    resos = set()

    for _,coords  in posses.items():
        for i, p1 in enumerate(coords):
            for p2 in coords[i + 1:]:
                slp = p2 - p1
                r1 = p2 + slp
                r2 = p1 - slp

                if bounded(r1):
                    resos.add(r1)

                if bounded(r2):
                    resos.add(r2)

    return len(resos)


def f2(posses, mx, my):
    bounded = lambda p: 0 <= p.real < mx and 0 <= p.imag < my

    resos = set()

    for _,coords  in posses.items():
        for i, p1 in enumerate(coords):
            for p2 in coords[i + 1:]:
                slp = p2 - p1
                r1 = p2

                while bounded(r1):
                    resos.add(r1)
                    r1 += slp

                r2 = p1
                while bounded(r2):
                    resos.add(r2)
                    r2 -= slp

    return len(resos)

print("Part 1: ", f1(*inpt))
print("Part 2: ", f2(*inpt))

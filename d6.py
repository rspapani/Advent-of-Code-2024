from collections import defaultdict as ddict, Counter as count
from functools import reduce,  cmp_to_key, partial as par
from math import prod, sqrt as root, lcm as lcm, gcd as gcd
from operator import itemgetter as ig
from re import findall as rall

import math
import re

from aoc import *

file = open("d6.txt")
raws = file.read().splitlines()
file.close()

rsaws = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...""".splitlines()

inpt = raws

def f1(li):
    
    for x, row in enumerate(li):
        for y, ch in enumerate(row):
            if ch == '^':
                strt = x + (y*1j)

    mx, my = len(li), len(li[0])

    bounded = lambda k: 0 <= k.real < mx and 0 <= k.imag < my
    getch = lambda k: li[int(k.real)][int(k.imag)] if bounded(k) else 'L'

    vel = -1 + 0j
    pos = strt
    dne = set()
    
    while True:
        dne.add(pos)
        npos = pos + vel

        match getch(npos):
            case '#':
                vel *= -1j
            case '.' | '^':
                pos = npos
            case 'L':
                break

    def canloop(obs):
        vel = -1 + 0j
        pos = strt
        lpe = set()

        while (pos, vel) not in lpe:
            lpe.add((pos, vel))
            npos = pos + vel

            if npos == obs:
                vel *= -1j
                continue

            match getch(npos):
                case '#':
                    vel *= -1j
                case '.' | '^':
                    pos = npos
                case 'L':
                    return False

        return True
    
    return len(dne), len({obs for obs in dne
                          if obs != strt and canloop(obs)
                        })

def f2(li):
    pass

print("Part 1: ", f1(inpt))
print("Part 2: ", f2(inpt))

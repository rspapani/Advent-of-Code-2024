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
    
    lobj = strt - 1j
    redirs = ddict(lambda: dict())

    while True:
        dne.add(pos)
        npos = pos + vel

        match getch(npos):
            case '#':
                redirs[lobj][vel * 1j] = pos
                lobj = npos

                if vel in redirs[npos]:
                    pos = redirs[npos][vel]
                    
                vel *= -1j
            case '.' | '^':
                pos = npos
            case 'L':
                break

    
    def canloop(obs):
        vel = -1 + 0j
        pos = strt
        lpe = set()
        sve = False

        inbet = lambda p1, p2: \
                    ((p1.real == obs.real == p2.real) and 
                    (min(p1.imag, p2.imag) <= obs.imag <= max(p1.imag, p2.imag))) or \
                    ((p1.imag == obs.imag == p2.imag) and 
                    (min(p1.real, p2.real) <= obs.real <= max(p1.real, p2.real)))

        while (pos, vel) not in lpe:
            lpe.add((pos, vel))
            npos = pos + vel

            if npos == obs:
                vel *= -1j
                continue

            match getch(npos):
                case '#':
                    if sve:
                        redirs[lobj][vel * 1j] = pos

                    if vel in redirs[npos]:
                        fpos = redirs[npos][vel]

                        # we choose not to memoize the redirects of our new obstacles
                        # cause that's a nuisance
                        if not inbet(pos, fpos):
                            pos = fpos

                        sve = False

                    else:
                        sve = True
                        lobj = npos

                    vel *= -1j
                case '.' | '^':
                    pos = npos
                case 'L':
                    return False

        return True
    
    return len(dne), sum((canloop(obs) for obs in dne
                          if obs != strt 
                          ))

def f2(li):
    pass

print("Part 1: ", f1(inpt))
print("Part 2: ", f2(inpt))

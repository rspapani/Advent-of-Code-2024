from collections import defaultdict as ddict, Counter as count
from functools import reduce,  cmp_to_key, partial as par
from math import prod, sqrt as root, lcm as lcm, gcd as gcd
from operator import itemgetter as ig
from re import findall as rall

import math
import re

from aoc import *

file = open("d12.txt")
raws = file.read().splitlines()
file.close()

rasws = """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE""".splitlines()

def proc(x):
    return x

inpt = lmap(proc, raws)

mx, my = len(inpt), len(inpt[0])
bounded = lambda k: 0 <= k.real < mx and 0 <= k.imag < my
getval = lambda k: inpt[int(k.real)][int(k.imag)] if bounded(k) else '.'

dirs = [(1j)**i for i in range(4)]
adj = lambda k: [k + dp for dp in dirs]

def flood(pos, ch):
    dne = set()
    perim = 0

    tbd = {pos}

    while tbd:
        npos = tbd.pop()
        dne.add(npos)
        nxts, bord = fsplit(lambda x: getval(x) == ch,
                            adj(npos))
        
        perim += len(bord)
        tbd.update([nxt for nxt in nxts
                    if nxt not in dne])
        
    return dne, perim

def f1(li, f = flood):
    gdne = set()
    outs = 0

    for x, row in enumerate(li):
        for y, ch in enumerate(row):
            cpos = x + (y*1j)
            if cpos not in gdne:
                cdne, cper = f(cpos, ch)
                outs += len(cdne) * cper
                gdne |= cdne
            
    return outs


# dirs2 = [(1 - 1j) * (1j**i) for i in range(4)]
# diags = lambda k: [k + dp 
#                    for pair in zip(dirs, dirs2)
#                    for dp in pair]

cdirs = [(i, i + j, j) for i,j in 
         zip(dirs, dirs[1:] + [dirs[0]])]


corn = lambda k: [(k + i, k + ij, k + j)
                  for i, ij, j in cdirs]

corns = {(0, 0, 0),(1, 1, 0),(0, 1, 0)}

def iscorn(pos):
    ch = getval(pos)
    iscorn = lambda diag: tuple(getval(c) == ch for c in diag) in corns
    
    return sum((iscorn(x) for x in corn(pos)))

def floodplusplus(pos, ch):
    spce, _ = flood(pos, ch)
    sides = sum(map(iscorn, spce))
    return spce, sides

def f2(li):
    return f1(li, f=floodplusplus)


print("Part 1: ", f1(inpt))
print("Part 2: ", f2(inpt))

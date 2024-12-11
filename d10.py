from collections import defaultdict as ddict, Counter as count
from functools import reduce,  cmp_to_key, partial as par
from math import prod, sqrt as root, lcm as lcm, gcd as gcd
from operator import itemgetter as ig
from re import findall as rall

import math
import re

from aoc import *

file = open("d10.txt")
raws = file.read().splitlines()
file.close()

rws = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732""".splitlines()

def proc(x):
    return lmap(int, x)

inpt = lmap(proc, raws)

mx, my = len(inpt), len(inpt[0])
bounded = lambda k: 0 <= k.real < mx and 0 <= k.imag < my
getval = lambda k: inpt[int(k.real)][int(k.imag)] if bounded(k) else -1

dirs = [(1j)**i for i in range(4)]
adj = lambda k: [k + dp for dp in dirs]

zeros = []
for x,row in enumerate(inpt):
    for y, val in enumerate(row):
        if val == 0:
            zeros.append(x + (y*1j))

def f1(li):
    def score(pos):
        posses = {pos}

        for i in range(1, 10):
            posses = {npos for p in posses
                    for npos in adj(p) 
                    if getval(npos) == i}
            
        return len(posses)
    
    return sum(map(score, zeros))

def f2(li):
    def score(pos):
        posses = ddict(lambda: 0)
        posses[pos] = 1

        for i in range(1, 10):
            np = ddict(lambda: 0)
            for npos, paths in posses.items():
                for nxt in filter(lambda x: getval(x) == i, adj(npos)):
                    np[nxt] += paths

            posses = np
            
        return sum(list(posses.values()))
    
    return sum(map(score, zeros))

print("Part 1: ", f1(inpt))
print("Part 2: ", f2(inpt))

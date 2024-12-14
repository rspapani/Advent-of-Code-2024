from collections import defaultdict as ddict, Counter as count
from functools import reduce,  cmp_to_key, partial as par
from math import prod, sqrt as root, lcm as lcm, gcd as gcd
from operator import itemgetter as ig
from re import findall as rall

import os, time

import math
import re

from aoc import *

file = open("d14.txt")
raws = file.read().splitlines()
file.close()

rws = """p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3""".splitlines()
    

def proc(x):
    ints = getints(x)
    p = ints[:2]
    v = ints[2:]
    return (p[0] + (p[1] * 1j)),(v[0] + (v[1]*1j))

inpt = lmap(proc, raws)

mx, my = 101, 103

bound = lambda k: int(k.real)%mx + ((int(k.imag)%my) * 1j)
oned = lambda k: int(k.real) == mx//2 or int(k.imag) ==  my//2
onr = lambda k: int(k.real) > mx//2 
onb = lambda k: int(k.imag) > my//2

def getq(p, v):
    k = bound(p + 100*v)
    return 2*onb(k) + onr(k) if not oned(k) else 4

def f1(li):
    quads = [0, 0, 0, 0, 0]

    for p, v in li:
        quads[getq(p, v)] += 1

    return reduce(lambda a, b: a*b, quads[:-1])

def f2(li):
    posses = {i:p[0] for i,p in enumerate(li)}

    mn = (float('inf'), -1)
    for wi in range(1, 103*101):
        for i,p in enumerate(li):
            posses[i] = bound(posses[i] + p[1])

        cent = sum(posses.values())/len(posses)
        disp = sum(abs(x - cent) for x in posses.values())/len(posses)

        mn = min(mn, (disp, wi))

    return mn

print("Part 1: ", f1(inpt))
print("Part 2: ", f2(inpt))

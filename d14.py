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

mx = 101
my = 103

# mx, my = 11, 7

bound = lambda k: int(k.real)%mx + ((int(k.imag)%my) * 1j)
oned = lambda k: int(k.real) == mx//2 or int(k.imag) ==  my//2
onr = lambda k: int(k.real) > mx//2 
onb = lambda k: int(k.imag) > my//2

def getq(p, v):
    k = bound(p + 100*v)

    if oned(k):
        return 4
    
    else:
        return 2*onb(k) + onr(k)

    

def proc(x):
    ints = getints(x)
    p = ints[:2]
    v = ints[2:]
    return (p[0] + (p[1] * 1j)),(v[0] + (v[1]*1j))

inpt = lmap(proc, raws)
# print(inpt)

def f1(li):
    quads = [0, 0, 0, 0, 0]

    for p, v in li:
        quads[getq(p, v)] += 1

    return reduce(lambda a, b: a*b, quads[:-1])

# def getperiod(k):

#i'm not making it faster, bite me
def render(dne, ch='X'):
    
    outs = []
    for x in range(mx):
        row = []
        for y in range(my):
            if x + (y*1j) in dne.values():
                row.append(ch)
            else:
                row.append('.')
        outs.append("".join(row))
        
    potential = any("XXXXXXXXX" in row for row in outs)

    if potential:
        os.system('clear')
        print('\n'.join(outs))

    return potential

def f2(li):
    posses = {i:p[0] for i,p in enumerate(li)}
    targ = 7750
    wi = 0

    while True:
        wi += 1
        if wi%100 == 0:
            print(wi)

        for i,p in enumerate(li):
            posses[i] = bound(posses[i] + p[1])

        if wi >= targ:
            if render(dne=posses):
                return wi


        if wi >= 103*101:
            break

# f2(inpt)
print("Part 1: ", f1(inpt))
print("Part 2: ", f2(inpt))

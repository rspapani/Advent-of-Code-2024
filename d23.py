from collections import defaultdict as ddict, Counter as count
from functools import reduce,  cmp_to_key, partial as par
from math import prod, sqrt as root, lcm as lcm, gcd as gcd
from operator import itemgetter as ig
from re import findall as rall

import math
import re

from aoc import *

file = open("d23.txt")
raws = file.read().splitlines()
file.close()

rws = """
""".splitlines()

graph = ddict(lambda: set())
def proc(x):
    a, b = x.split('-')
    graph[a].add(b)
    graph[b].add(a)

inpt = lmap(proc, raws)

def twolevel(pc, dne):
    outs = 0
    rel = graph[pc] - dne
    for two in rel:
        outs += len(graph[two] & rel)

    return outs

def f1(li):
    dne = set()
    outs = 0
    for pc in graph:
        if pc[0] == 't':
            outs += twolevel(pc, dne)
            dne.add(pc)

    return outs//2

def twoleveltwo(pc, two):
    curr = [pc, two]
        
    for pot in graph:
        if pot not in [pc, two] and \
            all(pot in graph[v] for v in curr):
            curr.append(pot)

    return curr

def f2(li):
    mxcomp = []
    dne = set()

    for pc in graph:
        dne.add(pc)
        rel = graph[pc] - dne
        
        for two in rel:
            curr = twoleveltwo(pc, two)
            
            if len(curr) > len(mxcomp):
                mxcomp = curr
                
    return ",".join(sorted(mxcomp))



print("Part 1: ", f1(inpt))
print("Part 2: ", f2(inpt))

from collections import defaultdict as ddict, Counter as count
from functools import reduce,  cmp_to_key, partial as par, cache
from math import prod, sqrt as root, lcm as lcm, gcd as gcd
from operator import itemgetter as ig
from re import findall as rall

import math
import re

from aoc import *

file = open("d11.txt")
raws = file.read()
file.close()

# raws = """0 1 10 99 999"""
# raws = "125 17"

def proc(x):
    return lmap(int, x.split())

inpt = proc(raws)

@cache
def step(x):
    digs = next((i for i in range(1,100) if (10**i)>x))
    if x == 0:
        return (1,)
    elif digs%2 == 0:
        splt = 10**(digs//2)
        return (x//splt, x%splt)
    else:
        return (x * 2024,)

def f1(li):
    for i in range(25):
        li = [nx for x in li
              for nx in step(x)]
        # print(i, len(li))
        
    return len(li)

def f2(li):
    cnts = ddict(lambda: 0)
    for x in li:
        cnts[x] += 1

    for i in range(75):
        nxts = ddict(lambda: 0)

        for x, cnt in cnts.items():
            for nx in step(x):
                nxts[nx] += cnt

        cnts = nxts
        
    return sum(list(cnts.values()))

print("Part 1: ", f1(inpt))
print("Part 2: ", f2(inpt))

from collections import defaultdict as ddict, Counter as count
from functools import reduce,  cmp_to_key, partial as par
from math import prod, sqrt as root, lcm as lcm, gcd as gcd
from operator import itemgetter as ig
from re import findall as rall

import math
import re

from aoc import *

file = open("d13.txt")
raws = file.read()
file.close()

rasws = """Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279"""

raws = raws.split('\n\n')


def proc(x):
    return  lmap(getints, x.split('\n'))

inpt = lmap(proc, raws)
# print(inpt)

def eqnsolv(x, off=0):
    a, b, g = x

    g[0] += off
    g[1] += off

    d = (a[0] * b[1]) - (b[0] * a[1])
    acnt = ((b[1] * g[0]) - (b[0] * g[1]))
    bcnt = ((a[0] * g[1]) - (a[1] * g[0]))

    if d == 0 or acnt%d != 0 or bcnt%d != 0:
        return 0
    else:
        acnt = acnt//d
        bcnt = bcnt//d

        return 3*acnt + bcnt


def f1(li):
    return sum(map(eqnsolv, li))

eqnsolv2 = lambda x: eqnsolv(x, off=10000000000000)

def f2(li):
    return sum(map(eqnsolv2, li))

print("Part 1: ", f1(inpt))
print("Part 2: ", f2(inpt))

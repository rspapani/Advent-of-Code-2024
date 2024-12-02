from collections import defaultdict as ddict, Counter as count
from functools import reduce,  cmp_to_key, partial as par
from math import prod, sqrt as root, lcm as lcm, gcd as gcd
from operator import itemgetter as ig
from re import findall as rall

import math
import re

from aoc import *

file = open("d2.txt")
raws = file.read().splitlines()
file.close()

rws = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483""".splitlines()

def proc(x):
    return lmap(int, x.split())

inpt = lmap(proc, raws)

def valid(l2):
    l2 = l2 if l2[0] < l2[1] else l2[::-1]
    diffs = [y - x for x,y in zip(l2, l2[1:])]
    return all((1 <= d <= 3 for d in diffs))

def f1(li):
    return sum(map(valid, li))

def f2(li):
    def svalid(l2):
        return any((valid(l2[:i] + l2[i + 1:]) for i,_ in enumerate(l2)))

    return sum(map(svalid, li))

print("Part 1: ", f1(inpt))
print("Part 2: ", f2(inpt))

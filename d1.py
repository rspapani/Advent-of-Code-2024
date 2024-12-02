from collections import defaultdict as ddict, Counter as count
from functools import reduce,  cmp_to_key, partial as par
from math import prod, sqrt as root, lcm as lcm, gcd as gcd
from operator import itemgetter as ig
from re import findall as rall

import math
import re

from aoc import *

file = open("d1.txt")
raws = file.read().splitlines()
file.close()

rws = """
""".splitlines()

def proc(x):
    return map(int, x.split())

inpt = lzip(*map(proc, raws))

def f1(li):
    return sum((abs(x - y) for x,y in zip(sorted(li[0]), sorted(li[1]))))

def f2(li):
    cnt = count(li[1])
    return sum((x * cnt[x] for x in li[0]))

print("Part 1: ", f1(inpt))
print("Part 2: ", f2(inpt))

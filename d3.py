from collections import defaultdict as ddict, Counter as count
from functools import reduce,  cmp_to_key, partial as par
from math import prod, sqrt as root, lcm as lcm, gcd as gcd
from operator import itemgetter as ig
from re import findall as rall

import math
import re

from aoc import *

file = open("d3.txt")
raws = file.read()
file.close()

# raws = """xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))""".splitlines()

def proc(x):
    return list(re.findall(r'(do\(\)|don\'t\(\)|mul\((\d+),(\d+)\))', x))

inpt = proc(raws)
# print(inpt)

def f1(li):
    return sum((x*y for x,y in map(lambda s: (int(s[1]), int(s[2])), filter(lambda s: s[0][0] != 'd', li))))

def f2(li):
    out = 0
    mul = True
    for s in li:
        if s[0] == "don't()":
            mul = False
        elif s[0] == "do()":
            mul = True

        elif mul:
            x,y = int(s[1]), int(s[2])
            out += x * y

    return out

print("Part 1: ", f1(inpt))
print("Part 2: ", f2(inpt))

from collections import defaultdict as ddict, Counter as count
from functools import reduce,  cmp_to_key, partial as par
from math import prod, sqrt as root, lcm as lcm, gcd as gcd
from operator import itemgetter as ig
from re import findall as rall

import math
import re

from aoc import *

file = open("d7.txt")
raws = file.read().splitlines()
file.close()

sraws = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20""".splitlines()

def proc(x):
    goal, nums = x.split(': ')
    return int(goal), lmap(int, nums.split())

inpt = lmap(proc, raws)

pot = lambda goal, num: (goal - num,) if goal%num else (goal - num, goal//num)

def poss(x, f = pot):
    go, nums = x
    goals = {go}

    for num in nums[1:][::-1]:
        goals = {ng for g in goals
                 for ng in f(g, num)}
        
    return nums[0] in goals 

def pot2(goal, num):
    digs = next((10**i for i in range(1,100) if (10**i)>num))
    return pot(goal, num) + (goal//digs,) if goal%digs == num else pot(goal, num)

def f2(li):
    return sum((r[0] for r in li if poss(r, pot2)))

vald, invald = fsplit(poss, inpt)
p1 = sum((x[0] for x in vald))

print("Part 1: ", p1)
print("Part 2: ", f2(invald) + p1)

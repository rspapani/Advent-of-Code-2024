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

rawss = """190: 10 19
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

def f1(li):
    outs = 0
    rej = []
    for go, nums in li:
        og = go
        goals = [go]
        for num in nums[1:][::-1]:
            ng = []
            for i, goal in enumerate(goals):
                ng.append(goal - num)

                if not goal%num:
                    ng.append(goal//num)

            goals = ng

        if nums[0] in goals:
            outs += og

        else:
            rej.append((og, nums))

    return outs, rej

def f2(li):
    outs = 0
    for go, nums in li:
        og = go
        goals = [go]

        for num in nums[1:][::-1]:
            ng = []
            for i, goal in enumerate(goals):
                ng.append(goal - num)

                if not goal%num:
                    ng.append(goal//num)


                ### only meaningful difference
                digs = next((10**i for i in range(1,100) if (10**i)>num))

                if goal%digs == num:
                    ng.append(goal//digs)
                ###

            goals = ng

        if nums[0] in goals:
            outs += og

    return outs

p1, p2in = f1(inpt)
print("Part 1: ", p1)
print("Part 2: ", f2(p2in) + p1)

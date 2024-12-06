from collections import defaultdict as ddict, Counter as count
from functools import reduce,  cmp_to_key, partial as par
from math import prod, sqrt as root, lcm as lcm, gcd as gcd
from operator import itemgetter as ig
from re import findall as rall

import math
import re

from aoc import *

file = open("d4.txt")
raws = file.read().splitlines()
file.close()

rws = """
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX""".splitlines()[1:]

def proc(x):
    return x

inpt = lmap(proc, raws)

def matches(s):
    cnt = 0
    for i,ch in enumerate(s):
        if ch == 'X':
            cnt += s[i:i + 4] == 'XMAS'

    s = s[::-1]
    for i,ch in enumerate(s):
        if ch == 'X':
            cnt += s[i:i + 4] == 'XMAS'

    return cnt

def diag(i, n):
    sy, sx, dn = min(i, n - 1), max(i - n, 0), min(i + 1, (2*n) - i)
    return [(sy - dc, sx + dc) for dc in range(dn)]

def f1(li):
    n = len(li)
    rows = li
    cols = ["".join([row[i] for row in li]) for i,_ in enumerate(li)]
    diag1 = ["".join([li[y][x] for y,x in diag(i, n)]) for i in range(2*n) if i != n]
    diag2 = ["".join([li[n - y - 1][x] for y,x in diag(i, n)]) for i in range(2*n) if i != n]
    
    return sum(sum(map(matches, sel)) for sel in (rows, cols, diag1, diag2))

def f2(li):
    dirs = lzip(range(-1, 2),range(-1, 2))
    accept = ['MAS', 'SAM']
    def xmatch(y, x):
        d1 = "".join((li[y + dy][x + dx] for dx, dy in dirs))
        d2 = "".join((li[y - dy][x + dx] for dx, dy in dirs))

        return (d1 in accept) and (d2 in accept)

    return sum([xmatch(y + 1, x + 1)     
                for y, row in enumerate(li[1:-1])
                for x, ch in enumerate(row[1:-1])
                if ch == 'A'
                ]
            )

print("Part 1: ", f1(inpt))
print("Part 2: ", f2(inpt))

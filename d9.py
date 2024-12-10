from collections import defaultdict as ddict, Counter as count
from functools import reduce,  cmp_to_key, partial as par
from math import prod, sqrt as root, lcm as lcm, gcd as gcd
from operator import itemgetter as ig
from re import findall as rall

import heapq as hq

import math
import re

from aoc import *

file = open("d9.txt")
raws = file.read()
file.close()

# raws = """2333133121414131402"""

def proc(x):
    mmap = []
    pos = 0
    free = True
    for i,sz in enumerate(lmap(int, x)):
        if free:
            mmap.append([i//2, sz])
            pos += sz
            free = False

        else:
            mmap.append([-1, sz])
            pos += sz
            free = True

    # free = False
    # for i,sz in enumerate(lmap(int, x)):
    #     if free:
    #         mmap.extend([-1 for _ in range(sz)])
    #         free = False
    #     else:
    #         mmap.extend([i//2 for _ in range(sz)])
    #         free = True


    return mmap

inpt = proc(raws)
# print(inpt)

def f1(li):
    n = len(li)
    i = 0
    ri = n - 1
    pos = 0

    outs = 0
    while i<=ri:
        # print(pos, outs, i, ri)
        if li[i][0] >= 0:
            outs += sum((li[i][0] * k for k in range(pos, pos + li[i][1])))
            pos += li[i][1]

        
        else:
            while li[i][1] > 0:
                if li[ri][0] == -1 or li[ri][1] == 0:
                    ri -= 1
                
                else:
                    val = li[ri][0]
                    li[ri][1] -= 1
                    li[i][1] -= 1

                    outs += val * pos
                    pos += 1

        i += 1

    # print(li)
    return outs

def f2(li):
    n = len(li)

    bests = [[] for _ in range(9)]
    newdat = lambda sz, i: hq.heappush(bests[sz - 1], (0 - i))
    szind = lambda sz: [x for x in bests[:sz] if len(x) > 0]

    rightmost = lambda sz: (0 - hq.heappop(
                                            min(szind(sz))
                                            ))
    
    hasdat = lambda sz: len(szind(sz)) > 0

    for i, vals in enumerate(li):
        val, sz = vals

        if val != -1 and sz > 0:
            newdat(sz, i)

    outs = 0

    pos = 0
    shifted = set()
    for i,vals in enumerate(li):
        val, sz = vals

        # print("\n\n------------")
        # print(outs, pos, i, val, sz)
        # print(bests)
        # print(shifted)

        if (i not in shifted) and val != -1:
            outs += sum((val * k for k in range(pos, pos + sz)))
        else:
            while sz > 0 and hasdat(sz):
                dat = rightmost(sz)

                if dat > i:
                    dval, dsz = li[dat]

                    outs += sum((dval * k for k in range(pos, pos + dsz)))
                    shifted.add(dat)
                    
                    sz -= dsz
                    pos += dsz

                # print(sz)

        pos += sz

    return outs


# print("Part 1: ", f1(inpt))
print("Part 2: ", f2(inpt))

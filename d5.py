from collections import defaultdict as ddict, Counter as count
from functools import reduce,  cmp_to_key, partial as par
from math import prod, sqrt as root, lcm as lcm, gcd as gcd
from operator import itemgetter as ig
from re import findall as rall

import math
import re

from aoc import *

file = open("d5.txt")
raws = file.read()
file.close()

ras = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""

raws = lmap(lambda x: x.splitlines(), raws.split('\n\n'))

def proc(x):
    return lmap(int, x.split('|'))

def proc2(x):
    return lmap(int, x.split(','))


inpt = lmap(proc, raws[0]), lmap(proc2, raws[1])

ordering = ddict(lambda: set())

def upstream(k):
    done = set()
    tbd = ordering[k]

    while tbd:
        nx = {y for x in tbd
              if x in ordering
              for y in ordering[x]}
        
        done |= tbd
        tbd = nx - done

    return done 

def f1(ru, ins):
    for b,a in ru:
        ordering[a].add(b)
    
    # tfw poor reading comprehension
    # fullorder = ddict(lambda: set())
    # fullorder.update({x:upstream(x) for x in ordering})

    outs1 = outs2 = 0
    for row in ins:
        n = len(row)
        if all((b not in ordering[a] 
                for i, a in enumerate(row) 
                for b in row[i + 1:])):
            outs1 += row[n//2]

        else:
            for i in range(n):
                for j in range(i, n):
                    if row[j] in ordering[row[i]]:
                        row[i], row[j] = row[j], row[i]

            outs2 += row[n//2]

            

    return outs1, outs2
    

def f2(ins):
    pass

print("Part 1: ", f1(*inpt))
print("Part 2: ", f2(inpt))

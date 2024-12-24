from collections import defaultdict as ddict, Counter as count
from functools import reduce,  cmp_to_key, partial as par
from math import prod, sqrt as root, lcm as lcm, gcd as gcd
from operator import itemgetter as ig
from re import findall as rall

import math
import re

from aoc import *

file = open("d15.txt")
raws = file.read()
file.close()

ras = """
"""

raws = raws.split('\n\n')

inpt = lmap(list, raws[0].splitlines())
mx, my = len(inpt), len(inpt[0])

bounded = lambda k: 0 <= k.real < mx and 0 <= k.imag < my
getval = lambda k: inpt[int(k.real)][int(k.imag)] if bounded(k) else 'L'

def findch(gch):
    for x, row in enumerate(inpt):
        for y, ch in enumerate(row):
            if ch == gch:
                return x + (y * (1j))

def write(k, ch):
    if bounded(k):
        inpt[int(k.real)][int(k.imag)] = ch
        return True
    
    return False

dirs = lambda ch: [(1j)**i for i in range(4)]['v>^<'.index(ch)]
movs = lmap(dirs, filter(
                        lambda ch: ch != '\n',
                        raws[1]
                        ))

def disp():
    for row in inpt:
        print("".join(row))

def score():
    outs = 0
    for x, row in enumerate(inpt):
        for y, ch in enumerate(row):
            if ch in ['O', '[']:
                outs += 100*x + y

    return outs

def push(cpos, mov):
    match getval(cpos):
        case 'O':
            return push(cpos + mov, mov)
        case '.':
            write(cpos, 'O')
            return True
        case '#':
            return False

def f1(movs):
    cpos = findch('@')
    write(cpos, '.')

    for mov in movs:
        match getval(cpos + mov):
            case '.':
                cpos += mov
            case 'O':
                if push(cpos + mov, mov):
                    cpos += mov
                    write(cpos, '.')

    return score()


makebig = lambda ch: lmap(list, ["##", "..", "[]", "@."])["#.O@".index(ch)]
makerowbig = lambda row: sum(map(makebig, row), [])

def shift(cpos, mov):
    write(cpos + mov, getval(cpos))
    write(cpos, '.')

def pushh(cpos, mov):
    match getval(cpos):
        case '[' | ']':
            if pushh(cpos + mov, mov):
                shift(cpos, mov)
                return True
        case '.':
            return True
        
    return False

def solidify(cposs):
    exc = set()

    for p in cposs:
        if getval(p) == '[':
            exc.add(p + 1j)
            exc.add(p)
        elif getval(p) == ']':
            exc.add(p - 1j)
            exc.add(p)

    return exc

def pushv(cposs, mov):
    cposs = solidify(cposs)
    nx = {p + mov for p in cposs}

    if any(getval(p) == '#' for p in nx):
        return False
    
    elif all(getval(p) == '.' for p in nx)\
        or pushv(nx, mov):
        for p in cposs:
            shift(p, mov)

        return True
    
    return False

def push2(cpos, mov):
    if mov.imag == 0 :
        return pushv([cpos], mov)
    else:
        return pushh(cpos, mov)


def f2(movs):
    global inpt, my

    inpt = lmap(makerowbig, 
                raws[0].splitlines())
    
    my = len(inpt[0])
    
    cpos = findch('@')
    write(cpos, '.')

    for mov in movs:
        match getval(cpos + mov):
            case '.':
                cpos += mov
            case '[' | ']':
                if push2(cpos + mov, mov):
                    cpos += mov

    return score()



print("Part 1: ", f1(movs))
print("Part 2: ", f2(movs))

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

raws = """##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^"""

raws = raws.split('\n\n')


#grid functions
inpt = lmap(list, raws[0].splitlines())
mx, my = len(inpt), len(inpt[0])

bounded = lambda k: 0 <= k.real < mx and 0 <= k.imag < my
getval = lambda k: inpt[int(k.real)][int(k.imag)] if bounded(k) else 'L'

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
    cpos = 0
    for x, row in enumerate(inpt):
        for y, ch in enumerate(row):
            if ch == '@':
                cpos += x + (y * (1j))
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

def pushh(cpos, mov):
    match getval(cpos):
        case '[':
            if pushh(cpos + mov, mov):
                write(cpos, ']')
                return True
        case ']':
            if pushh(cpos + mov, mov):
                write(cpos, '[')
                return True
        case '.':
            return True
        
    return False

def pushv(cpos, mov):
    match getval(cpos):
        case '[':
            rpos = cpos + 1j
            if pushv(cpos + mov, mov) and pushv(rpos + mov, mov):
                write(cpos + mov, '[')
                write(rpos + mov, ']')
                return True
        case ']':
            return pushv(cpos - 1j, mov)
        case '.':
            return True
        
    return False

def push2(cpos, mov):
    vert = mov.imag == 0
    
    if vert and pushv(cpos, mov):
        opos = cpos + (1j if getval(cpos) == '[' else -1j)
        write(cpos, '.')
        write(opos, '.')
        return True

    elif (not vert) and pushh(cpos, mov):
        write(cpos, '.')
        return True
    
    return False


def f2(movs):
    global inpt, my

    inpt = lmap(makerowbig, 
                raws[0].splitlines())
    my = len(inpt[0])
    
    cpos = 0
    for x, row in enumerate(inpt):
        for y, ch in enumerate(row):
            if ch == '@':
                cpos += x + (y * (1j))
                inpt[int(cpos.real)][int(cpos.imag)] = '.'

    for row in inpt:
        print("".join(row))

    for mov in movs:
        match getval(cpos + mov):
            case '.':
                cpos += mov
            case '[' | ']':
                if push2(cpos + mov, mov):
                    cpos += mov

    for row in inpt:
        print("".join(row))

    return score()



print("Part 1: ", f1(movs))
print("Part 2: ", f2(movs))

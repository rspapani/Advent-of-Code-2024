from collections import defaultdict as ddict, Counter as count
from functools import reduce,  cmp_to_key, partial as par
from math import prod, sqrt as root, lcm as lcm, gcd as gcd
from operator import itemgetter as ig
from re import findall as rall

import math
import re

from aoc import *

file = open("d24.txt")
raws = file.read().split('\n\n')
file.close()

rws = """
""".split('\n\n')

vals = {x[:3]:int(x[-1]) for x in raws[0].splitlines()}
gates = {}

funcs = {
    'AND': lambda a,b: a & b,
    'OR': lambda a,b: a|b,
    'XOR': lambda a,b: a^b
}

fors = {}

def proc2(x):
    a, f, b, _, o  = x.split()
    gates[o] = (f, a, b)
    fors[(f, a, b)] = o

lmap(proc2, raws[1].splitlines())

def evalg(g):
    if g not in vals:
        f, a, b = gates[g]
        vals[g] = funcs[f](evalg(a), evalg(b))

    return vals[g]

def f1():
    outs = []
    for g in gates:
        if g[0] == 'z':
            outs.append((g, evalg(g)))

    k = [str(x[1]) for x in  sorted(outs)][::-1]
    print(len(k))
    return "".join(k)

def trace(g):
    if g in gates:
        f, a, b = gates[g]
        return f"({g} = {trace(a)} {f} {trace(b)})"
    else:
        return f"({g} = {vals[g]})"
    
# def orcheck(g):
#     return []

# def faultfind(g):
#     f, a, b = gates[g]

#     if f != 'XOR':
#         return [g]
    
#     else:
#         outs = []
#         for x in (a, b):
#             if x not in vals:
#                 fx, ax, bx = gates[x]
#                 if fx == 'XOR':
#                     if ax[0] not in ['x', 'y']:
#                         outs.append(x)

#                 elif fx == 'OR':
#                     outs.extend(orcheck(x))

#                 else:
#                     outs.append(x)

#         return outs


A = 'AND'
O = 'OR'
X = 'XOR'

def f2():
    outs = []

    def forw(i, cin):
        print(i, set(outs))
        k = str(100+i)[1:]
        x = f'x{k}'
        y = f'y{k}'
        z = f'z{k}'

        if (A, x, y) in fors:
            axy = fors[(A, x, y)]

        elif (A, y, x) in fors:
            axy = fors[(A, y, x)]

        if (X, x, y) in fors:
            xxy = fors[(X, x, y)]

        elif (X, y, x) in fors:
            xxy = fors[(X, y, x)]


        if (X, axy, cin) in fors:
            xou = fors[(X, axy, cin)]

        elif (X, axy, cin) in fors:
            xou = fors[(X, axy, cin)]

        else:
            for g in gates:
                if (X, g, cin) in fors:
                    xou = fors[(X, g, cin)]
                    outs.append(axy)

                elif (X, cin, g) in fors:
                    xou = fors[(X, cin, g)]
                    outs.append(axy)

                elif (X, g, axy) in fors:
                    xou = fors[(X, g, axy)]
                    outs.append(cin)

                elif (X, axy, g) in fors:
                    xou = fors[(X, axy, g)]
                    outs.append(cin)

        if (A, axy, cin) in fors:
            axou = fors[(A, axy, cin)]

        elif (A, axy, cin) in fors:
            axou = fors[(A, axy, cin)]

        else:
            for g in gates:
                if (A, g, cin) in fors:
                    axou = fors[(A, g, cin)]
                    outs.append(axy)

                elif (A, cin, g) in fors:
                    axou = fors[(A, cin, g)]
                    outs.append(axy)

                elif (A, g, axy) in fors:
                    axou = fors[(A, g, axy)]
                    outs.append(cin)

                elif (A, axy, g) in fors:
                    axou = fors[(A, axy, g)]
                    outs.append(cin)

        try:
            if (O, axou, axy) in fors:
                cout = fors[(O, axou, axy)]

            elif (O, axy, axou) in fors:
                cout = fors[(O, axy, axou)]

            else:
                for g in gates:
                    if (O, axou, g) in fors:
                        cout = fors[(O, axou, g)]
                        outs.append(axy)

                    elif (O, g, axou) in fors:
                        cout = fors[(O, g, axou)]
                        outs.append(axy)

                    elif (O, g, axy) in fors:
                        cout = fors[(O, g, axy)]
                        outs.append(axou)

                    elif (O, axy, g) in fors:
                        cout = fors[(O, axy, g)]
                        outs.append(axou)
        except:
            print("we tried")
            return "aaa"

        return cout
    
    try:
        cin = 'rfg'
        for i in range(1, 45):
            cin = forw(i, cin)

    except:
        print("we tried!")

    print(outs)

    outs = []
    for i in range(45):
        k = str(100+i)[1:]
        outs.extend(faultfind(f"z{k}"))

    outs = set(outs)

    outs = set()
    xorins = set()
    orins = set()
    for row in raws[1].splitlines():
        a, f, b, _, o  = row.split()
        if f == 'XOR':
            xorins.add(a)
            xorins.add(b)
            if a[0] in ['x', 'y'] or o[0] == 'z':
                pass
            else:
                print("i", row)
                outs.add(o)

        elif o[0] == 'z':
            print("o", row)
            outs.add(o)





    print("ORS")
    for row in raws[1].splitlines():
        a, f, b, _, o  = row.split()
        if f == 'OR':
            orins.add(a)
            orins.add(b)
            if o not in xorins:
                print(row)
                outs.add(o)

    
    print("ANDS")
    for row in raws[1].splitlines():
        a, f, b, _, o  = row.split()
        if f == 'AND':
            if o not in orins:
                print(row)
                outs.add(o)

    

    
    print(",".join(sorted(list(outs))))

    



# for i in range(46):
#     k = str(100+i)[1:]
#     # print(k, trace(f"z{k}"))
#     print(gates[f"z{k}"])

# xs = []
# ys = []

# for i in range(46):
#     k = str(100+i)[1:]
#     x = f"x{k}"
#     y = f"y{k}"

#     if x in vals:
#         xs.append(str(vals[x]))
#     if y in vals:
#         ys.append(str(vals[y]))

print("Part 1: ", f1())
print("Part 2: ", f2())

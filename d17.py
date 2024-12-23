from collections import defaultdict as ddict, Counter as count
from functools import reduce,  cmp_to_key, partial as par
from math import prod, sqrt as root, lcm as lcm, gcd as gcd
from operator import itemgetter as ig
from re import findall as rall

import math
import re

from aoc import *

# file = open("d0.txt")
# raws = file.read().splitlines()
# file.close()

rws = """
""".splitlines()

class intcode():
    def comb(self, op):
        match op:
            case 4:
                return self.A
            case 5:
                return self.B
            case 6:
                return self.comb
            case _:
                return op

    def dv(self, op, sve=0):
        res = self.A//(2**self.comb(op))
        match sve:
            case 1:
                self.A = res
            case 2:
                self.B = res
            case 3:
                self.C = res

    def bxl(self, op):
        self.B = self.B^op

    def bst(self, op):
        self.B = self.comb(op)%8

    def jnz(self, op):
        if self.A:
            self.ip = op - 2

    def bxc(self, op):
        self.B = self.B ^ self.C

    def out(self, op):
        if self.loud:
            print(op, self.comb(op)%8)

        self.outs.append(self.comb(op)%8)

    def adv(self, op):
        self.dv(op, 1)
    
    def bdv(self, op):
        self.dv(op, 2)
    
    def cdv(self, op):
        self.dv(op, 3)

    def __str__(self):
        return ",".join(map(str, self.outs))

    def __init__(self, A, B, C, ops=[], loud=False):
        self.ins = {
            0: self.adv,
            1: self.bxl,
            2: self.bst,
            3: self.jnz,
            4: self.bxc,
            5: self.out,
            6: self.bdv,
            7: self.cdv
        }

        self.outs = []

        self.A = A
        self.B = B
        self.C = C

        self.loud = loud
        

        if len(ops) > 0:
            self.exec(ops)

    def exec(self, ops):
        n = len(ops)
        self.ip = 0

        while self.ip < n:
            op, inp = ops[self.ip], ops[self.ip + 1]
            if self.loud:
                print(self.ip, op, inp, self.A, self.B, self.C)
            self.ins[op](inp)

            self.ip += 2 


# def proc(x):
#     pass

# inpt = lmap(proc, raws)
inpt = []

def f1(li):
    X = intcode(A=46337277, B=0, C=0)
    X.exec([2,4,1,1,7,5,4,4,1,4,0,3,5,5,3,0])
    return str(X)

def f2(li):
    for i in range(8**7):
        X = intcode(A= i, B=0, C=0, loud = False)
        X.exec([2,4,1,1,7,5,4,4,1,4,0,3,5,5,3,0])
        if '2,4,1' in str(X):
            print(i, i//8, i%8, str(X))

    n = len([2,4,1,1,7,5,4,4,1,4,0,3,5,5,3,0])
    X = intcode(A=(8**(n - 1)) + 7 + 24, B=0, C=0)
    X.exec([2,4,1,1,7,5,4,4,1,4,0,3,5,5,3,0])
    return str(X)

print("Part 1: ", f1(inpt))
print("Part 2: ", f2(inpt))

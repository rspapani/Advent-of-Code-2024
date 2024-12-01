#why yes I am aware of numpy

import re
import math
from math import prod
from functools import reduce
from collections.abc import Iterable, Sequence

### PARSING

getints = lambda x: lmap(lambda y: int(y.group()), re.finditer('(-?\d+)', x))

### CONSTANTS:
isdig = lambda x: x in '0123456789'
ldigs = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
digits = {**{dig: str(i) for i,dig in enumerate(ldigs)},
          **{i: i for i in '0123456789'}}


### FUNCTIONS:
lmap = lambda f, li: [f(x) for x in li]
lzip = lambda *li: list(zip(*li))

def index(*li):
    def get(itm):
        return reduce(lambda x, y: x[y], li, itm)
    
    return get

#def lcm(*args):
    #lc = lambda a, b: (a*b)//math.gcd(a,b)
    #return reduce(lc, args, 1)

def egcd(a, b):
    if a >= b:
        xp, yp = 1, 0
        x, y = 0, 1

    else:
        a, b = b, a
        xp, yp = 0, 1
        x, y = 1, 0

    while b:
        d, b, a = a//b, a%b, b
        xp, yp, x, y = x, y, xp - (d*x), yp - (d*y)

    return a, xp, yp

#Individual CRT
def chnrem(p1, p2):
    a1, n1 = p1
    a2, n2 = p2
    g, m1, m2 = egcd(n1, n2)

    if (a1%g) != (a2%g):
        # no solution
        return 0, 0

    cb = math.lcm(n1,n2)

    return ((a2*m1*n1 + a1*m2*n2)//g)%cb, cb


#Chinese Remainder Theorem

def crt(*pairs):
    return reduce(chnrem, pairs)


def zipm(f, *v):
    return [f(z) for z in zip(*v)]

# Interval intersection
# returns c, left remainder of a, right remainder of a
# the format for an interval is [x, y), where x,y are integers

def intsec(a, b):
    sa, ea = a
    sb, eb = b

    ls, le = 0, 0
    rs, re = 0, 0

    sc = max(sa, sb)
    ec = min(ea, eb)

    if sc >= ec:
        return ((0,0), a, (0,0))

    if sc != sa:
        ls, le = sa, sc - 1
        
    if ec != ea:
        rs, rb = ec, ea

    return ((sc, ec), (ls, le), (rs, re))


### MODULAR ARITHMETIC

#Computes sum_{i = 0}^{n - 1} {a * (r^i)} (mod m)

#a = first term
#r = common ratio
#n = number of terms
#m = modulo m
def powmodseries(a, r, n, m):
    binoms = [(1 + pow(r, 2**i, m)) for i in range(int(math.log2(n)))]
    outs = 0
    
    xcof = 0
    
    def twopow(xcof, n2):
        return reduce(lambda x, y: (x * y)%m, binoms[:n2], pow(r, xcof ,m))

    while n > 0:
        npow = int(math.log2(n))       
        outs = (outs + twopow(xcof, npow))%m

        n = n - (2**npow)     
        xcof += 2**npow      

    return (a * outs)%m


### VECTORS:
class vec(tuple):
    def __add__(self, v2):
        if v2 != 0:
            return vec(zipm(sum, self, v2))
        else:
            return self
        
    __radd__ = __add__

    def __sub__(self, v2):
        if v2:
            return self + (-1 * vec(v2))
        else:
            return self
        
    def __rsub__(self, v2):
        if v2:
            return (-1 * self) + v2
        else:
            return self

    def __mul__(self, val):
        return vec([a*val for a in self])

    __rmul__ = __mul__
    
    def __truediv__(self, val):
        return self * (1/val)

    def __floordiv__(self, val):
        return vec((int(i) for i in self/val))

    #v1 < v2 iff v1 fits within the bounding box of v2

    def __lt__(self, v2):
        return all(zipm(lambda x: x[0] < x[1], self, v2))

    def __le__(self, v2):
        return all(zipm(lambda x: x[0] <= x[1], self, v2))

    def __gt__(self, v2):
        return all(zipm(lambda x: x[0] > x[1], self, v2))

    def __ge__(self, v2):
        return all(zipm(lambda x: x[0] >= x[1], self, v2))
    
    def vmul(self, v2):
        return vec(zipm(prod, self, v2))

    def ip(self, v2):
        return sum(self.vmul(v2))

    def norm(self):
        return math.sqrt(self.ip(self))
    
    def t(self):
        return mat(([x] for x in self), clean=True, fast=True)

    def m(self):
        return mat([self], clean=True, fast=True)

    def map(self, f):
        return vec((f(x) for x in vec))

    def vert(self):
        return '\n'.join(('|' + str(row[0]) + '|' for row in self.t()))

    def rev(self):
        return vec(self[::-1])

class mat(Sequence):
    def __init__(self, args, clean = True, fast = True):
        self.m = 0
        self.fast = fast
        
        cols = []

        if not clean:
            for col in args:
                cols.append(list(col))
                self.m = max(self.m, len(cols[-1]))

            for col in cols:
                col.extend((self.m - len(col)) * [0])

            cols = map(vec, cols)
            

        else:
            for col in args:
                cols.append(vec(col))
                self.m = max(self.m, len(cols[-1]))

        self.cols = tuple(cols)
        self.n = len(self.cols)

        super().__init__()

    def __getitem__(self, i):
        return self.cols[i]

    def __len__(self):
        return self.n

    def t(self):
        return mat([[self[i][j] for i in range(self.n)] for j in range(self.m)],
                   clean=self.fast, fast=self.fast)
    
    def __add__(self, m2):
        if m2 == 0:
            return self
        else:
            return mat(zipm(sum, self, m2),
                       clean=self.fast, fast=self.fast)


    __radd__ = __add__

    def __sub__(self, m2):
        if m2:
            return self + (-1 * mat(m2))
        else:
            return self

    def __rsub__(self, m2):
        return (-1 * self) + m2

    def __mul__(self, m2):
        if m2 == 0:
            return 0
        
        elif m2 == 1:
            return self        
        
        elif isinstance(m2, mat):
            return mat([self * v for v in m2],
                       clean=self.fast, fast=self.fast)
                        
        elif isinstance(m2, Iterable):
            return sum(zipm(prod, self, m2))
        
        else:
            return mat([m2 * c for c in self],
                       clean=self.fast, fast=self.fast)

    def __rmul__(self, m2):
        if m2 == 0:
            return 0
        
        elif m2 == 1:
            return self
        
        elif isinstance(m2, mat):
            return mat([m2 * v for v in self],
                       clean=self.fast, fast=self.fast)
        
        else:
            return mat([m2 * c for c in self],
                       clean=self.fast, fast=self.fast)

    def __repr__(self):
        return '\n'.join(('|' + str(row)[1:-1] + '|' for row in self.t()))



def principle_evec(matrix, strt=[], thres = 0.000000001):
    x = strt if strt else [1] * matrix.n
    xk = matrix * x
    xk = 1/xk.norm() * xk


    while (x - xk).norm() >= thres:
        xprv = x
        x = xk
        xk = matrix * x
        xk = 1/xk.norm() * xk

        if xk == xprv:
            return vec([0] * matrix.n)
        
    #print(x, xk)

    return xk

#principle eigenvalue
def principle_eval(m, pvec):
    return pvec.t() * m * pvec

def principle_pair(matrix):
    pvec = principle_evec(matrix)
    pval = principle_eval(matrix, pvec)[0]

    return pvec, pval

def symmetric_eigenpairs(matrix, n = 0):
    if not n:
        n = matrix.n

    outs = []

    for _ in range(n):
        pvec, pval = principle_pair(matrix)
        outs.append((pvec, pval))
        print(pvec.vert(), pval)
        matrix = matrix - (pval * pvec.m() * pvec.t())

    return outs


def ads(n):
    base = [0 for _ in range(n)]

    for i in range(n):
        base[i] = 1
        yield vec(base)
        base[i] = -1
        yield vec(base)
        base[i] = 0

#All Adjacent coordinates of a vector
adjs = lambda k: map(lambda x: k + x, ads(len(k)))








if __name__ == "__main__":
    # Correct Output is:
    
    # ([0.8943821770509506, -0.447303612073055], 2.0006000201288243)
    matr2 = mat([[1.603, -0.795], [-0.795, 0.411]])
    print(principle_pair(matr2))
    
    # [([0.4472135956679416, 0.894427190915924], 7.0),
    # ([0.8944271907059447, -0.4472135960879008], 2.000000000000001)]
    matr1 = mat([[3, 2], [2, 6]])
    print(symmetric_eigenpairs(matr1))

    # [([0.21848174521148284, 0.5216089742445763, 0.8247362032776697],
    #    7.16227766016838),
    #  ([0.8863402621256237, 0.24750234598689216, -0.39133557015183945],
    #    0.8377223398316206),
    #  ([0, 0, 0], 0.0)]
    matr3 = mat([[1, 1, 1], [1, 2, 3], [1, 3, 5]])
    print(symmetric_eigenpairs(matr3))

    print("----------------------------------------")
    print("----------------------------------------")
    print("----------------------------------------")


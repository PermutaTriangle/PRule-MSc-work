import json
from permuta import *
import itertools
from math import factorial
import functools

def load_set(filename):
    patts = []
    with open(filename,'r') as f:
        for line in f.readlines():
            obj = json.loads(line)
            pattern = MeshPattern(Permutation(obj["perm"]),map(tuple,obj["mesh"]))
            patts.append(pattern)
    return patts

class MyCounter(object):
    """Class to keep track of containment"""
    def __init__(self):
        self.length = 0
        self.value = 0

    def __add__(self, other):
        if isinstance(other, bool):
            self.value = self.value + (int(other)<<self.length)
            self.length += 1
        else:
            raise NotImplementedError("MyCounter is only used to track booleans")

    def __eq__(self,other):
        if isinstance(other, MyCounter):
            assert len(self) == len(other)
            return self.value == other.value
        else:
            raise NotImplementedError()

    def __len__(self):
        return self.length

    def __xor__(self,other):
        if isinstance(other, MyCounter):
            assert len(self) == len(other)
            return self.value ^ other.value
        else:
            raise NotImplementedError()

    def __repr__(self):
        return format(self.value, '#0%db' % (self.length+2))[2:]

    def __str__(self):
        return format(self.value, '#0%db' % (self.length+2))[2:]

def get_representatives(classes):
    return [clas[0] for clas in classes]

def get_coincidences(representatives, length, perm):
    counters = [MyCounter() for representative in representatives]

    for permlength in range(1,length+1):
        for p in AvoidanceClass(permlength,perm):
            for i,v in enumerate(representatives):
                counters[i] + p.avoids(v)

    coinc = [(p1,p2) for p1,p2 in itertools.combinations(enumerate(counters),2) if p1[1] == p2[1]]

    return coinc

def get_all_coincidences(representatives, length):
    counters = [MyCounter() for representative in representatives]

    for p in Permutations(length):
        for i,v in enumerate(representatives):
            counters[i] + p.avoids(v)

    coinc = [(p1,p2) for p1,p2 in itertools.combinations(enumerate(counters),2) if p1[1] == p2[1]]

    return coinc


def coincidences_to_dictionary(coincidences):
    coincdict = {}
    for c1,c2 in coincidences:
        coincdict[c1[0]] = coincdict.get(c1[0],[]) + [c2[0]]

    coincdict_clean = {}
    for k in coincdict:
        if not any(k in p for p in coincdict_clean.values()):
            coincdict_clean[k] = coincdict[k]
    return {k:[k]+v for k,v in coincdict_clean.iteritems()}

def printclass(x,classlist):
    for p in classlist[x]:
        print str(p) + "\n"

def mpdict(classes):
    mpdict = {}
    for i,classi in enumerate(classes):
        for patt in classi:
            mpdict[patt] = i
    return mpdict

def countclasses(coincidict):
    return 220 - sum(map(len,coincidict.values())) + len(coincidict)

def catalan(n):
    return factorial(2*n)/(factorial(n+1)*factorial(n))

def partition(perm):
    last = 0
    currblock = -1
    partition = []
    for value in perm:
        if value > last:
            partition.append([])
            currblock += 1
        partition[currblock].append(value)
        last = value
    return partition

def meshpatt_to_tex(mp):
    cj = ",".join
    stm = functools.partial(map,str)
    pstr = cj(stm(mp.perm))
    mstr = cj("/".join(stm(pair)) for pair in mp.mesh)
    outstr = "\\textpattern{{}}{{{}}}{{{}}}".format(pstr, mstr)
    return outstr

def pad_sequence(length, seq):
    seql = list(seq)
    while len(seql) < length:
        seql.append(0)
    return tuple(seql)

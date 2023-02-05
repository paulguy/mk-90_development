#!/usr/bin/env python

import array
import itertools
import random
from enum import Enum

class BlockType(Enum):
    Nothing = 0
    Air = 1
    Land = 2
    Water = 3

class PMod(Enum):
    Disallow = 0
    AddOne = 1
    Double = 2
    NoChange = 3

probabilities = {
    # north, south, west, east order
    # Nothing - equal chance of anything, except water
    BlockType.Nothing: ((PMod.AddOne, PMod.AddOne, PMod.NoChange),
                        (PMod.AddOne, PMod.AddOne, PMod.NoChange),
                        (PMod.AddOne, PMod.AddOne, PMod.NoChange),
                        (PMod.AddOne, PMod.AddOne, PMod.NoChange)),
    # Air - More chance to produce more air, but might make land
    # No floating water
    BlockType.Air: ((PMod.Double, PMod.AddOne, PMod.Disallow),
                    (PMod.Double, PMod.AddOne, PMod.NoChange),
                    (PMod.Double, PMod.NoChange, PMod.Disallow),
                    (PMod.Double, PMod.NoChange, PMod.Disallow)),
    # Land - More chance to produce more land, but might make air
    # more chance to make air above than below
    # tries to embed water
    BlockType.Land: ((PMod.Double, PMod.NoChange, PMod.NoChange),
                     (PMod.AddOne, PMod.AddOne, PMod.NoChange),
                     (PMod.AddOne, PMod.Double, PMod.AddOne),
                     (PMod.AddOne, PMod.Double, PMod.AddOne)),
    # Water - Only embed in land
    BlockType.Water: ((PMod.AddOne, PMod.Disallow, PMod.Double),
                      (PMod.Disallow, PMod.AddOne, PMod.Double),
                      (PMod.Disallow, PMod.AddOne, PMod.Double),
                      (PMod.Disallow, PMod.AddOne, PMod.Double))
}

WIDTH = 9
CONTWIDTH = 40
HEIGHT = 12

levelMap = array.array('h', itertools.repeat(BlockType.Nothing.value, WIDTH*HEIGHT))
levelMapL = array.array('h', itertools.repeat(BlockType.Nothing.value, CONTWIDTH*HEIGHT))
levelMapR = array.array('h', itertools.repeat(BlockType.Nothing.value, CONTWIDTH*HEIGHT))

def getMap(data, x, y, w):
    return data[w*y+x]

def setMap(data, x, y, w, val):
    data[w*y+x] = val

def gen(data, x, y, w):
    vals = [0, 0, 0]
    double = [1, 1, 1]
    neighbors = [probabilities[BlockType.Nothing][0],
                 probabilities[BlockType.Nothing][1],
                 probabilities[BlockType.Nothing][2],
                 probabilities[BlockType.Nothing][3]]
    # get the probabilities for the direction looking towards this map cell
    if y + 1 < HEIGHT:
        # south neighbor will want the north probabilities
        neighbors[0] = probabilities[BlockType(getMap(data, x, y + 1, w))][0]
    if y - 1 >= 0:
        # north will want south
        neighbors[1] = probabilities[BlockType(getMap(data, x, y - 1, w))][1]
    if x + 1 < WIDTH:
        # east will want west
        neighbors[2] = probabilities[BlockType(getMap(data, x + 1, y, w))][2]
    if x - 1 >= 0:
        # west will want east
        neighbors[3] = probabilities[BlockType(getMap(data, x - 1, y, w))][3]
    for neigh in neighbors:
        for num, pmod in enumerate(neigh):
            if vals[num] < 0:
                continue
            if pmod == PMod.Disallow:
                vals[num] = -1
            elif pmod == PMod.AddOne:
                vals[num] += 1
            elif pmod == PMod.Double:
                double[num] *= 2
    for n, d in enumerate(double):
        if vals[n] < 0:
            vals[n] = 0
            continue
        else:
            vals[n] += 1
        vals[n] *= d
    for n in range(len(vals)-1):
        vals[n+1] += vals[n]
    if vals[-1] == 0:
        raise ValueError("No candidates!")
    spin = random.randint(1, vals[-1])
    for n in range(len(vals)):
        if n == 0 and \
           spin > 0 and spin <= vals[0]:
            return BlockType(1)
        elif spin > vals[n-1] and spin <= vals[n]:
            return BlockType(n+1)

def genUp(data, x, y, w):
    for my in range(y, -1, -1):
        setMap(data, x, my, w, gen(data, x, my, w).value)

def genDown(data, x, y, w):
    for my in range(y, HEIGHT):
        setMap(data, x, my, w, gen(data, x, my, w).value)

def genLeft(data, x, w):
    for mx in range(x, -1, -1):
        my = random.randint(1, HEIGHT-2)
        setMap(data, mx, my, w, gen(data, mx, my, w).value)
        genUp(data, mx, my-1, w)
        genDown(data, mx, my+1, w)

def genRight(data, x, w):
    for mx in range(x, w):
        my = random.randint(1, HEIGHT-2)
        setMap(data, mx, my, w, gen(data, mx, my, w).value)
        genUp(data, mx, my-1, w)
        genDown(data, mx, my+1, w)

# put a platform for the player
setMap(levelMap, WIDTH//2, HEIGHT-3, WIDTH, BlockType.Land.value)
setMap(levelMap, WIDTH//2, HEIGHT-4, WIDTH, BlockType.Air.value)

random.seed()

genUp(levelMap, WIDTH//2, HEIGHT-5, WIDTH)
genDown(levelMap, WIDTH//2, HEIGHT-2, WIDTH)
genLeft(levelMap, WIDTH//2-1, WIDTH)
genRight(levelMap, WIDTH//2+1, WIDTH)

for y in range(HEIGHT):
    levelMapL[y*CONTWIDTH-1] = levelMap[(y-1)*WIDTH]
    levelMapR[(y-1)*CONTWIDTH] = levelMap[y*WIDTH-1]

genLeft(levelMapL, CONTWIDTH-2, CONTWIDTH)
genRight(levelMapR, 1, CONTWIDTH)

for y in range(HEIGHT):
    for x in range(CONTWIDTH):
        print(levelMapL[y*CONTWIDTH+x], end='')
    print(end=' ')
    for x in range(WIDTH):
        print(levelMap[y*WIDTH+x], end='')
    print(end=' ')
    for x in range(CONTWIDTH):
        print(levelMapR[y*CONTWIDTH+x], end='')
    print()

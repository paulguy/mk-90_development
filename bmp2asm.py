#!/usr/bin/env python

import sys
from sdl2 import SDL_LoadBMP, SDL_LockSurface
import ctypes
import copy

ITEMS_PER_LINE = 6

def load_bmp(fname):
    bmp_p = SDL_LoadBMP(fname.encode('utf-8'))
    SDL_LockSurface(bmp_p)
    bmp = bmp_p.contents
    return bmp.w, bmp.h, copy.copy(ctypes.string_at(bmp.pixels, bmp.w * bmp.h))

width, height, pixels = load_bmp(sys.argv[1])
if width != 64 and height != 96:
    raise ValueError("Width must be 64 and height must be 96.")

lineItem = ITEMS_PER_LINE
print("    .word ", end='')

for y in range(width//2):
    for x in range(0, height, 8):
        gfxdata = \
            pixels[((x+8)*width-1)-y] << 0 | \
            pixels[((x+7)*width-1)-y] << 1 | \
            pixels[((x+6)*width-1)-y] << 2 | \
            pixels[((x+5)*width-1)-y] << 3 | \
            pixels[((x+4)*width-1)-y] << 4 | \
            pixels[((x+3)*width-1)-y] << 5 | \
            pixels[((x+2)*width-1)-y] << 6 | \
            pixels[((x+1)*width-1)-y] << 7 | \
            pixels[((x+8)*width-1-(width//2))-y] << 8 | \
            pixels[((x+7)*width-1-(width//2))-y] << 9 | \
            pixels[((x+6)*width-1-(width//2))-y] << 10 | \
            pixels[((x+5)*width-1-(width//2))-y] << 11 | \
            pixels[((x+4)*width-1-(width//2))-y] << 12 | \
            pixels[((x+3)*width-1-(width//2))-y] << 13 | \
            pixels[((x+2)*width-1-(width//2))-y] << 14 | \
            pixels[((x+1)*width-1-(width//2))-y] << 15

        print("^D{}".format(gfxdata), end='')
        lineItem -= 1
        if lineItem == 0:
            lineItem = ITEMS_PER_LINE
            print()
            print("    .word ", end='')
        else:
            print(", ", end='')

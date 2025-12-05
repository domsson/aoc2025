#!/usr/bin/env python3

#
# day 4 - part 1
#

import os
import sys
import time
import argparse

cfg_anykey_before_abort = (os.name == 'nt')

def abort(message, code=0, anykey=False):
    print(message)
    if anykey:
        input("Press any key to end")
    sys.exit(code)

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input",  help="Input file", default="", required=True)
args = parser.parse_args()

filename = args.input

if not os.path.isfile(filename):
    abort("Not a file: " + filename, 0, cfg_anykey_before_abort)

#
# timing
#

t0 = time.perf_counter_ns()

#
# start of solution
#

with open(filename) as file:
    lines = [line.rstrip() for line in file]

# TODO
width = len(lines[0])
height = len(lines)

print(f"width: {width}, height: {height}")

def count_adjacent(lines, w, h, x, y):
    count = 0
    #top
    if y > 0:
        if lines[y-1][x] == '@':
            count += 1
        # top left
        if x > 0:
            if lines[y-1][x-1] == '@':
                count += 1
        # top right
        if x < (width-1):
            if lines[y-1][x+1] == '@':
                count += 1
    # bottom
    if y < (height-1):
        if lines[y+1][x] == '@':
            count += 1
        # bottom left
        if x > 0:
            if lines[y+1][x-1] == '@':
                count += 1
        # bottom right
        if x < (width-1):
            if lines[y+1][x+1] == '@':
                count += 1
    # left
    if x > 0:
        if lines[y][x-1] == '@':
            count += 1
    # right
    if x < (width-1):
        if lines[y][x+1] == '@':
            count += 1
    return count

rolls = 0

for y, line in enumerate(lines):
    for x, c in enumerate(line):
        if c == '@':
            adjacent = count_adjacent(lines, width, height, x, y)
            if y == 0:
                print(f"x={x}: {adjacent}")
            if adjacent < 4:
                rolls += 1

print(f"Accessible rolls: {rolls}")

#
# end of solution
#

t1 = time.perf_counter_ns()
nanos = t1 - t0
millis = nanos / 1_000_000

print("Runtime: " + str(millis) + " ms (" + str(nanos) + " ns)")

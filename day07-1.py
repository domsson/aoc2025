#!/usr/bin/env python3

#
# day 7 - part 1;
#

import os
import sys
import time
import math
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
    lines = [line for line in file]

#
# DATA SIZE
#

width = len(lines[0])
height = len(lines)

print(f"data size: {width} x {height}")

#
# FIND ORIGIN, BUILD INT DATA
#

data = [[0] * width for _ in range(height)]

#origin = { "x": 0, "y": 0 }
for y, line in enumerate(lines):
    for x, c in enumerate(line):
        if c == '.':
            data[y][x] = 0
            continue
        if c == 'S':
            data[y][x] = 1
            continue
        if c == '^':
            data[y][x] = 2
            continue
 #          origin["x"] = x
 #          origin["y"] = y

#print(f"origin: {origin["x"]}, {origin["y"]}")

#
# TRACE BEAM
#

split_count = 0

for y, line in enumerate(data):
    for x, c in enumerate(line):
        split = False
        if c == 0 and y > 0 and data[y-1][x] == 1: # empty with beam above
            data[y][x] = 1 # turn to beam
        if c == 2 and y > 0 and data[y-1][x] == 1: # splitter with beam above
            if x > 0 and data[y][x-1] < 2:
                data[y][x-1] = 1
                split = True
            if x < width-1 and data[y][x+1] < 2:
                data[y][x+1] = 1
                split = True
        split_count += int(split)

print(f"split count: {split_count}")

#
# end of solution
#

t1 = time.perf_counter_ns()
nanos = t1 - t0
millis = nanos / 1_000_000

print("Runtime: " + str(millis) + " ms (" + str(nanos) + " ns)")


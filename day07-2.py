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

for y, line in enumerate(lines):
    for x, c in enumerate(line):
        if c == '.':
            data[y][x] = 0
            continue
        if c == 'S':
            data[y][x] = 1
            continue
        if c == '^':
            data[y][x] = -1
            continue

#
# TRACE BEAM
#

def print_line(line):
    line_str = ""
    for c in line:
        if c == 0:
            line_str += '.'
            continue
        if c == 1:
            line_str += '|'
            continue
        if c > 1:
            line_str += 'I'
            continue
        if c < 0:
            line_str += '^'
            continue
    print(line_str)

def count_beams(line):
    total = 0
    for c in line:
        if c >= 0:
            total += c
    return total


#split_count = 0

for y, line in enumerate(data):
    if y == height-1:
        break
    for x, c in enumerate(line):
        below = data[y+1][x]
        if c > 0: # beam
            if below >= 0: # empty or beam below
                data[y+1][x] += c
                continue
            if below == -1: # splitter
                if x > 0:
                    data[y+1][x-1] += c
                if x < width-1:
                    data[y+1][x+1] += c
                continue
    print_line(data[y])

print(data[height-1])
#print(f"split count: {split_count}")

timelines = sum([n for n in data[height-1]])
print(f"timelines: {timelines}")

#
# end of solution
#

t1 = time.perf_counter_ns()
nanos = t1 - t0
millis = nanos / 1_000_000

print("Runtime: " + str(millis) + " ms (" + str(nanos) + " ns)")


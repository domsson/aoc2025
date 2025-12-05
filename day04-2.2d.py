#!/usr/bin/env python3

#
# day 4 - part 2
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

width = len(lines[0])
height = len(lines)

print(f"width: {width}, height: {height}")


def prep_data(lines, width, height):
    new_w = width + 2
    new_h = height + 2

    new_data = [[0 for _ in range(new_w)] for _ in range(new_h)]

    for y in range(1, new_h-1):
        for x in range(1, new_w-1):
            if lines[y-1][x-1] == '@':
                new_data[y][x] = 1 

    return new_data, new_w, new_h


def nuke_data(data, width, height):
    new_data = [row[:] for row in data]
    nuked = 0

    for y in range(1, height-1):

        row_top = data[y-1]
        row_mid = data[y]
        row_bot = data[y+1]

        for x in range(1, width-1):

            if row_mid[x] == 0:
                continue

            adjacent = \
                row_top[x-1] + row_top[x] + row_top[x+1] + \
                row_mid[x-1] +              row_mid[x+1] + \
                row_bot[x-1] + row_bot[x] + row_bot[x+1]

            if adjacent < 4:
                new_data[y][x] = 0
                nuked += 1

    return [new_data, nuked]


data, width, height = prep_data(lines, width, height)

nuked_total = 0
nuked = 1
i = 0
while (nuked):
    data, nuked = nuke_data(data, width, height)
    nuked_total += nuked
    i += 1

print(f"removed a total of {nuked_total} rolls in {i} iterations")

#
# end of solution
#

t1 = time.perf_counter_ns()
nanos = t1 - t0
millis = nanos / 1_000_000

print("Runtime: " + str(millis) + " ms (" + str(nanos) + " ns)")


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

    new_data = [0] * (new_w * new_h)

    for y in range(1, new_h-1):
        for x in range(1, new_w-1):
            if lines[y-1][x-1] == '@':
                new_data[y * new_w + x] = 1

    return new_data


def nuke_data(data, width, height, off):
    new_data = data[:] 
    nuked = 0

    for y in range(1, height-1):

        row = y * width

        for x in range(1, width-1):

            idx = row + x

            if data[idx] == 0:
                continue

            adjacent = \
                data[idx + off[0]] + data[idx + off[1]] + data[idx + off[2]] + \
                data[idx + off[3]]                      + data[idx + off[4]] + \
                data[idx + off[5]] + data[idx + off[6]] + data[idx + off[7]]

            if adjacent < 4:
                new_data[idx] = 0
                nuked += 1

    return [new_data, nuked]

data = prep_data(lines, width, height)

width  += 2
height += 2

kernel = [-width-1, -width, -width+1,
                -1,               +1,
           width-1,  width,  width+1]

removed = 0
rc = 1
i = 0
while (rc):
    data, rc = nuke_data(data, width, height, kernel)
    removed += rc
    i += 1

print(f"removed a total of {removed} rolls in {i} iterations")

#
# end of solution
#

t1 = time.perf_counter_ns()
nanos = t1 - t0
millis = nanos / 1_000_000

print("Runtime: " + str(millis) + " ms (" + str(nanos) + " ns)")


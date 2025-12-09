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

nums = []
ops = []

for y, line in enumerate(lines): 
    if y == height-1:
        ops = line.split()
    else:
        nums.append([int(n) for n in line.split()])
        #print(nums[y])

totals = [0] * len(ops)
for x, o in enumerate(ops):
    if o == '*':
        totals[x] = 1


for y, row in enumerate(nums):
    for x, n in enumerate(row):
        if ops[x] == '+':
            totals[x] += n
            continue
        if ops[x] == '*':
            totals[x] *= n
            continue

print(totals)

total = 0
for n in totals:
    total += n

print(f"total = {total}")

#
# end of solution
#

t1 = time.perf_counter_ns()
nanos = t1 - t0
millis = nanos / 1_000_000

print("Runtime: " + str(millis) + " ms (" + str(nanos) + " ns)")


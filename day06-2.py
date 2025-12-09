#!/usr/bin/env python3

#
# day 4 - part 2
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
# EXTRACT OPERATORS
#
# for each set, is it '+' or '*'?
# we convert '*' to 1 and '+' to 0 as it simplifies things
#

last_line = lines.pop()
ops = [1 if c=='*' else 0 for c in last_line.split()]

#
# FIGURE OUT LONGEST LINE (DATA WIDTH)
#
# this will later determine the number of rows in the transposed data
# let's also get the number of rows (minus the last) while we're at it
#

width = max([len(line) for line in lines])
height = len(lines)
print(f"data size: {height} rows, {width} columns")

#
# TRANSPOSE THE DATA
#
# this will give us one number (as string) per line
# sets will be separated by an empty line
#

data = ["" * height for _ in range(width)]

for line in lines:
    for x, c in enumerate(line):
        data[x] += c

#
# PREPARE RESULTS PER SETS
#
# init to 1 for '*' sets, 0 for '+' sets
# which means we can just simply copy the `ops` array
#

set_totals = ops[:]

#
# ACTUALLY SUM/MULTIPLY EACH SET
#
# keep track of where we are by increasing the set index for each empty line we see
#

cur_set = 0
for row in data:
    if row.isspace():
        cur_set += 1
        continue

    if ops[cur_set]:
        set_totals[cur_set] *= int(row)
    else:
        set_totals[cur_set] += int(row)

#
# SUM IT ALL UP
#
# thanks, python, for making this stupidly simple 
#

grand_total = sum(set_totals)
print(f"grand_total: {grand_total}")

#
# end of solution
#

t1 = time.perf_counter_ns()
nanos = t1 - t0
millis = nanos / 1_000_000

print("Runtime: " + str(millis) + " ms (" + str(nanos) + " ns)")


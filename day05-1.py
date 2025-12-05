#!/usr/bin/env python3

#
# day 5 - part 1
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
    lines = [line.rstrip() for line in file]

# TODO

ranges = []
items = []

reading_ranges = True
overall_low = math.inf
overall_high = -1

for line in lines:
    if not line.strip():
        reading_ranges = False
        continue

    if reading_ranges:
        low_str, high_str = line.strip().split('-')
        low = int(low_str)
        high = int(high_str)
        ranges.append([low, high])
        if low < overall_low:
            overall_low = low
        if high > overall_high:
            overall_high = high
        
    else:
        item = line.strip()
        items.append(int(item))

fresh_items = set()

for item in items:
    for r in ranges:
        if item >= r[0] and item <= r[1]:
            fresh_items.add(item)

print(len(fresh_items))

#
# find smallest valid ID, largest valid ID, then count gaps in ranges you moron
#

valids = set()

num_ranges_before = len(ranges)

def merge_ranges(r1, r2):
    '''
    # r2 contained within r1
    if (r1[0] <= r2[0] and r1[1] >= r2[1]):
        return [r1[0], r1[1]]

    # r1 contained within r2
    if (r2[0] <= r1[0] and r2[1] >= r1[1]):
        return [r2[0], r2[1]]

    # r1's end goes into r2's start
    if r2[0] <= r1[1] and r2[1] >= r1[1]:
        return [r1[0], r2[1]]

    # r2's end goes into r1's start
    if r1[0] <= r2[1] and r1[1] >= r2[1]:
        return [r2[0], r1[1]]
    '''

    # this is slower, but so much cleaner - covers all cases
    if max(r1[0], r2[0]) <= min(r1[1], r2[1]):
        return [min(r1[0], r2[0]), max(r1[1], r2[1])]

    return False

def nuke_a_range(ranges):
    for i, r in enumerate(ranges):
        for j, s in enumerate(ranges):
            if j == i:
                continue
            merged = merge_ranges(r, s)
            if merged:
                return [merged, i, j]
    return [None, -1, -1]

'''
def mutate_ranges(ranges, delidx1, delidx2, new_item):
    new_ranges = []
    for i, r in enumerate(ranges):
        if i == delidx1 or i == delidx2:
            continue
        new_ranges.append(r)
    new_ranges.append(new_item)
    return new_ranges
'''


nuke = True
rounds = 0
while (nuke):
    merged, i, j = nuke_a_range(ranges)
    if merged:
        ranges = mutate_ranges(ranges, i, j, merged)
        nuke = True
    else:
        nuke = False
    rounds += 1

num_ranges_after = len(ranges)

ranges.sort(key=lambda tup: tup[0])  # sorts in place

valid_items_total = 0
for r in ranges:
    valid_items_total += (r[1] - r[0] + 1)

for r in ranges:
    n = r[1] - r[0] + 1
    print(f"{r} => {n}")

print(f"low  = {overall_low}")
print(f"high = {overall_high}")
print(f"did {rounds} rounds of range merging")
print(f"number of ranges before vs after: {num_ranges_before} -> {num_ranges_after}")
print(f"valid_items_total = {valid_items_total}")

#
# end of solution
#

t1 = time.perf_counter_ns()
nanos = t1 - t0
millis = nanos / 1_000_000

print("Runtime: " + str(millis) + " ms (" + str(nanos) + " ns)")

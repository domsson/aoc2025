#!/usr/bin/env python3

#
# day 10 - part 1
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


def parse_bits(lstr):
    layout = ""
    for c in lstr[1:-1]:
        layout += '0' if c=='.' else '1'
    bits = int(layout, 2)
    length = len(layout)
    return [bits, length]


def parse_masks(btns, field_len):
    data = []
    for btn_str in btns:
        btn = parse_mask(btn_str, field_len)
        data.append(btn)
    return data


def parse_mask(btn_str, field_len):
    meat = btn_str[1:-1]
    nums = [int(c) for c in meat.split(',')]
    mask = 0
    for num in nums:
        mask |= 1 << ((field_len - 1) - num)
    return mask


def apply_mask(bits, mask):
    return bits ^ mask


def find_combo(machine):
    target = machine["bits"]
    masks  = machine["masks"]

    actions = []
    # TODO



def fuckyou(target, bits, mask):
    return (apply_mask(bits, mask) == target)
        

data = []

for line in lines:
    line_data = {"bits": 0, "length": 0, "masks": []}

    tokens = line.split()

    # take the front off
    bits, length = parse_bits(tokens.pop(0))
    line_data["bits"]   = bits
    line_data["length"] = length

    # take the rear off
    joltages = tokens.pop()

    # take the in-between
    masks = parse_masks(tokens, length)
    line_data["masks"] = masks

    data.append(line_data)

for d in data:
    print(d)


for machine in data:
    path = find_combo(machine)
    print(path)


#
# observations:
# 
#  = never need to push the same button twice in a row, as it simply undoes the previous change
#  - however, if any other button has been pressed in between, then we need to try the previous button again
#


#
# end of solution
#

t1 = time.perf_counter_ns()
nanos = t1 - t0
millis = nanos / 1_000_000

print("Runtime: " + str(millis) + " ms (" + str(nanos) + " ns)")

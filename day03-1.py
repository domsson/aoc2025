#!/usr/bin/env python3

#
# day 3 - part 1
#

import os
import sys
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

with open(filename) as file:
    lines = [line.rstrip() for line in file]


total_joltage = 0

linenum = 0
for line in lines:
    linenum = linenum+1
    
    left_n  = 0
    left_i  = -1
    right_n = 0
    right_i = -1

    linelen = len(line)
    i = 0
    for c in line[:-1]:
        n = int(c)
        if n > left_n:
            left_n = n
            left_i = i
        i = i + 1

    for c in line[(left_i+1):]:
        n = int(c)
        if n > right_n:
            right_n = n
            right_i = i
        i = i + 1

    bank_joltage = int(str(left_n) + str(right_n))

    if linenum == 1:
        print(str(bank_joltage))
    total_joltage = total_joltage + bank_joltage

print("Total Joltage: " + str(total_joltage))

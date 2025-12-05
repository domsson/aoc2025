#!/usr/bin/env python3

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

current = 50
limit = 99
match = 0
match_count = 0

for i in lines:
    direction = -1 if (i[0] == 'L') else 1
    distance = int(i[1:])

    current = (current + (distance * direction)) % (limit + 1)
    if current == match:
        match_count = match_count + 1

print("Got to zero a total of " + str(match_count) + " times")

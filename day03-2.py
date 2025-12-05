#!/usr/bin/env python3

#
# day 3 - part 2
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
# start of solution
#

t0 = time.perf_counter()

with open(filename) as file:
    lines = [line.rstrip() for line in file]

def which_number_fucks(bank):
    fucker_n = 0
    fucker_i = 0

    for i, c in enumerate(bank):
        n = int(c)
        if n > fucker_n:
            fucker_n = n
            fucker_i = i

    return [fucker_n, fucker_i]


total_joltage = 0

for line in lines:
    index_used = 0
    bank_joltage = ""

    for d in range(12):
        bank = ""
        save = d - 11
        if save == 0:
            bank = line[index_used:]
        else:
            bank = line[index_used:save]
        
        fucker_n, fucker_i = which_number_fucks(bank)
        index_used += fucker_i + 1
        bank_joltage += str(fucker_n) 

    total_joltage += int(bank_joltage)

#
# end of solution
#

t1 = time.perf_counter()
millis = (t1-t0)*1000

print("Total Joltage: " + str(total_joltage))
print("Runtime: " + str(millis) + "ms")

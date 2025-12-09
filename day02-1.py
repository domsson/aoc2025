#!/usr/bin/env python3

import os
import sys
import argparse

#
# boilerplate
#

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
# solution
#

def is_tuple(s):
    s_len = len(s)
    if s_len % 2 > 0:
        return False
    half = int(s_len * 0.5)
    a = s[:half]
    b = s[half:]
    if a == b:
        return True
    return False

def is_tuples(s):
    s_len = len(s)
    half = int(s_len * 0.5)
    for n in range(1, half+1, 1):
        #print(" => " + s + " for stride " + str(n))
        fucks = str_fucks(s, s_len, n)
        if fucks:
            return True
    return False

def str_fucks(s, s_len, stride):
    if s_len % stride > 0:
        return False
    first = s[:stride]
    gonts = int(s_len / stride)
    for g in range(1, gonts):
        start = stride * g
        end = start + stride
        ficker = s[start:end]
        #print(first + " vs " + ficker + " (stride=" + str(stride) + ", g=" + str(g) + ")")
        if first != ficker:
            return False
    return True


with open(filename, 'r') as file:
    data = file.read().rstrip()

ranges = data.split(',')
invalid_id_sum = 0

for r in ranges:
    print("Working " + r + "...")
    limits = r.split('-')
    low = int(limits[0])
    high = int(limits[1])

    for n in range(low, high+1, 1):
        n_str = str(n) 
        #print(" -> " + n_str + " (" + str(n_len) + ")")
        #tuples = is_tuple(n_str)
        tuples = is_tuples(n_str)
        if tuples:
            print(" => " + n_str)
            invalid_id_sum = invalid_id_sum + n

print(str(invalid_id_sum))

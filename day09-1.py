#!/usr/bin/env python3

#
# day 4 - part 1
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

verts = []

for line in lines:
    coords = line.split(',')
    vert = tuple((int(coords[0]), int(coords[1])))
    verts.append(vert)

#print(verts)
num_verts = len(verts)

def area(p, q):
    return (abs(p[0]-q[0])+1) * (abs(p[1]-q[1])+1)

distances = []

for i in range(num_verts):
    for j in range(i+1, num_verts):
        a = area(verts[i], verts[j])
        t = tuple((verts[i], verts[j]))
        distances.append([a, t])

distances.sort(key=lambda x: x[0], reverse=True)

#for d in distances:
#    print(d)

print(distances[0])


# TODO


#
# end of solution
#

t1 = time.perf_counter_ns()
nanos = t1 - t0
millis = nanos / 1_000_000

print("Runtime: " + str(millis) + " ms (" + str(nanos) + " ns)")

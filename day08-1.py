#!/usr/bin/env python3

#
# day 8 - part 1
#

import os
import sys
import time
import argparse
import math

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


data = []

for line in lines:
    vert = [int(n) for n in line.split(',')]
    data.append(vert)

data_len = len(data)
print(f"data_len = {data_len}")
#print(data)

def dist3d(p, q):
    return math.pow(p[0] - q[0], 2) + math.pow(p[1] - q[1], 2) + math.pow(p[2] - q[2], 2)

def smallest_from(distances):
    shortest_dist = math.inf
    shortest_i = -1
    shortest_j = -1
    for i, row in enumerate(distances):
        for j, dist in enumerate(row):
            if dist > 0.0 and dist < shortest_dist:
                shortest_dist = dist
                shortest_i = i
                shortest_j = j
    return [shortest_i, shortest_j, shortest_dist]

distances = []

for i in range(data_len):
    box_i = data[i]
    for j in range(i+1, data_len):
        box_j = data[j]
        dist = int(dist3d(box_i, box_j))
        pair = [i, j]
        distances.append([dist, pair])

circuits = [[n] for n in range(data_len)]

distances.sort(key=lambda x: x[0])

'''
for d in distances:
    print(d)
'''

def find_in_circuits(circuits, box_idx):
    for i, circuit in enumerate(circuits):
        if box_idx in circuit:
            return i

def merge_circuits(circuits, i, j):
    circuits[i] += circuits[j]
    del circuits[j] #circuits[j].clear()

for n in range(1000):
    dist, boxes = distances.pop(0)
    i = find_in_circuits(circuits, boxes[0])
    j = find_in_circuits(circuits, boxes[1])
    if i == j:
        continue
    else:
        merge_circuits(circuits, i, j)

print(circuits)

lengths = [len(circuit) for circuit in circuits]
print(lengths)

lengths.sort(reverse=True)
print(lengths)

total = 1
for n in range(3):
    total *= lengths[n]

print(total)


'''
for d in distances:
    print(d)
'''



#
# end of solution
#

t1 = time.perf_counter_ns()
nanos = t1 - t0
millis = nanos / 1_000_000

print("Runtime: " + str(millis) + " ms (" + str(nanos) + " ns)")

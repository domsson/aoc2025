#!/usr/bin/env python3

#
# day 8 - part 2
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

data = []

with open(filename) as file:
    for line in file:
        data.append(tuple((int(n) for n in line.split(','))))

data_len = len(data)
print(f"data_len: {data_len}")

def dist3d(p, q):
    return math.pow(p[0]-q[0], 2) + math.pow(p[1]-q[1], 2) + math.pow(p[2]-q[2], 2)

distances = []

for i in range(data_len):
    box_i = data[i]
    for j in range(i+1, data_len):
        box_j = data[j]
        dist = int(dist3d(box_i, box_j))
        pair = [i, j]
        #pair = tuple((i, j))
        distances.append([dist, pair])

circuits = [[n] for n in range(data_len)]

distances.sort(key=lambda x: x[0])

def find_in_circuits(circuits, box_idx):
    for i, circuit in enumerate(circuits):
        if box_idx in circuit:
            return i

def merge_circuits(circuits, i, j):
    circuits[i] += circuits[j]
    del circuits[j]

last_boxes = [-1, -1]

while(len(distances)):
    dist, boxes = distances.pop(0)
    i = find_in_circuits(circuits, boxes[0])
    j = find_in_circuits(circuits, boxes[1])
    if i == j:
        continue
    else:
        merge_circuits(circuits, i, j)
        last_boxes = boxes[:]


box_a = data[last_boxes[0]]
box_b = data[last_boxes[1]]
print(f"number circuits left: {len(circuits)}")
print(f"last boxes connected: {last_boxes[0]} and {last_boxes[1]} ({box_a}, {box_b})")

result = box_a[0] * box_b[0]
print(f"result: {result}")

#
# end of solution
#

t1 = time.perf_counter_ns()
nanos = t1 - t0
millis = nanos / 1_000_000

print("Runtime: " + str(millis) + " ms (" + str(nanos) + " ns)")

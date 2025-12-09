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


# circle is being drawn counter-clockwise, starting right-hand side, about middle

def area(p, q):
    return (abs(p[0]-q[0])+1) * (abs(p[1]-q[1])+1)

def find_largest_area(verts):
    num_verts = len(verts)
    areas = []
    for i in range(num_verts):
        for j in range(i+1, num_verts):
            a = area(verts[i], verts[j])
            t = tuple((verts[i], verts[j]))
            areas.append([a, t])
    
    areas.sort(key=lambda x: x[0], reverse=True)
    return areas[0]


diameter = 100_000
radius = diameter * 0.5

verts = []
cutoffs = []
cutoff_verts = []

prev = None
for line in lines:
    coords = line.split(',')
    vert = tuple((int(coords[0]), int(coords[1])))
    verts.append(vert)
    if prev and abs(vert[0] - prev[0]) > radius:
        cutoffs.append(vert[1])
        cutoff_verts.append(prev)
        cutoff_verts.append(vert)
    prev = vert

print(f"cut-offs: {cutoff_verts}")

relevant_verts_top_right    = [] # y-value going up /
relevant_verts_top_left     = [] # y-value going down \
relevant_verts_bottom_left  = [] # y-value going down \
relevant_verts_bottom_right = [] # y-value going up /
relevant_range = radius * 0.66

for vert in verts:
    x = vert[0]
    y = vert[1]

    if y >= cutoffs[0]: # top half
        if y <= cutoffs[0] + relevant_range:
            if x > radius:
                relevant_verts_top_right.append(vert)
            else:
                relevant_verts_top_left.append(vert)
        continue
    if y <= cutoffs[1]: # bottom half
        if y >= cutoffs[1] - relevant_range:
            if x > radius:
                relevant_verts_bottom_right.append(vert)
            else:
                relevant_verts_bottom_left.append(vert)
        continue

print(f"relevant verts top right:    {len(relevant_verts_top_right)}")
print(f"relevant verts top left:     {len(relevant_verts_top_left)}")
print(f"relevant verts bottom left:  {len(relevant_verts_bottom_left)}")
print(f"relevant verts bottom right: {len(relevant_verts_bottom_right)}")


def find_largest_area_h(anchor, verts_left, verts_right): # this assumes anchor vert is on right-hand side
    biggest_area = [0, (0,0)]

    for v_left in verts_left:
        rect_viable = True
        top    = max(v_left[1], anchor[1])
        bottom = min(v_left[1], anchor[1])
        left   = v_left[0]
        right  = anchor[0]

        for v in verts_left:
            if v[1] > top:
                continue
            if v[1] < bottom:
                continue
            if v[0] > left:
                rect_viable = False
                continue
        for v in verts_right:
            if v[1] > top:
                continue
            if v[1] < bottom:
                continue
            if v[0] < right:
                rect_viable = False
                continue

        if rect_viable:
            a = area(v_left, anchor)
            t = tuple((v_left, anchor))
            if a > biggest_area[0]:
                biggest_area = [a, t]
    
    return biggest_area

def someone_below_blocks_left(candidate, others):
    for o in others:
        if o[1] >= candidate[1]:
            continue
        if o[0] > candidate[0]:
            return True
    return False

def someone_above_blocks_left(candidate, others):
    for o in others:
        if o[1] <= candidate[1]:
            continue
        if o[0] > candidate[0]:
            return True
    return False

def find_largest_fucker_fast_top(anchor, verts_left, verts_right):
    x = anchor[0]

    verts_right.sort(key=lambda x: x[1]) # y-value low to high - moving UP the circle
    limiting_vert_right = (0, 0)

    for v in verts_right:
        if v == anchor:
            continue
        if v[1] < anchor[1]:
            continue

        dist_x = v[0] - anchor[0]
        if dist_x < 0:
            break
        limiting_vert_right = v

    print(f"limiting vert right: {limiting_vert_right}")

    verts_left.sort(key=lambda x: x[1])
    best_candidate_left = (0, 0)
    largest_area = 0
    for v in verts_left:
        if v[1] < anchor[1]:
            continue
        if v[1] > limiting_vert_right[1]:
            continue
        v_area = area(anchor, v)
        if someone_below_blocks_left(v, verts_left):
            continue
        if v_area > largest_area:
            largest_area = v_area
            best_candidate_left = v

    print(f"best candidate left: {best_candidate_left}")
    print(f"area: {largest_area}")

def find_largest_fucker_fast_bottom(anchor, verts_left, verts_right):
    x = anchor[0]

    verts_right.sort(key=lambda x: x[1], reverse=True) # y-value high to low - moving DOWN the circle
    limiting_vert_right = (0, 0)

    for v in verts_right:
        if v == anchor:
            continue
        if v[1] > anchor[1]:
            continue

        dist_x = v[0] - anchor[0]
        if dist_x < 0:
            break
        limiting_vert_right = v

    print(f"limiting vert right: {limiting_vert_right}")

    verts_left.sort(key=lambda x: x[1], reverse=True)
    best_candidate_left = (0, 0)
    largest_area = 0
    for v in verts_left:
        if v[1] > anchor[1]:
            continue
        if v[1] < limiting_vert_right[1]:
            continue
        v_area = area(anchor, v)
        if someone_above_blocks_left(v, verts_left):
            continue
        if v_area > largest_area:
            largest_area = v_area
            best_candidate_left = v

    print(f"best candidate left: {best_candidate_left}")
    print(f"area: {largest_area}")



#biggest_area_top    = find_largest_area_h(cutoff_verts[1], relevant_verts_top_left, relevant_verts_top_right)
#biggest_area_bottom = find_largest_area_h(cutoff_verts[2], relevant_verts_bottom_left, relevant_verts_bottom_right)

biggest_area_top    = find_largest_fucker_fast_top(cutoff_verts[1],    relevant_verts_top_left,    relevant_verts_top_right)
biggest_area_bottom = find_largest_fucker_fast_bottom(cutoff_verts[2], relevant_verts_bottom_left, relevant_verts_bottom_right)

print(f"largest area top: {biggest_area_top}")
print(f"largest area bottom: {biggest_area_bottom}")

#largest = max(biggest_area_top, biggest_area_bottom)
#print(f"largest area overall: {largest}")


'''
path = "<path d=\""

for i, line in enumerate(lines):
    c = "L" if i > 0 else "M"
    coords = line.split(',')
    path += f"{c} {coords[0]} {coords[1]} "

path += "Z\" />"

print(path)
'''

#
# end of solution
#

t1 = time.perf_counter_ns()
nanos = t1 - t0
millis = nanos / 1_000_000

print("Runtime: " + str(millis) + " ms (" + str(nanos) + " ns)")

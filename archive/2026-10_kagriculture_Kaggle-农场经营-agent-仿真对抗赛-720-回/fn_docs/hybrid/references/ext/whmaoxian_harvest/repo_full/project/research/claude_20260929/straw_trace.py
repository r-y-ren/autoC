"""Trace strawberry/tomato production days: watered? fertilized? usage: straw_trace.py a.py b.py seed [crop]"""
import sys, collections
from dbg import run

crop = sys.argv[4] if len(sys.argv) > 4 else 'STRAWBERRY'
env = run(sys.argv[1], sys.argv[2], int(sys.argv[3]))
first, interval = {'STRAWBERRY': (10, 2), 'TOMATO': (8, 1)}[crop]
stat = collections.Counter()
lost = collections.Counter()
for t in range(len(env.steps)):
    o = env.steps[t][0].observation
    if o.hour != 23:
        continue
    f = o.farms[0]
    for y in range(10):
        for x in range(10):
            tl = f['tiles'][y][x]
            if not (isinstance(tl, dict) and tl.get('crop') == crop):
                continue
            k = o.day + 1 - tl['planted_day'] - first
            if k >= 0 and k % interval == 0 and k // interval + 1 <= 4:
                w = tl['watered_today']
                fe = tl['fertilized_until_day'] >= o.day
                stat[(w, fe)] += 1
                if tl['yield_units'] >= 3:
                    lost['near_cap'] += 1
print('production days (watered, fertilized):', dict(stat), 'yield>=3 at prod:', dict(lost))

"""Why do plants die? usage: deaths.py a.py b.py seed"""
import sys, collections
from dbg import run

env = run(sys.argv[1], sys.argv[2], int(sys.argv[3]))
c = collections.Counter()
ex = []
for t in range(len(env.steps) - 1):
    o = env.steps[t][0].observation
    n = env.steps[t + 1][0].observation
    for y in range(10):
        for x in range(10):
            a, b = o.farms[0]['tiles'][y][x], n.farms[0]['tiles'][y][x]
            if isinstance(a, dict) and a.get('kind') == 'PLANT' and isinstance(b, dict) and b.get('kind') == 'WEED':
                age = o.day - a['planted_day']
                if o.hour == 23 and not a['watered_today'] and a['consecutive_unwatered'] >= 1:
                    cause = 'unwatered'
                else:
                    cause = 'decay'
                c[(a['crop'], cause)] += 1
                if len(ex) < 12 and cause == 'unwatered':
                    ex.append((a['crop'], 'd', o.day, 'age', age, 'yield', a['yield_units'], (x, y)))
print(dict(c))
for e in ex:
    print(e)

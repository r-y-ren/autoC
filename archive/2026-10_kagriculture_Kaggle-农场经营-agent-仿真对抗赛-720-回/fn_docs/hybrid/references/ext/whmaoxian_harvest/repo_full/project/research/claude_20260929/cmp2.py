"""Run A vs B and B vs B on the same seed; print per-day seat-0 stats side by side.
usage: cmp2.py a.py b.py seed"""
import sys, collections
from dbg import run


def daily(env, seat=0):
    rows = {}
    hires = collections.Counter()
    for t, s in enumerate(env.steps):
        o = s[seat].observation
        f = o.farms[seat]
        if o.hour == 23:
            hires[o.day] = f['hires_today']
        if o.hour == 12:
            c = collections.Counter()
            for y in range(10):
                for x in range(10):
                    tt = f['tiles'][y][x]
                    if tt is None:
                        c['.'] += 1
                    elif tt == 'LOCKED':
                        pass
                    elif tt['kind'] == 'PLANT':
                        c[tt['crop'][:2]] += 1
                    elif tt['kind'] == 'WEED':
                        c['#'] += 1
                    elif tt.get('animal'):
                        c[tt['animal'][:2]] += 1
                    else:
                        c['o'] += 1
            rows[o.day] = (int(f['money']), dict(c))
    return rows, hires


if __name__ == '__main__':
    a, b, seed = sys.argv[1], sys.argv[2], int(sys.argv[3])
    ea = run(a, b, seed)
    eb = run(b, b, seed)
    ra, ha = daily(ea)
    rb, hb = daily(eb)
    for d in range(30):
        print(f"d{d:2d} A ${ra[d][0]:6d} h{ha[d]:2d} {ra[d][1]}")
        print(f"    B ${rb[d][0]:6d} h{hb[d]:2d} {rb[d][1]}")
    print('final A', ea.steps[-1][0].observation.farms[0]['money'], 'B', eb.steps[-1][0].observation.farms[0]['money'])

"""Average harvested units per HARVEST by crop/animal for seat 0, plus wasted yield.
usage: yields.py a.py b.py seed"""
import sys, collections
from dbg import run


def yields(env, seat=0):
    got = collections.defaultdict(list)
    for t in range(len(env.steps) - 1):
        o = env.steps[t][seat].observation
        f = o.farms[seat]
        act = env.steps[t + 1][seat].action or {}
        units = [tuple(f['farmer'])] + [tuple(h) for h in f['hands']]
        cmds = [act.get('farmer')] + list(act.get('hands') or [])
        for pos, c in zip(units, cmds):
            if c and c[0] == 'HARVEST':
                tile = f['tiles'][pos[1]][pos[0]]
                if isinstance(tile, dict) and tile.get('yield_units', 0) > 0:
                    k = tile.get('crop') or tile.get('animal')
                    age = o.day - tile.get('planted_day', tile.get('placed_day', 0))
                    got[k].append((tile['yield_units'], age))
    return got


if __name__ == '__main__':
    a, b, seed = sys.argv[1], sys.argv[2], int(sys.argv[3])
    for name, env in (('A', run(a, b, seed)), ('B', run(b, b, seed))):
        g = yields(env)
        print(name, {k: (len(v), round(sum(x for x, _ in v) / len(v), 2), sum(x for x, _ in v)) for k, v in sorted(g.items())})

"""Health report of seat-0 agent: escapes, dead plants, idle/move turns, unplaced animals.
usage: health.py cand.py opp.py seed"""
import sys, collections
from dbg import run


def report(env, seat=0, verbose=True):
    steps = env.steps
    esc = collections.Counter()
    dead = collections.Counter()
    ops = collections.Counter()
    unplaced_turns = 0
    for t in range(len(steps) - 1):
        o = steps[t][seat].observation
        f = o.farms[seat]
        n = steps[t + 1][seat].observation.farms[seat]
        for y in range(10):
            for x in range(10):
                a, b = f['tiles'][y][x], n['tiles'][y][x]
                if isinstance(a, dict) and a.get('animal') and not (isinstance(b, dict) and b.get('animal')):
                    esc[a['animal']] += 1
                if isinstance(a, dict) and a.get('kind') == 'PLANT' and isinstance(b, dict) and b.get('kind') == 'WEED':
                    if a.get('yield_units', 0) > 0 and o.hour == 23:
                        dead[a['crop']] += 1
        act = steps[t + 1][seat].action or {}
        for c in [act.get('farmer')] + list(act.get('hands') or []):
            if c:
                ops[c[0] if c[0] not in ('NORTH', 'SOUTH', 'EAST', 'WEST') else 'MOVE'] += 1
        unplaced_turns += sum(v for k, v in o.private['shed'].items() if k in ('COW', 'SHEEP', 'GOOSE'))
    fin = [steps[-1][i].observation.farms[i]['money'] for i in (0, 1)]
    if verbose:
        print('final', fin)
        print('escapes', dict(esc), 'dead plants', dict(dead), 'animal-turns in shed', unplaced_turns)
        tot = sum(ops.values())
        print('ops', tot, sorted(ops.items(), key=lambda x: -x[1]))
    return fin, esc, dead, ops


if __name__ == '__main__':
    env = run(sys.argv[1], sys.argv[2], int(sys.argv[3]))
    report(env)

"""When does R2 sell goods relative to the step they reach the shed?
usage: droplag.py cand.py opp.py seed"""
import sys, collections
from dbg import run

ADJ = {(4, 4), (5, 4), (4, 5), (5, 5)}
PREM = ('STRAWBERRY', 'MELON', 'MILK', 'WOOL', 'TOMATO', 'EGG', 'CARROT')

if __name__ == '__main__':
    env = run(sys.argv[1], sys.argv[2], int(sys.argv[3]))
    lag = collections.Counter()
    same = collections.Counter()
    for t in range(719):
        o = env.steps[t][0].observation
        act = env.steps[t + 1][0].action or {}
        f = o.farms[0]
        units = [tuple(f['farmer'])] + [tuple(h) for h in f['hands']]
        cmds = [act.get('farmer')] + list(act.get('hands') or [])
        invs = o.private['inventories']
        arrived = collections.Counter()
        for i, c in enumerate(cmds):
            if not c or i >= len(units) or units[i] not in ADJ or i >= len(invs):
                continue
            if c[0] == 'DROP':
                for k, v in invs[i].items():
                    if k in PREM and v:
                        arrived[k] += v
            elif c[0] == 'PLACE' and len(c) >= 2 and c[1] in PREM:
                arrived[c[1]] += int(c[2]) if len(c) > 2 else 1
        if not arrived:
            continue
        for k, v in arrived.items():
            # find first step >= t where a SELL of k is issued
            for d in range(0, 30):
                if t + d + 1 >= len(env.steps):
                    break
                a2 = env.steps[t + d + 1][0].action or {}
                if any(m and m[0] == 'SELL' and m[1] == k for m in (a2.get('market') or [])):
                    lag[(k, d)] += v
                    break
            else:
                lag[(k, 'none')] += v
    for k in PREM:
        row = {d: n for (kk, d), n in lag.items() if kk == k}
        print(k, dict(sorted(row.items(), key=lambda x: str(x[0]))))

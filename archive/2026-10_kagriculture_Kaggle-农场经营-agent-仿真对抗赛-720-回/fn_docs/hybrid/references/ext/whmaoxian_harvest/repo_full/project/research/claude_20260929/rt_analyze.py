"""Analyze forced-route sweep: per table-route group, which forced route wins most.
usage: rt_analyze.py [min_games]"""
import json, sys, collections

min_games = int(sys.argv[1]) if len(sys.argv) > 1 else 5
pairs = json.load(open('results/ep_pairs.json'))
eps = set(l.strip() for l in open('r42have.txt') if l.strip())
res = collections.defaultdict(dict)   # ep -> route -> margin
base = {}
for l in open('results/surrogate_fix.jsonl'):
    r = json.loads(l)
    if 'me' not in r or str(r['ep']) not in eps:
        continue
    c = r['cand']
    if '/rt/rt' in c:
        R = int(c.split('/rt/rt')[1].split('.py')[0])
        res[str(r['ep'])][R] = r['me'] - r['op']
    elif c == 'cand/h9.py':
        base[str(r['ep'])] = r['me'] - r['op']
routes = sorted({R for v in res.values() for R in v})
print('episodes with results', len(res), 'routes', len(routes))
# sanity: forced(table route) == baseline
bad = sum(1 for e, v in res.items() if pairs[e]['table'] in v and e in base and v[pairs[e]['table']] != base[e])
print('sanity mismatches (forced table route vs baseline):', bad)
# global: each route forced everywhere
print('\n== forced everywhere (186 games): wins, mean margin')
glob = []
for R in routes:
    m = [v[R] for v in res.values() if R in v]
    glob.append((sum(x > 0 for x in m), sum(m) / max(1, len(m)), R))
for w, mm, R in sorted(glob, reverse=True)[:12]:
    print(f'  route {R:4d}: W={w:3d} mean={mm:8.0f}')
print('  baseline h9: W=%d mean=%.0f' % (sum(x > 0 for x in base.values()), sum(base.values()) / max(1, len(base))))
# per table-route group
groups = collections.defaultdict(list)
for e in res:
    groups[pairs[e]['table']].append(e)
print('\n== per table-route group: baseline vs best alternatives')
plan = {}
for T, es in sorted(groups.items(), key=lambda x: -len(x[1])):
    if len(es) < min_games:
        continue
    bw = sum(base[e] > 0 for e in es if e in base)
    bm = sum(base.get(e, 0) for e in es) / len(es)
    cands = []
    for R in routes:
        m = [res[e][R] for e in es if R in res[e]]
        if len(m) < len(es):
            continue
        cands.append((sum(x > 0 for x in m), sum(m) / len(m), R))
    cands.sort(reverse=True)
    print(f'  table route {T:4d} (n={len(es):3d}): baseline W={bw:3d} mean={bm:7.0f} | best: ' +
          ', '.join(f'{R}:W{w}/{mm:.0f}' for w, mm, R in cands[:5]))
    if cands and cands[0][0] > bw:
        plan[T] = cands[0][2]
print('\nproposed remap (group -> route):', plan)
json.dump({str(k): v for k, v in plan.items()}, open('results/rt_plan.json', 'w'))

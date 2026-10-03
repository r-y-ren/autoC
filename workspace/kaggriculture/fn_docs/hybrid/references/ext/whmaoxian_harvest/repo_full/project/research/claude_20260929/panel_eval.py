"""Paired panel: each candidate vs each opponent on the same seeds, both seats.
usage: panel_eval.py seeds workers tag cand1.py [cand2.py ...]"""
import sys, json, os, collections
from concurrent.futures import ProcessPoolExecutor
import arena

OPPS = {
    'aurax': 'panel/aurax.py', 'fieldcraft': 'panel/fieldcraft.py', 'dmitrii': 'panel/dmitrii.py',
    'metav4': 'panel/metav4.py', 'pipe16': 'panel/pipe16.py', 'v10': 'panel/v10.py',
    'marketshock': '../v10_rebuild_20260926/continuation/marketshock_adapter.py',
    'structured': '../v10_rebuild_20260926/continuation/structured_adapter.py',
}

if __name__ == '__main__':
    seeds, workers, tag = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    cands = sys.argv[4:]
    jobs = [(c, o, s, seat) for c in cands for o in OPPS.values() for s in range(2000, 2000 + seeds) for seat in (0, 1)]
    with ProcessPoolExecutor(workers) as p:
        res = list(p.map(arena.run, jobs))
    os.makedirs('results', exist_ok=True)
    with open(f'results/panel_{tag}.jsonl', 'w') as f:
        for r in res:
            f.write(json.dumps(r) + '\n')
    inv = {v: k for k, v in OPPS.items()}
    tab = collections.defaultdict(lambda: [0, 0, 0, 0.0, 0])
    for r in res:
        if 'me' not in r:
            print('ERR', r.get('opp'), r.get('err', '')[-300:])
            continue
        k = (r['cand'], inv[r['opp']])
        d = r['me'] - r['op']
        tab[k][0] += d > 0
        tab[k][1] += d < 0
        tab[k][2] += d == 0
        tab[k][3] += d
        tab[k][4] += 1
    for c in cands:
        tot = [0, 0, 0]
        print('==', c)
        for o in OPPS:
            w, l, t, s, n = tab[(c, o)]
            tot[0] += w; tot[1] += l; tot[2] += t
            print(f'   {o:12s} W{w:3d} L{l:3d} T{t:3d} mean margin {s / max(1, n):8.0f}')
        print('   TOTAL', tot)

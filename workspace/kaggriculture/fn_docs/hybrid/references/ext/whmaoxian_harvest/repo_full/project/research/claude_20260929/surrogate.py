"""Replay online episodes with our seat replaced by a candidate; the opponent replays its recorded tape.
usage: surrogate.py team_name workers cand1.py [cand2.py ...] -- ep1 ep2 ...
Prints per episode: original (me, opp) and for each cand (me, opp)."""
import sys, os, io, json, gzip, contextlib


def load(eid):
    return json.loads(gzip.decompress(open(f'replays/{eid}.json.gz', 'rb').read()))


def job(args):
    cand, eid, team = args
    try:
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            from kaggle_environments import make
            from kaggle_environments.agent import get_last_callable
            g = load(eid)
            names = g['info']['TeamNames']
            me = names.index(team)
            op = 1 - me
            tape = [g['steps'][t + 1][op]['action'] for t in range(719)]

            def opp(obs, cfg=None):
                return tape[obs['step']]
            ent = get_last_callable(open(cand, encoding='utf-8').read(), path=os.path.abspath(cand))
            agents = [None, None]
            agents[me] = ent
            agents[op] = opp
            env = make('kaggriculture', configuration={'episodeSteps': 720}, debug=False)
            env.info['seed'] = g['info']['seed']
            if os.environ.get('FIXSHOPS'):
                import kaggle_environments.envs.kaggriculture.kaggriculture as K
                if not hasattr(K, '_orig_eod'):
                    K._orig_eod = K._end_of_day
                rec = [list(g['steps'][min(719, d * 24)][0]['observation']['town']['unlocked_shops']) for d in range(31)]
                def eod(state, env_, day, _rec=rec):
                    K._orig_eod(state, env_, day)
                    state[0].observation.town['unlocked_shops'] = list(_rec[min(30, day + 1)])
                K._end_of_day = eod
            env.run(agents)
            f = env.steps[-1]
            m = [f[i].observation.farms[i]['money'] for i in range(2)]
            orig = g['rewards']
        return dict(cand=cand, ep=eid, seat=me, me=m[me], op=m[op], ome=orig[me], oop=orig[op], fix=bool(os.environ.get('FIXSHOPS')), shops=list(f[0].observation.town['unlocked_shops']))
    except Exception:
        import traceback
        return dict(cand=cand, ep=eid, err=traceback.format_exc()[-600:])


if __name__ == '__main__':
    from concurrent.futures import ProcessPoolExecutor
    a = sys.argv[1:]
    k = a.index('--')
    team, workers, cands, eps = a[0], int(a[1]), a[2:k], [int(e) for e in a[k + 1:]]
    jobs = [(c, e, team) for e in eps for c in cands]
    with ProcessPoolExecutor(workers) as p:
        res = list(p.map(job, jobs))
    os.makedirs('results', exist_ok=True)
    with open('results/surrogate_fix.jsonl' if os.environ.get('FIXSHOPS') else 'results/surrogate.jsonl', 'a') as f:
        for r in res:
            f.write(json.dumps(r) + '\n')
    by = {}
    for r in res:
        if 'err' in r:
            print('ERR', r['cand'], r['ep'], r['err'])
            continue
        by.setdefault(r['ep'], {})[r['cand']] = r
    tot = {c: [0, 0, 0.0] for c in cands}
    tot['orig'] = [0, 0, 0.0]
    for e in eps:
        rr = by.get(e, {})
        if not rr:
            continue
        r0 = next(iter(rr.values()))
        line = f"{e} seat{r0['seat']} orig {r0['ome']:7.0f}-{r0['oop']:7.0f} ({r0['ome'] - r0['oop']:+6.0f})"
        tot['orig'][0] += r0['ome'] > r0['oop']; tot['orig'][1] += r0['ome'] < r0['oop']; tot['orig'][2] += r0['ome'] - r0['oop']
        for c in cands:
            if c in rr:
                r = rr[c]
                d = r['me'] - r['op']
                line += f" | {os.path.basename(c)[:10]} {r['me']:7.0f}-{r['op']:7.0f} ({d:+6.0f})"
                tot[c][0] += d > 0; tot[c][1] += d < 0; tot[c][2] += d
        print(line)
    for c, v in tot.items():
        print('TOTAL', c, 'W', v[0], 'L', v[1], 'sum margin', round(v[2]))

"""Surrogate vs strong teams: keep the named team's recorded tape, replace the OTHER seat with a candidate.
usage: surrogate2.py list.tsv workers tag cand1.py [cand2.py ...]
list.tsv lines: episode<TAB>keep_team_name[<TAB>score]"""
import sys, os, io, json, gzip, contextlib, collections


def load(eid):
    return json.loads(gzip.decompress(open(f'replays/{eid}.json.gz', 'rb').read()))


def job(args):
    cand, eid, keep = args
    try:
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            from kaggle_environments import make
            from kaggle_environments.agent import get_last_callable
            g = load(eid)
            names = g['info']['TeamNames']
            if keep not in names:
                return dict(cand=cand, ep=eid, err='keep team not in replay: ' + repr(names))
            op = names.index(keep)
            me = 1 - op
            tape = [g['steps'][t + 1][op]['action'] for t in range(719)]
            ent = get_last_callable(open(cand, encoding='utf-8').read(), path=os.path.abspath(cand))
            agents = [None, None]
            agents[me] = ent
            agents[op] = lambda obs, cfg=None: tape[obs['step']]
            env = make('kaggriculture', configuration={'episodeSteps': 720}, debug=False)
            env.info['seed'] = g['info']['seed']
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
        return dict(cand=cand, ep=eid, keep=keep, me=m[me], op=m[op], orig_keep=orig[op], orig_other=orig[me])
    except Exception:
        import traceback
        return dict(cand=cand, ep=eid, err=traceback.format_exc()[-400:])


if __name__ == '__main__':
    from concurrent.futures import ProcessPoolExecutor
    lst, workers, tag, cands = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4:]
    rows = [l.rstrip('\n').split('\t') for l in open(lst, encoding='utf-8') if l.strip()]
    rows = [(int(r[0]), r[1]) for r in rows if os.path.exists(f'replays/{r[0]}.json.gz')]
    jobs = [(c, e, k) for e, k in rows for c in cands]
    with ProcessPoolExecutor(workers) as p:
        res = list(p.map(job, jobs))
    with open(f'results/sur2_{tag}.jsonl', 'w') as f:
        for r in res:
            f.write(json.dumps(r) + '\n')
    tot = collections.defaultdict(lambda: [0, 0, 0.0, 0])
    errs = 0
    for r in res:
        if 'err' in r:
            errs += 1
            continue
        d = r['me'] - r['op']
        t = tot[r['cand']]
        t[0] += d > 0; t[1] += d < 0; t[2] += d; t[3] += 1
    for c in cands:
        w, l, s, n = tot[c]
        print(f'{c:28s} n={n:3d} W={w:3d} L={l:3d} mean margin={s / max(1, n):8.0f}')
    print('errors', errs)

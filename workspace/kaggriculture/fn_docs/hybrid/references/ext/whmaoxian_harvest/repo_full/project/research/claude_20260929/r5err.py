"""Error analysis: per-category transaction totals for both players when a candidate plays online episodes (surrogate).
usage: r4err.py cand.py team out.json ep1 ep2 ...
Writes {ep: {'me': {key: [n, $]}, 'op': {...}, 'money': [me, op], 'guard': [...]}}."""
import sys, os, io, json, contextlib, collections
from concurrent.futures import ProcessPoolExecutor


def job(args):
    cand, eid, keep = args
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        import resim as R
        from surrogate import load
        from kaggle_environments import make
        from kaggle_environments.agent import get_last_callable
        g = load(eid)
        op = g['info']['TeamNames'].index(keep); me = 1 - op
        tape = [g['steps'][t + 1][op]['action'] for t in range(719)]
        ent = get_last_callable(open(cand, encoding='utf-8').read(), path=os.path.abspath(cand))
        rep = ent.__globals__.get('_NGTX_REPORT')
        glog = []
        base = ent.__globals__.get('_ngtx_apply')
        if base is not None:
            def spy(obs, action, _b=base):
                out = _b(obs, action)
                if out is not action:
                    extra = [o for o in out['market'] if o not in (action.get('market') or [])]
                    glog.append((int(obs['step']), extra, dict(obs['market']['prices'])))
                return out
            ent.__globals__['_ngtx_apply'] = spy
        ag = [None, None]; ag[me] = ent; ag[op] = lambda o, c=None: tape[o['step']]
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
        R.LOG.clear()
        env.run(ag)
        agg = [collections.defaultdict(lambda: [0, 0.0]) for _ in range(2)]
        for f, opn, item, price in R.LOG:
            if f is None:
                continue
            k = opn + ':' + item
            agg[f][k][0] += 1; agg[f][k][1] += price
        m = [env.steps[-1][i].observation.farms[i]['money'] for i in range(2)]
        # animals fed/cared days at end of each day
        an = [collections.Counter(), collections.Counter()]
        for d in range(30):
            o = env.steps[d * 24 + 23][0].observation
            for p in range(2):
                for row in o.farms[p]['tiles']:
                    for t in row:
                        if isinstance(t, dict) and t.get('animal'):
                            an[p][t['animal'] + '_days'] += 1
                            an[p][t['animal'] + '_fed'] += bool(t.get('fed_today'))
    return eid, dict(me={k: v for k, v in agg[me].items()}, op={k: v for k, v in agg[op].items()},
                     money=[m[me], m[op]], guard=glog, an=[dict(an[me]), dict(an[op])], names=g['info']['TeamNames'], seat=me)


if __name__ == '__main__':
    cand, lst, out = sys.argv[1], sys.argv[2], sys.argv[3]
    rows = [l.rstrip('\n').split('\t') for l in open(lst, encoding='utf-8') if l.strip()]
    res = {}
    with ProcessPoolExecutor(30) as p:
        for eid, d in p.map(job, [(cand, int(r[0]), r[1]) for r in rows]):
            res[eid] = d
    json.dump(res, open(out, 'w'))
    print('saved', len(res))

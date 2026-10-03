"""Error analysis: per-category transaction totals for both players when a candidate plays online episodes (surrogate).
usage: r4err.py cand.py team out.json ep1 ep2 ...
Writes {ep: {'me': {key: [n, $]}, 'op': {...}, 'money': [me, op], 'guard': [...]}}."""
import sys, os, io, json, contextlib, collections
from concurrent.futures import ProcessPoolExecutor


def job(args):
    cand, eid, team = args
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        import resim as R
        from surrogate import load
        from kaggle_environments import make
        from kaggle_environments.agent import get_last_callable
        g = load(eid)
        me = g['info']['TeamNames'].index(team); op = 1 - me
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
    cand, team, out = sys.argv[1], sys.argv[2], sys.argv[3]
    eps = [int(e) for e in sys.argv[4:]]
    res = {}
    with ProcessPoolExecutor(30) as p:
        for eid, d in p.map(job, [(cand, e, team) for e in eps]):
            res[eid] = d
    json.dump(res, open(out, 'w'))
    print('saved', len(res))

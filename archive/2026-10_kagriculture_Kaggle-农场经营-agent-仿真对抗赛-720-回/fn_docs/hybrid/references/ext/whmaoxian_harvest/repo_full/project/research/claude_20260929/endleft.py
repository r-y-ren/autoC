"""What value is left unrealized at the end (shed, carried, tile yields) when a candidate plays online episodes.
usage: endleft.py cand.py team ep1 ep2 ..."""
import sys, os, io, json, gzip, contextlib, collections
from concurrent.futures import ProcessPoolExecutor
from surrogate import load


def job(args):
    cand, eid, team = args
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        from kaggle_environments import make
        from kaggle_environments.agent import get_last_callable
        g = load(eid)
        me = g['info']['TeamNames'].index(team); op = 1 - me
        tape = [g['steps'][t + 1][op]['action'] for t in range(719)]
        ent = get_last_callable(open(cand, encoding='utf-8').read(), path=os.path.abspath(cand))
        ag = [None, None]; ag[me] = ent; ag[op] = lambda o, c=None: tape[o['step']]
        env = make('kaggriculture', configuration={'episodeSteps': 720}, debug=False)
        env.info['seed'] = g['info']['seed']
        env.run(ag)
    out = {}
    for t in (695, 705, 712, 717, 719):
        o = env.steps[t][me].observation
        f = o.farms[me]
        prices = o.market['prices']
        shed = {k: v for k, v in o.private['shed'].items() if v}
        carried = collections.Counter()
        for inv in o.private['inventories']:
            for k, v in inv.items():
                carried[k] += v
        tiles = collections.Counter()
        for row in f['tiles']:
            for tl in row:
                if isinstance(tl, dict) and tl.get('yield_units'):
                    k = tl.get('animal') or tl.get('crop')
                    tiles[k] += tl['yield_units']
        out[t] = dict(shed=shed, carried=dict(carried), tiles=dict(tiles), prices={k: prices.get(k) for k in ('EGG', 'MILK', 'WOOL', 'STRAWBERRY', 'MELON', 'TOMATO', 'CARROT', 'WHEAT')})
    return eid, out


if __name__ == '__main__':
    cand, team, eps = sys.argv[1], sys.argv[2], [int(e) for e in sys.argv[3:]]
    with ProcessPoolExecutor(28) as p:
        for eid, out in p.map(job, [(cand, e, team) for e in eps]):
            print('EP', eid)
            for t, v in out.items():
                print('  t', t, v)

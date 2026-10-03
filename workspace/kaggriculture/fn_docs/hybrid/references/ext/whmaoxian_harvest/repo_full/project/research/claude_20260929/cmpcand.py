"""Transaction diff between two candidates on one online episode (surrogate).
usage: cmpcand.py candA.py candB.py team ep"""
import sys, os, io, contextlib, collections
import resim as R
from surrogate import load


def run(cand, eid, team):
    from kaggle_environments import make
    from kaggle_environments.agent import get_last_callable
    g = load(eid)
    me = g['info']['TeamNames'].index(team); op = 1 - me
    tape = [g['steps'][t + 1][op]['action'] for t in range(719)]
    with contextlib.redirect_stdout(io.StringIO()):
        ent = get_last_callable(open(cand, encoding='utf-8').read(), path=os.path.abspath(cand))
    ag = [None, None]; ag[me] = ent; ag[op] = lambda o, c=None: tape[o['step']]
    env = make('kaggriculture', configuration={'episodeSteps': 720}, debug=False)
    env.info['seed'] = g['info']['seed']
    R.LOG.clear()
    env.run(ag)
    agg = collections.defaultdict(lambda: [0, 0.0])
    byday = collections.defaultdict(float)
    for f, opn, item, price in R.LOG:
        if f != me:
            continue
        k = opn + ':' + item
        agg[k][0] += 1; agg[k][1] += price
    m = [env.steps[-1][i].observation.farms[i]['money'] for i in range(2)]
    money_by_day = [env.steps[d * 24 + 23][me].observation.farms[me]['money'] for d in range(30)]
    return agg, m[me], m[op], money_by_day


if __name__ == '__main__':
    a, b, team, eid = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
    A = run(a, eid, team); B = run(b, eid, team)
    print('money A', A[1], 'opp', A[2], '| B', B[1], 'opp', B[2])
    print('daily money diff B-A:', [round(y - x) for x, y in zip(A[3], B[3])])
    keys = sorted(set(A[0]) | set(B[0]), key=lambda k: -abs(B[0].get(k, [0, 0])[1] - A[0].get(k, [0, 0])[1]))
    for k in keys[:14]:
        x = A[0].get(k, [0, 0]); y = B[0].get(k, [0, 0])
        print(f'{k:24s} A {x[0]:5d} {x[1]:8.0f}  B {y[0]:5d} {y[1]:8.0f}  diff {y[1] - x[1]:+8.0f}')

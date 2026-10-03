"""Run a game and print our farm map / stats each day. usage: dbg.py cand.py opp.py seed [days]"""
import sys, io, contextlib, os, collections
from mapview import tch

with contextlib.redirect_stdout(io.StringIO()):
    from kaggle_environments import make
    from kaggle_environments.agent import get_last_callable


def run(a, b, seed):
    with contextlib.redirect_stdout(io.StringIO()):
        ents = [get_last_callable(open(p, encoding='utf-8').read(), path=os.path.abspath(p)) for p in (a, b)]
    env = make('kaggriculture', configuration={'seed': seed, 'episodeSteps': 720}, debug=True)
    env.run(ents)
    return env


if __name__ == '__main__':
    a, b, seed = sys.argv[1], sys.argv[2], int(sys.argv[3])
    hours = [int(h) for h in sys.argv[4].split(',')] if len(sys.argv) > 4 else [12]
    env = run(a, b, seed)
    for t, s in enumerate(env.steps):
        o = s[0].observation
        if o.hour in hours:
            f = o.farms[0]
            inv = o.private['inventories']
            print(f"d{o.day:2d}h{o.hour:2d} ${f['money']:7.0f} hands={len(f['hands'])} q={len(f['unlocked_quadrants'])} shed={ {k:v for k,v in o.private['shed'].items() if v} } seeds={ {k:v for k,v in o.private['seeds'].items() if v} } carried={sum(sum(i.values()) for i in inv)}")
            rows = [''.join(tch(f['tiles'][y][x]) for x in range(10)) for y in range(10)]
            pos = [tuple(f['farmer'])] + [tuple(h) for h in f['hands']]
            for y in range(10):
                print('   ' + rows[y] + '   ' + ''.join('*' if (x, y) in pos else '.' for x in range(10)))
    for i in (0, 1):
        print('final', i, env.steps[-1][i].observation.farms[i]['money'], env.steps[-1][i].status)
    for step in env.logs[:720]:
        for i, l in enumerate(step):
            if isinstance(l, dict) and l.get('stderr'):
                print('STDERR', i, l['stderr'][:500])
                break

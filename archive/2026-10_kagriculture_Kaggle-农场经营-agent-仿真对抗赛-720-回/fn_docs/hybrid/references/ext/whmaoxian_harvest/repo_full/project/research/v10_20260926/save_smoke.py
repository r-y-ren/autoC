"""Run a full official game and preserve the replay for an actual cash audit."""
import argparse, contextlib, gzip, io, json, sys
from pathlib import Path
root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(root))
p = argparse.ArgumentParser()
p.add_argument('--candidate', required=True)
p.add_argument('--opponent', required=True)
p.add_argument('--seed', type=int, required=True)
p.add_argument('--output', required=True)
a = p.parse_args()
with contextlib.redirect_stdout(io.StringIO()):
    from kaggle_environments import make
    from kaggle_environments.agent import get_last_callable
    entries = [get_last_callable((root/x).read_text(encoding='utf-8'),
               path=str(root/x)) for x in (a.candidate, a.opponent)]
env = make('kaggriculture', configuration={'seed':a.seed,'episodeSteps':720}, debug=True)
env.run(entries)
final = env.steps[-1]
errors = [log.get('stderr') for row in env.logs for log in row if log.get('stderr','').strip()]
assert len(env.steps)==720 and all(s.status=='DONE' for s in final) and not errors, errors
raw = json.dumps(env.toJSON(), ensure_ascii=False).encode('utf-8')
(root/a.output).write_bytes(gzip.compress(raw))
print(json.dumps({'entries':[f.__name__ for f in entries], 'rewards':[s.reward for s in final],
                  'states':len(env.steps),'output':a.output},ensure_ascii=False),flush=True)

import argparse,contextlib,io,json,gzip
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--candidate',required=True);p.add_argument('--opponent',default='external/round9/frontier/main.py');p.add_argument('--seed',type=int,required=True);p.add_argument('--output',required=True);a=p.parse_args()
with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
 from kaggle_environments import make
 from kaggle_environments.agent import get_last_callable
 f=get_last_callable(Path(a.candidate).read_text(encoding='utf-8'));o=get_last_callable(Path(a.opponent).read_text(encoding='utf-8'))
env=make('kaggriculture',configuration={'seed':a.seed,'episodeSteps':720},debug=True);env.run([f,o]);g=env.toJSON()
Path(a.output+'.json.gz').write_bytes(gzip.compress(json.dumps(g).encode()))
from league_round8 import telemetry
report={'candidate':a.candidate,'opponent':a.opponent,'seed':a.seed,'rewards':g['rewards'],'events':f.__globals__.get('_R9R_EVENTS',[]),'telemetry':telemetry(f)}
Path(a.output+'.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps({k:v for k,v in report.items() if k!='telemetry'}),flush=True)

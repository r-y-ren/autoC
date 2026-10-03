"""Win-first summaries for full-route search; expose the retrospective oracle only as an upper bound."""
from pathlib import Path
from collections import defaultdict,Counter
import json,statistics
D=Path(__file__).resolve().parent
BASE='submissions/release_v10_r2/main.py'
def load(p):return [json.loads(s) for s in p.read_text().splitlines() if s.strip()] if p.exists() else []
def context(r):return (r['opponent_sha256'],r['seed'],r['seat'])
def point(r):return 1 if r['margin']>0 else (.5 if r['margin']==0 else 0)
rows=load(D/'route_choice_results.jsonl');groups=defaultdict(list)
for row in rows:groups[context(row)].append(row)
base={context(r):r for r in rows if r['candidate']==BASE};out={};by_route=defaultdict(list)
for row in rows:
    if row.get('valid') and row.get('forced_route') is not None:by_route[row['forced_route']].append(row)
for route,data in by_route.items():
    pairs=[(r,base[context(r)]) for r in data if context(r) in base and base[context(r)].get('valid')]
    out[route]=dict(cases=len(data),wins=sum(point(r)==1 for r in data),points=sum(point(r) for r in data),baseline_points=sum(point(b) for r,b in pairs),gain=sum(point(r)-point(b) for r,b in pairs),mean_margin_gain=statistics.mean(r['margin']-b['margin'] for r,b in pairs) if pairs else None)
oracle=[]
for key,data in groups.items():
    valid=[r for r in data if r.get('valid')]
    if key not in base or not valid:continue
    best=max(valid,key=lambda r:(point(r),r['margin']))
    oracle.append(dict(seed=key[1],seat=key[2],family=best['family'],baseline_margin=base[key].get('margin'),best_route=best.get('forced_route'),best_margin=best['margin'],routes=len({r.get('forced_route') for r in valid})))
report=dict(completed=len(rows),invalid=sum(not r.get('valid') for r in rows),contexts=len(groups),routes=out,retrospective_oracle=oracle,scope='Oracle uses outcomes and is not a deployable or heldout result.')
(D/'route_choice_summary.json').write_text(json.dumps(report,indent=2))
print('COUNTS',report['completed'],report['invalid'],report['contexts'],flush=True)
print('ROUTES',json.dumps(sorted(out.items(),key=lambda x:(-x[1]['gain'],-(x[1]['mean_margin_gain'] or 0)))),flush=True)
print('ORACLE',json.dumps(oracle),flush=True)

"""Freeze a harder developmental panel before playing the candidate variants."""
from pathlib import Path
from collections import Counter
import hashlib,json,statistics
D=Path(__file__).resolve().parent;R=D.parents[1]
roster=json.loads((D/'counter_roster.json').read_text())
rows=[json.loads(s) for s in (D/'counter_screen_results.jsonl').read_text().splitlines()]
assert len(rows)==240 and all(r['valid'] for r in rows)
ranked=sorted(roster,key=lambda o:(sum(r['margin']>0 for r in rows if r['family']==o['family']),statistics.mean(r['margin'] for r in rows if r['family']==o['family'])))
selected=[];teachers=Counter()
for o in ranked:
    if teachers[o['teacher']]>=2:continue
    selected.append(o);teachers[o['teacher']]+=1
    if len(selected)==8:break
public=[o for o in json.loads((D/'pilot_design.json').read_text())['roster'] if o['panel']!='responsive_proxy']
roster=public+selected
seen=set()
for p in (R/'research').rglob('*jobs.json'):
    value=json.loads(p.read_text())
    if isinstance(value,list):seen.update(r['seed'] for r in value if isinstance(r,dict) and isinstance(r.get('seed'),int))
seeds=[int.from_bytes(hashlib.sha256(f'route-value-broad-dev-927-{i}'.encode()).digest()[:4],'big')%2000000000 for i in range(8)]
assert len(set(seeds))==8 and not set(seeds)&seen
candidates=['research/route_value_20260927/learned.py','research/route_value_20260927/combined.py',
 'research/v10_top10_20260926/micro_candidates/all_care_first.py','submissions/release_v10_r2/main.py']
jobs=[]
for candidate in candidates:
    for opponent in roster:
        for seed in seeds:
            for seat in (0,1):
                j=dict(candidate=candidate,opponent=opponent['path'],seed=seed,seat=seat,family=opponent['family'],panel=opponent['panel'])
                for key in ('candidate','opponent'):j[key+'_sha256']=hashlib.sha256((R/j[key]).read_bytes()).hexdigest()
                j['id']=hashlib.sha256(json.dumps(j,sort_keys=True).encode()).hexdigest()[:24];jobs.append(j)
(D/'broad_jobs.json').write_text(json.dumps(jobs,indent=2))
(D/'broad_design.json').write_text(json.dumps(dict(seeds=seeds,roster=roster,candidates=candidates,
    jobs=len(jobs),opponent_selection='Hardest development proxies, maximum two views per teacher.',
    scope='Harder prospective DEVELOPMENT. Proxies are not private leaderboard agents; no rating calibration.'),indent=2))
print(json.dumps(dict(games=len(jobs),proxies=[o['family'] for o in selected],worlds=len(seeds))),flush=True)

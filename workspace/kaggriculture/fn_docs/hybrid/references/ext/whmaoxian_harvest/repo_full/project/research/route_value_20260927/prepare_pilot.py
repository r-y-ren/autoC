"""Prospective development batch; preserve all earlier confirmation worlds."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1];M=R/'research/macro_population_20260927'
seen=set()
for path in (R/'research').rglob('*jobs.json'):
    value=json.loads(path.read_text(encoding='utf-8'))
    if isinstance(value,list):seen.update(j['seed'] for j in value if isinstance(j,dict) and isinstance(j.get('seed'),int))
for values in json.loads((M/'worlds.json').read_text()).values():
    if isinstance(values,list):seen.update(v for v in values if isinstance(v,int))
seeds=[int.from_bytes(hashlib.sha256(f'route-value-pilot-20260927-{i}'.encode()).digest()[:4],'big')%2000000000 for i in range(8)]
assert len(set(seeds))==8 and not set(seeds)&seen
roster=json.loads((R/'research/v10_top10_20260926/route_expansion_design.json').read_text())['roster']
variants=json.loads((D/'agents.json').read_text())
base='submissions/release_v10_r2/main.py';paths=[v['path'] for v in variants if not v['shadow']]+[base]
jobs=[]
for candidate in paths:
    for opponent in roster:
        for seed in seeds:
            for seat in (0,1):
                j=dict(candidate=candidate,opponent=opponent['path'],seed=seed,seat=seat,family=opponent['family'],panel=opponent['panel'])
                for key in ('candidate','opponent'):j[key+'_sha256']=hashlib.sha256((R/j[key]).read_bytes()).hexdigest()
                j['id']=hashlib.sha256(json.dumps(j,sort_keys=True).encode()).hexdigest()[:24];jobs.append(j)
(D/'pilot_jobs.json').write_text(json.dumps(jobs,indent=2))
(D/'pilot_design.json').write_text(json.dumps(dict(seeds=seeds,roster=roster,candidates=paths,jobs=len(jobs),
   previous_seen_count=len(seen),overlap=0,scope='Prospective development, not final confirmation or measured rating.'),indent=2))
print(json.dumps(dict(games=len(jobs),new_worlds=len(seeds))),flush=True)

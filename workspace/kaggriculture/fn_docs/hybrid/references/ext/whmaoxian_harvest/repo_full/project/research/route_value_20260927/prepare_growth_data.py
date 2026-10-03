"""Expand actual route outcomes against newly discovered difficult behaviors."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1];M=R/'research/macro_population_20260927'
old=json.loads((M/'route_learning_design.json').read_text())
variants=[v for v in old['variants'] if v['route'] in (None,9,12,100,110,128)]
broad=json.loads((D/'broad_design.json').read_text());roster=[];teachers=set()
for o in broad['roster']:
    if o['panel']=='responsive_proxy' and o['teacher'] not in teachers:
        roster.append(o);teachers.add(o['teacher'])
    if len(teachers)==4:break
roster+=[o for o in broad['roster'] if o['family'] in ('fieldcraft','marketshock','r2')]
assert len(roster)==7 and len(variants)==6
seen=set()
for p in (R/'research').rglob('*jobs.json'):
    value=json.loads(p.read_text())
    if isinstance(value,list):seen.update(r['seed'] for r in value if isinstance(r,dict) and isinstance(r.get('seed'),int))
for values in json.loads((M/'worlds.json').read_text()).values():
    if isinstance(values,list):seen.update(x for x in values if isinstance(x,int))
seeds=[int.from_bytes(hashlib.sha256(f'route-value-expanded-training-927-{i}'.encode()).digest()[:4],'big')%2000000000 for i in range(32)]
assert len(set(seeds))==32 and not set(seeds)&seen
jobs=[]
for variant in variants:
    for opponent in roster:
        for seed in seeds:
            for seat in (0,1):
                j=dict(candidate=variant['path'],opponent=opponent['path'],seed=seed,seat=seat,family=opponent['family'],panel=opponent['panel'])
                for key in ('candidate','opponent'):j[key+'_sha256']=hashlib.sha256((R/j[key]).read_bytes()).hexdigest()

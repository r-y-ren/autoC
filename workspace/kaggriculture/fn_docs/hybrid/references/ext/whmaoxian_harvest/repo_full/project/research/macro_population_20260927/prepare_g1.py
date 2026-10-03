"""Freeze development worlds and opponents before reading any new outcomes."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1];T=R/'research/v10_top10_20260926'
variants=json.loads((D/'population_g1.json').read_text())
old=json.loads((T/'route_expansion_design.json').read_text())['roster']
roster=[r for r in old if r['family'] in ('fieldcraft','aurax','marketshock','top_style_02','top_style_03','r2')]
assert len(roster)==6
seen=set()
for root in (T,R/'research/v10_rebuild_20260926'):
    for path in root.rglob('*_jobs.json'):
        for job in json.loads(path.read_text(encoding='utf-8')):
            if isinstance(job,dict) and isinstance(job.get('seed'),int):seen.add(job['seed'])
def seeds(label,n):
    result=[int.from_bytes(hashlib.sha256(f'macro-pop-20260927-{label}-{i}'.encode()).digest()[:4],'big')%2000000000 for i in range(n)]
    assert len(set(result))==n and not seen.intersection(result);return result
worlds={label:seeds(label,n) for label,n in [('g1',4),('g2',8),('confirmation',32)]}
assert len(set(sum(worlds.values(),[])))==44
candidates=[v['path'] for v in variants]+['submissions/release_v9/main.py','submissions/release_v10/main.py','submissions/release_v10_r2/main.py']
jobs=[]
for candidate in candidates:
    for opponent in roster:
        for seed in worlds['g1']:
            for seat in (0,1):
                j=dict(candidate=candidate,opponent=opponent['path'],family=opponent['family'],panel=opponent['panel'],seed=seed,seat=seat)
                for k in ('candidate','opponent'):j[k+'_sha256']=hashlib.sha256((R/j[k]).read_bytes()).hexdigest()
                j['id']=hashlib.sha256(json.dumps(j,sort_keys=True).encode()).hexdigest()[:24];jobs.append(j)
(D/'worlds.json').write_text(json.dumps(worlds,indent=2))
(D/'roster.json').write_text(json.dumps(roster,indent=2))
(D/'g1_jobs.json').write_text(json.dumps(jobs,indent=2))
control=variants[0]['path'];baseline='submissions/release_v10_r2/main.py'
smoke=[j for j in jobs if j['candidate'] in (control,baseline) and j['seed']==worlds['g1'][0] and j['family'] in ('fieldcraft','top_style_03')]
assert len(smoke)==8
(D/'smoke_jobs.json').write_text(json.dumps(smoke,indent=2))
print(json.dumps(dict(population=len(variants),jobs=len(jobs),worlds=worlds['g1'],smoke=len(smoke),seen_worlds=len(seen))))

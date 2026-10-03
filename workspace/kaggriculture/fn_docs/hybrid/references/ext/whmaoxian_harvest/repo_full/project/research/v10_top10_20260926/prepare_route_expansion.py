"""Prospective development comparison of the strongest route and R2 controls."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1]
design=json.loads((D/'extended_design.json').read_text())
roster=[r for r in design['roster'] if r['family']!='counter_advance36']
candidates=['submissions/release_v10_r2/main.py','research/v10_top10_20260926/micro_candidates/all_care_first.py','research/v10_top10_20260926/guard_ablations/top_style_03_default.py','research/v10_top10_20260926/guard_ablations/top_style_03_no_dead.py']
seen=set()
for root in (D,R/'research/v10_rebuild_20260926'):
    for path in root.rglob('*jobs.json'):
        if path.name=='route_expansion_jobs.json':continue
        data=json.loads(path.read_text(encoding='utf-8'))
        if isinstance(data,list):seen.update(r['seed'] for r in data if isinstance(r,dict) and isinstance(r.get('seed'),int))
seeds=[int.from_bytes(hashlib.sha256(f'kaggriculture-top10-route-expansion-d1-{i}'.encode()).digest()[:4],'big')%2000000000 for i in range(8)]
assert not seen.intersection(seeds) and len(set(seeds))==8
jobs=[]
for candidate in candidates:
    for opponent in roster:
        for seed in seeds:
            for seat in (0,1):
                job=dict(candidate=candidate,opponent=opponent['path'],family=opponent['family'],panel=opponent['panel'],seed=seed,seat=seat)
                for key in ('candidate','opponent'):job[key+'_sha256']=hashlib.sha256((R/job[key]).read_bytes()).hexdigest()
                job['id']=hashlib.sha256(json.dumps(job,sort_keys=True).encode()).hexdigest()[:24];jobs.append(job)
assert len(jobs)==704
(D/'route_expansion_jobs.json').write_text(json.dumps(jobs,indent=2),encoding='utf-8')
(D/'route_expansion_design.json').write_text(json.dumps(dict(candidates=candidates,roster=roster,seeds=seeds,overlap=0,prior_seen_seeds=len(seen),jobs=len(jobs),scope='Fresh prospective development, not final confirmation. Public programs, reactive proxies and direct-reference panels stay separate.'),indent=2),encoding='utf-8')
print(json.dumps(dict(jobs=len(jobs),worlds=len(seeds),prior_seeds=len(seen),overlap=0)),flush=True)

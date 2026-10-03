"""Expand existing complete-plan candidates on new prospective development worlds."""
from pathlib import Path
import hashlib,json
P=Path(__file__).resolve().parent;R=P.parents[1]
roster=json.loads((R/'research/macro_population_20260927/roster.json').read_text())
candidates=['research/structural_20260927/plans/plan02_physical.py','research/structural_20260927/plans/plan02_default.py','research/structural_20260927/plans/plan01_physical.py','submissions/release_v10_r2/main.py']
seeds=[int.from_bytes(hashlib.sha256(f'structural-route-expanded-20260927-{i}'.encode()).digest()[:4],'big')%2000000000 for i in range(12)]
assert len(set(seeds))==12
jobs=[]
for candidate in candidates:
    for rival in roster:
        for seed in seeds:
            for seat in (0,1):
                row=dict(candidate=candidate,opponent=rival['path'],family=rival['family'],panel=rival['panel'],seed=seed,seat=seat)
                for key in ('candidate','opponent'):row[key+'_sha256']=hashlib.sha256((R/row[key]).read_bytes()).hexdigest()
                row['id']=hashlib.sha256(json.dumps(row,sort_keys=True).encode()).hexdigest()[:24];jobs.append(row)
for filename,data in [('plan_extended_jobs.json',jobs),('plan_extended_design.json',dict(candidates=candidates,roster=roster,seeds=seeds,total=len(jobs),scope='Prospective development after first screen, not final independent confirmation.'))]:
    path=P/filename
    if path.exists():assert json.loads(path.read_text())==data
    else:path.write_text(json.dumps(data,indent=2))
print(json.dumps(dict(jobs=len(jobs),worlds=len(seeds),candidates=len(candidates))),flush=True)

"""Finite activation-and-economics pilot for independent ranch workers."""
from pathlib import Path
import hashlib,json
P=Path(__file__).resolve().parent;R=P.parents[1]
variants=json.loads((P/'ranch_manifest.json').read_text())
design=json.loads((P/'plan_screen_design.json').read_text())
roster=[r for r in design['roster'] if r['family'] in ('fieldcraft','r2')]
seeds=design['seeds'][:2];jobs=[]
for candidate in [v['path'] for v in variants]+['submissions/release_v10_r2/main.py']:
    for rival in roster:
        for seed in seeds:
            for seat in (0,1):
                row=dict(candidate=candidate,opponent=rival['path'],family=rival['family'],panel=rival['panel'],seed=seed,seat=seat)
                for key in ('candidate','opponent'):row[key+'_sha256']=hashlib.sha256((R/row[key]).read_bytes()).hexdigest()
                row['id']=hashlib.sha256(json.dumps(row,sort_keys=True).encode()).hexdigest()[:24];jobs.append(row)
for name,data in [('ranch_screen_jobs.json',jobs),('ranch_screen_design.json',dict(variants=variants,roster=roster,seeds=seeds,total=len(jobs),scope='Activation and development only; all forced investments retained including losses.'))]:
    path=P/name
    if path.exists():assert json.loads(path.read_text())==data
    else:path.write_text(json.dumps(data,indent=2))
print(json.dumps(dict(jobs=len(jobs),worlds=len(seeds))),flush=True)

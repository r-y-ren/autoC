"""Declare second-generation paired development without using sealed test worlds."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1]
variants=json.loads((D/'generation2_manifest.json').read_text())
roster=json.loads((R/'research/macro_population_20260927/roster.json').read_text())
seeds=[667500670,942022459,223350887,1726596017]
paths=[v['path'] for v in variants]+['submissions/release_v10_r2/main.py']
jobs=[]
for path in paths:
    for other in roster:
        for seed in seeds:
            for seat in (0,1):
                row=dict(candidate=path,opponent=other['path'],family=other['family'],panel=other['panel'],seed=seed,seat=seat)
                for key in ('candidate','opponent'):row[key+'_sha256']=hashlib.sha256((R/row[key]).read_bytes()).hexdigest()
                row['id']=hashlib.sha256(json.dumps(row,sort_keys=True).encode()).hexdigest()[:24];jobs.append(row)
manifest=D/'g2_jobs.json'
if manifest.exists():assert json.loads(manifest.read_text())==jobs
else:manifest.write_text(json.dumps(jobs,indent=2))
(D/'g2_design.json').write_text(json.dumps(dict(seeds=seeds,roster=roster,variants=variants,total_games=len(jobs),scope='Paired development. Forced-entry probes are diagnostic, not approved candidates.'),indent=2))
print(json.dumps(dict(jobs=len(jobs))),flush=True)

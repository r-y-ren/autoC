"""Predeclare finite development matches for slot-order variants."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1]
design=json.loads((D/'extended_design.json').read_text(encoding='utf-8'))
models=json.loads((D/'slot_candidates_manifest.json').read_text(encoding='utf-8'))
candidates=[r['path'] for r in models]+['submissions/release_v10_r2/main.py']
seeds=design['seeds'][:2];roster=design['roster'];jobs=[]
for candidate in candidates:
    for opponent in roster:
        for seed in seeds:
            for seat in (0,1):
                job=dict(candidate=candidate,opponent=opponent['path'],family=opponent['family'],panel=opponent['panel'],seed=seed,seat=seat)
                for key in ('candidate','opponent'):job[key+'_sha256']=hashlib.sha256((R/job[key]).read_bytes()).hexdigest()
                job['id']=hashlib.sha256(json.dumps(job,sort_keys=True).encode()).hexdigest()[:24]
                jobs.append(job)
assert len(jobs)==288 and len({j['id'] for j in jobs})==288
path=D/'slot_screen_jobs.json'
if path.exists():assert json.loads(path.read_text())==jobs
else:path.write_text(json.dumps(jobs,indent=2),encoding='utf-8')
(D/'slot_screen_design.json').write_text(json.dumps(dict(candidates=models,roster=roster,seeds=seeds,jobs=len(jobs),scope='Development only. All matches fresh; observer-only control must remain action-identical to R2. No held-out game or release is created.'),indent=2),encoding='utf-8')
print(json.dumps(dict(jobs=len(jobs),models=len(models),worlds=len(seeds),opponents=len(roster))),flush=True)

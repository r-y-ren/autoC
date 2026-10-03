"""Prepare the second local farming-game evaluation batch."""
from pathlib import Path
import hashlib,json
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[1]
candidates=[r['path'] for r in json.loads((OUT/'generation2_manifest.json').read_text())]
candidates += ['submissions/release_v10/main.py','research/v10_rebuild_20260926/candidates/open_5.py']
programs=json.loads((OUT/'public_programs.json').read_text())
opponents=[r['path'] for r in programs]
opponents += ['submissions/release_v9/main.py','submissions/release_v10/main.py','external/round9/frontier/main.py']
cases=[]
for opponent in opponents:
    for index in range(3):
        seed=int.from_bytes(hashlib.sha256(f'v10r2-closed-development-{index}'.encode()).digest()[:4],'big')%2000000000
        for seat in (0,1):
            cases.append(dict(opponent=opponent,seed=seed,seat=seat,panel='closed_loop',family=Path(opponent).parent.name))
for row in json.loads((OUT/'probe_roster.json').read_text(encoding='utf-8')):
    if row['role']=='actual_v10_loss':
        cases.append(dict(opponent=row['path'],seed=row['seed'],seat=1-row['seat'],
            panel='online_loss_probe',family=str(row['submission'])))
jobs=[]
for candidate in candidates:
    for case in cases:
        job=dict(case,candidate=candidate)
        for key in ('candidate','opponent'):
            job[key+'_sha256']=hashlib.sha256((ROOT/job[key]).read_bytes()).hexdigest()
        job['id']=hashlib.sha256(json.dumps(job,sort_keys=True).encode()).hexdigest()[:24]
        jobs.append(job)
(OUT/'generation2_jobs.json').write_text(json.dumps(jobs,indent=2),encoding='utf-8')
print('Frozen generation 2',len(jobs),'complete-match jobs',flush=True)

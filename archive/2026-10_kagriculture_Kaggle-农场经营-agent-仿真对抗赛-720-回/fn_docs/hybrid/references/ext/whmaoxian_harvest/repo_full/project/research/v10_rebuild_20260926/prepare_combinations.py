"""Frozen larger development panel; public programs and local population separated."""
from pathlib import Path
import hashlib,json,runpy
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[1]
_ = runpy.run_path(str(OUT/'build_combinations.py'),run_name='__main__')
candidates=[r['path'] for r in json.loads((OUT/'combination_manifest.json').read_text())]
candidates += ['research/v10_rebuild_20260926/generation2/h12_observed4.py','submissions/release_v10/main.py']
programs=json.loads((OUT/'public_programs.json').read_text())
opponents=[(p['path'],'public_program',p['name']) for p in programs if p['name']!='pipe5']
opponents += [(f'submissions/release_{version}/main.py','old_reference',version) for version in ('v9','v10')]
opponents += [(f'research/v10_rebuild_20260926/generation2/{name}.py','local_population',name)
              for name in ('h12_observed4','h24','h12_book')]
cases=[]
for opponent,panel,family in opponents:
    for index in range(8):
        seed=int.from_bytes(hashlib.sha256(f'v10r2-closed-development-{index}'.encode()).digest()[:4],'big')%2000000000
        for seat in (0,1):
            cases.append(dict(opponent=opponent,seed=seed,seat=seat,panel=panel,family=family))
for row in json.loads((OUT/'probe_roster.json').read_text(encoding='utf-8')):
    if row['role']=='actual_v10_loss':
        cases.append(dict(opponent=row['path'],seed=row['seed'],seat=1-row['seat'],panel='online_loss_probe',family=str(row['submission'])))
jobs=[]
for candidate in candidates:
    for case in cases:
        job=dict(case,candidate=candidate)
        for key in ('candidate','opponent'):
            job[key+'_sha256']=hashlib.sha256((ROOT/job[key]).read_bytes()).hexdigest()
        job['id']=hashlib.sha256(json.dumps(job,sort_keys=True).encode()).hexdigest()[:24]
        jobs.append(job)
(OUT/'combination_jobs.json').write_text(json.dumps(jobs,indent=2),encoding='utf-8')
print('Combination round complete-match jobs',len(jobs),flush=True)

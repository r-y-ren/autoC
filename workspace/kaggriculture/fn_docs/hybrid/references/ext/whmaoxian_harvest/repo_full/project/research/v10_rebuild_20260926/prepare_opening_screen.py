from pathlib import Path
import hashlib,json,runpy
OUT=Path(__file__).resolve().parent; ROOT=OUT.parents[1]
runpy.run_path(str(OUT/'build_opening_candidates.py'),run_name='__main__')
runpy.run_path(str(OUT/'build_trace_probes.py'),run_name='__main__')
candidates=[r['path'] for r in json.loads((OUT/'candidates/opening_manifest.json').read_text())]
candidates += ['submissions/release_v9/main.py','submissions/release_v10/main.py']
roster=json.loads((OUT/'probe_roster.json').read_text(encoding='utf-8'))
sealed={56555482,56551631,56531474,56494372}
cases=[]
for row in roster:
    if row['role']=='actual_v10_loss' or (row['role']=='study' and row['submission'] not in sealed):
        cases.append(dict(opponent=row['path'],seed=row['seed'],seat=1-row['seat'],
            family=str(row['submission']),panel='online_loss_probe' if row['role']=='actual_v10_loss' else 'current_ladder_probe'))
for opponent in ['submissions/release_v9/main.py','external/round9/frontier/main.py','external/round8/master2965/main.py']:
    for index in range(3):
        seed=int.from_bytes(hashlib.sha256(f'v10r2-opening-development-{index}'.encode()).digest()[:4],'big')%2000000000
        for seat in (0,1):
            cases.append(dict(opponent=opponent,seed=seed,seat=seat,family=opponent,panel='closed_loop_regression'))
jobs=[]
for candidate in candidates:
    for case in cases:
        job=dict(case,candidate=candidate)
        for key in ('candidate','opponent'):
            job[key+'_sha256']=hashlib.sha256((ROOT/job[key]).read_bytes()).hexdigest()
        job['id']=hashlib.sha256(json.dumps(job,sort_keys=True).encode()).hexdigest()[:24]
        jobs.append(job)
(OUT/'opening_jobs.json').write_text(json.dumps(jobs,indent=2),encoding='utf-8')
print('Prepared opening screen',len(jobs),'full matches',flush=True)

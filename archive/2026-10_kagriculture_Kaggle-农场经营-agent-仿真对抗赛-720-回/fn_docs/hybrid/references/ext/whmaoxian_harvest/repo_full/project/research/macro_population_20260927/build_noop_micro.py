"""Build and schedule a finite farming-command efficiency experiment."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1];out=D/'noop_micro';out.mkdir(exist_ok=True)
base_path='submissions/release_v10_r2/main.py';raw=(R/base_path).read_bytes()
assert hashlib.sha256(raw).hexdigest()=='b35b5b09fbec059ab7cbd2ba67a9fbb6d3e467ef5262f3e2ddba592b3e50c1c4'
configs=[('control',False,()),('pass_only',True,('care','fertilizer','harvest','water')),('care_only',False,('care',)),('care_water',False,('care','water')),('care_first',False,('care','fertilizer','harvest','water')),('fert_first',False,('fertilizer','care','harvest','water')),('harvest_first',False,('harvest','care','fertilizer','water'))]
variants=[]
for name,pass_only,priority in configs:
    settings=f'\n_NM_MODE={name!r}\n_NM_START=24\n_NM_PASS_ONLY={pass_only!r}\n_NM_MIN_PRICE=2\n_NM_PRIORITY={priority!r}\n'
    data=raw+settings.encode()+(D/'noop_micro_tail.py.txt').read_bytes();path=out/(name+'.py')
    compile(data,str(path),'exec')
    if path.exists():assert path.read_bytes()==data
    else:path.write_bytes(data)
    variants.append(dict(path=path.relative_to(R).as_posix(),name=name,sha256=hashlib.sha256(data).hexdigest()))
base_jobs=[j for j in json.loads((D/'route_jobs.json').read_text()) if j['candidate']==base_path]
jobs=list(base_jobs)
for variant in variants:
    for old in base_jobs:
        job=dict(old,candidate=variant['path'],candidate_sha256=variant['sha256']);job.pop('id')
        job['id']=hashlib.sha256(json.dumps(job,sort_keys=True).encode()).hexdigest()[:24];jobs.append(job)
controls=[json.loads(s) for s in (D/'route_results.jsonl').read_text().splitlines() if s.strip()]
controls=[r for r in controls if r['candidate']==base_path];assert len(controls)==48 and all(r['valid'] for r in controls)
output=D/'noop_micro_results.jsonl';assert not output.exists()
output.write_text(''.join(json.dumps(r)+'\n' for r in controls))
(D/'noop_micro_manifest.json').write_text(json.dumps(variants,indent=2))
(D/'noop_micro_jobs.json').write_text(json.dumps(jobs,indent=2))
print(json.dumps(dict(variants=len(variants),games=len(jobs),reused_controls=len(controls),fresh_games=len(jobs)-len(controls))),flush=True)

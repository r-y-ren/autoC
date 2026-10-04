"""Finite terminal-search compute ablation using unchanged physical acceptance."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1];out=D/'terminal_search';out.mkdir(exist_ok=True)
base_path='submissions/release_v10_r2/main.py';base=(R/base_path).read_bytes()
assert hashlib.sha256(base).hexdigest()=='b35b5b09fbec059ab7cbd2ba67a9fbb6d3e467ef5262f3e2ddba592b3e50c1c4'
variants=[]
for name,simulations,passes,proposals in [('control',64,1,4),('broad',128,1,8),('two_pass',160,2,8),('wide',240,2,12)]:
    tail=f'\n_TS_MODE={name!r}\n_TS_SIMULATIONS={simulations}\n_TS_PASSES={passes}\n_TS_PROPOSALS={proposals}\n'
    raw=base+tail.encode()+(D/'terminal_search_tail.py.txt').read_bytes();path=out/(name+'.py');compile(raw,str(path),'exec')
    if path.exists():assert path.read_bytes()==raw
    else:path.write_bytes(raw)
    variants.append(dict(path=path.relative_to(R).as_posix(),name=name,sha256=hashlib.sha256(raw).hexdigest()))
base_jobs=[j for j in json.loads((D/'route_jobs.json').read_text()) if j['candidate']==base_path];jobs=list(base_jobs)
for variant in variants:
    for old in base_jobs:
        job=dict(old,candidate=variant['path'],candidate_sha256=variant['sha256']);job.pop('id')
        job['id']=hashlib.sha256(json.dumps(job,sort_keys=True).encode()).hexdigest()[:24];jobs.append(job)
controls=[json.loads(s) for s in (D/'route_results.jsonl').read_text().splitlines()]
controls=[r for r in controls if r['candidate']==base_path];assert len(controls)==48 and all(r['valid'] for r in controls)
output=D/'terminal_search_results.jsonl';assert not output.exists()
output.write_text(''.join(json.dumps(r)+'\n' for r in controls))
(D/'terminal_search_manifest.json').write_text(json.dumps(variants,indent=2))
(D/'terminal_search_jobs.json').write_text(json.dumps(jobs,indent=2))
print(json.dumps(dict(variants=len(variants),total=len(jobs),reused=len(controls),fresh=len(jobs)-len(controls))),flush=True)

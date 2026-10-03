"""Test complete existing production plans in an isolated research directory."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1]
raw=(R/'submissions/release_v10_r2/main.py').read_bytes()
assert hashlib.sha256(raw).hexdigest()=='b35b5b09fbec059ab7cbd2ba67a9fbb6d3e467ef5262f3e2ddba592b3e50c1c4'
catalog=json.loads((D/'native_route_catalog.json').read_text())
allowed={r['route'] for r in catalog['routes'] if r['prefix144_exact']}
ids=[0,9,12,100,101,109,110,114,115,123,126,128]
assert set(ids)<=allowed
out=D/'route_population';out.mkdir(exist_ok=True);variants=[]
for route in [None]+ids:
    path=out/('native_control.py' if route is None else f'route_{route}.py')
    data=raw+('\n_RP_FIXED_ROUTE='+repr(route)+'\n').encode()+(D/'route_policy_tail.py.txt').read_bytes()+b'\n_MP_REPORT=_RP_REPORT\n'
    compile(data,str(path),'exec')
    if path.exists():assert path.read_bytes()==data
    else:path.write_bytes(data)
    variants.append(dict(path=path.relative_to(R).as_posix(),route=route,sha256=hashlib.sha256(data).hexdigest()))
(D/'route_population.json').write_text(json.dumps(variants,indent=2))
seen=set(sum(json.loads((D/'worlds.json').read_text()).values(),[]))
seeds=[int.from_bytes(hashlib.sha256(f'macro-complete-route-study-20260927-{i}'.encode()).digest()[:4],'big')%2000000000 for i in range(4)]
assert len(set(seeds))==4 and not set(seeds)&seen
roster=json.loads((D/'roster.json').read_text())
paths=[v['path'] for v in variants]+['submissions/release_v10_r2/main.py']
jobs=[]
for candidate in paths:
    for opponent in roster:
        for seed in seeds:
            for seat in (0,1):
                job=dict(candidate=candidate,opponent=opponent['path'],family=opponent['family'],panel=opponent['panel'],seed=seed,seat=seat)
                for key in ('candidate','opponent'):
                    job[key+'_sha256']=hashlib.sha256((R/job[key]).read_bytes()).hexdigest()
                job['id']=hashlib.sha256(json.dumps(job,sort_keys=True).encode()).hexdigest()[:24]
                jobs.append(job)
manifest=D/'route_jobs.json'
if manifest.exists():assert json.loads(manifest.read_text())==jobs
else:manifest.write_text(json.dumps(jobs,indent=2))
(D/'route_design.json').write_text(json.dumps(dict(seeds=seeds,roster=roster,variants=variants,jobs=len(jobs),scope='Prospective development; not rating or heldout validation.'),indent=2))
print(json.dumps(dict(variants=len(variants),jobs=len(jobs),seeds=seeds)),flush=True)

"""Compile finite routed-dispatch ablations, with original prototypes preserved."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1]
base=(R/'submissions/release_v10_r2/main.py').read_bytes()
assert hashlib.sha256(base).hexdigest()=='b35b5b09fbec059ab7cbd2ba67a9fbb6d3e467ef5262f3e2ddba592b3e50c1c4'
helpers=(D/'dispatch.py.txt').read_bytes();tail=(D/'route_dispatch.py.txt').read_bytes()
manifest=[]
for workers in (12,13,14):
    for feed,care in ((200,0),(600,100)):
        name=f'routed_w{workers}_f{feed}'
        constants=f'\n_DP_START=16\n_DP_WORKERS={workers}\n_DP_DELIVERY=16\n_DP_PLANT_WEIGHT=.3\n_DP_FEED_WEIGHT=1\n_DP_DISTANCE_POWER=1.0\n_VR_START=16\n_VR_WORKERS={workers}\n_VR_FEED={feed}\n_VR_CARE={care}\n'
        code=base+constants.encode()+helpers+tail;path=D/(name+'.py');compile(code,str(path),'exec')
        assert not path.exists();path.write_bytes(code)
        manifest.append(dict(name=name,path=path.relative_to(R).as_posix(),sha256=hashlib.sha256(code).hexdigest()))
base_path='submissions/release_v10_r2/main.py'
cases=[j for j in json.loads((D/'smoke_jobs.json').read_text()) if j['candidate']==base_path];jobs=[]
for item in manifest:
    for case in cases:
        job=dict(case,candidate=item['path'],candidate_sha256=item['sha256']);job.pop('id')
        job['id']=hashlib.sha256(json.dumps(job,sort_keys=True).encode()).hexdigest()[:24];jobs.append(job)
(D/'routed_manifest.json').write_text(json.dumps(manifest,indent=2))
(D/'routed_jobs.json').write_text(json.dumps(jobs,indent=2))
(D/'routed_single_jobs.json').write_text(json.dumps(jobs[:1],indent=2))
print(json.dumps(dict(variants=len(manifest),games=len(jobs))),flush=True)

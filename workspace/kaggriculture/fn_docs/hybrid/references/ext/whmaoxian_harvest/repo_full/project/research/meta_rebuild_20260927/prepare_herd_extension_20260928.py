"""Freeze a fresh development panel before running any candidate on its worlds."""
from pathlib import Path
import hashlib,json,random
D=Path(__file__).resolve().parent;R=D.parents[1]
sha=lambda data:hashlib.sha256(data).hexdigest()
source=json.loads((D/'midgame_herd_design.json').read_text())
manifest=D/'herd_extension_jobs.json';design_path=D/'herd_extension_design.json'
if manifest.exists() or design_path.exists():
    raise SystemExit('Existing panel preserved; use its stored manifest.')
seeds=random.Random(202609280417).sample(range(1,2147483647),32)
jobs=[]
for v in source['variants']:
    assert sha((R/v['path']).read_bytes())==v['sha256']
    for rival in source['roster']:
        for seed in seeds:
            for seat in (0,1):
                j=dict(candidate=v['path'],opponent=rival['path'],family=rival['family'],panel=rival['panel'],seed=seed,seat=seat,candidate_sha256=v['sha256'],opponent_sha256=sha((R/rival['path']).read_bytes()))
                j['id']=sha(json.dumps(j,sort_keys=True).encode())[:24];jobs.append(j)
design=dict(variants=source['variants'],roster=source['roster'],seeds=seeds,cases=len(jobs),scope='Fresh prospective development worlds. Not final heldout, not rating calibration.',selection='32 seeds generated before results; both seats and fixed roster.')
design_path.write_text(json.dumps(design,indent=2));manifest.write_text(json.dumps(jobs,indent=2))
print(json.dumps({'cases':len(jobs),'worlds':len(seeds)}),flush=True)

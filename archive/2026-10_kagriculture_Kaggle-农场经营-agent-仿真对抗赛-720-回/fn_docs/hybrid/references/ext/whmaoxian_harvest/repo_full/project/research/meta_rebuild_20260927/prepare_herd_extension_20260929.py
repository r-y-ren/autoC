"""Expand the existing herd pilot onto new development worlds. No releases touched."""
from pathlib import Path
import hashlib,json,random
D=Path(__file__).resolve().parent;R=D.parents[1]
prior=json.loads((D/'midgame_herd_design.json').read_text())
rng=random.Random(2026092901); seeds=rng.sample(range(100000,2100000000),24)
variants=prior['variants'];roster=prior['roster'];jobs=[]
for v in variants:
    assert hashlib.sha256((R/v['path']).read_bytes()).hexdigest()==v['sha256']
    for op in roster:
        for seed in seeds:
            for seat in (0,1):
                j=dict(candidate=v['path'],opponent=op['path'],family=op['family'],panel=op['panel'],seed=seed,seat=seat,candidate_sha256=v['sha256'],opponent_sha256=hashlib.sha256((R/op['path']).read_bytes()).hexdigest())
                j['id']=hashlib.sha256(json.dumps(j,sort_keys=True).encode()).hexdigest()[:24];jobs.append(j)
out=dict(variants=variants,roster=roster,seeds=seeds,jobs=len(jobs),scope='New development worlds; not final heldout and not online rating evidence.')
for name,obj in [('herd_extended_design_20260929.json',out),('herd_extended_jobs_20260929.json',jobs)]:
    path=D/name;data=json.dumps(obj,indent=2)
    if path.exists():assert path.read_text()==data
    else:path.write_text(data)
print(json.dumps(dict(worlds=len(seeds),cases=len(jobs))),flush=True)

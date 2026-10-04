"""Component replication on the remaining eighteen predeclared development worlds."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1];sha=lambda b:hashlib.sha256(b).hexdigest()
old=json.loads((D/'noop_deposit_design_20260929.json').read_text())
worlds=json.loads((D/'herd_extended_design_20260929.json').read_text())
variants=[v for v in old['variants'] if v['name'] in ('depot_sell','depot_late')]
seeds=worlds['seeds'][6:];jobs=[]
for v in variants:
    assert sha((R/v['path']).read_bytes())==v['sha256']
    for op in worlds['roster']:
        for seed in seeds:
            for seat in (0,1):
                j=dict(candidate=v['path'],opponent=op['path'],family=op['family'],panel=op['panel'],seed=seed,seat=seat,candidate_sha256=v['sha256'],opponent_sha256=sha((R/op['path']).read_bytes()))
                j['id']=sha(json.dumps(j,sort_keys=True).encode())[:24];jobs.append(j)
for name,obj in [('noop_deposit_extended_jobs_20260929.json',jobs),('noop_deposit_extended_design_20260929.json',dict(variants=variants,seeds=seeds,roster=worlds['roster'],scope='Extension on predeclared remaining development worlds. Not a final holdout; unchanged frozen policies and cached R2 controls.'))]:
    path=D/name;text=json.dumps(obj,indent=2)
    if path.exists():assert path.read_text()==text
    else:path.write_text(text)
print(json.dumps(dict(variants=len(variants),games=len(jobs),worlds=len(seeds))),flush=True)

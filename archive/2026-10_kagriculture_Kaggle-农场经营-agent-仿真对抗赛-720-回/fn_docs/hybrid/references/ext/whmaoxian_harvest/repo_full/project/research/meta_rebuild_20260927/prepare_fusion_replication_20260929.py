"""Replicate previously frozen promising combinations on the new development panel."""
from pathlib import Path
import json,hashlib
D=Path(__file__).resolve().parent;R=D.parents[1];sha=lambda b:hashlib.sha256(b).hexdigest()
old=json.loads((R/'research/production_upgrade_20260928/fusion_design.json').read_text())
worlds=json.loads((D/'herd_extended_design_20260929.json').read_text())
variants=[v for v in old['variants'] if v['name'] in ('finish','herd_finish')]
assert len(variants)==2
jobs=[]
for v in variants:
    assert sha((R/v['path']).read_bytes())==v['sha256']
    for op in worlds['roster']:
        for seed in worlds['seeds']:
            for seat in (0,1):
                j=dict(candidate=v['path'],opponent=op['path'],family=op['family'],panel=op['panel'],seed=seed,seat=seat,candidate_sha256=v['sha256'],opponent_sha256=sha((R/op['path']).read_bytes()))
                j['id']=sha(json.dumps(j,sort_keys=True).encode())[:24];jobs.append(j)
for name,obj in [('fusion_replication_jobs_20260929.json',jobs),('fusion_replication_design_20260929.json',dict(variants=variants,seeds=worlds['seeds'],roster=worlds['roster'],scope='Replication of pre-existing unchanged candidates on new development worlds, baseline cached in herd_extended_results_20260929.jsonl.'))]:
    path=D/name;data=json.dumps(obj,indent=2)
    if path.exists():assert path.read_text()==data
    else:path.write_text(data)
print(json.dumps(dict(candidates=len(variants),new_games=len(jobs))),flush=True)

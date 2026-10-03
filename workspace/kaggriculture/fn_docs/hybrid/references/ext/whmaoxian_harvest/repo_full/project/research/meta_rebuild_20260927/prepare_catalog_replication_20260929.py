"""Replicate source-reviewed historical candidates, without reusing their tuning worlds."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1];sha=lambda b:hashlib.sha256(b).hexdigest()
worlds=json.loads((D/'herd_extended_design_20260929.json').read_text())
choices=[('stack_all_gate','research/midgame_campaign_20260928/candidates/stack_all_gate.py','6b21eab0dd628f9324e5e55c410c9118b018c1da7159b24c764ac83b5244b064'),('sequence3','research/meta_rebuild_20260927/candidates/sequence_v2_early3_nomilk.py','cb2dbfc3d86a2dce6b36fab40b9383ab94b878b1c5557010ccd2f5afc69e5e90'),('scenario_herd','research/meta_rebuild_20260927/candidates/g3_robust.py','77004dee79d7d79acad0f1ebb0287f2f98912bff4f32e57fbce12463b5942982')]
variants=[];jobs=[]
for name,path,digest in choices:
    assert sha((R/path).read_bytes())==digest
    variants.append(dict(name=name,path=path,sha256=digest))
    for op in worlds['roster']:
        for seed in worlds['seeds']:
            for seat in (0,1):
                j=dict(candidate=path,opponent=op['path'],family=op['family'],panel=op['panel'],seed=seed,seat=seat,candidate_sha256=digest,opponent_sha256=sha((R/op['path']).read_bytes()))
                j['id']=sha(json.dumps(j,sort_keys=True).encode())[:24];jobs.append(j)
for name,obj in [('catalog_replication_jobs_20260929.json',jobs),('catalog_replication_design_20260929.json',dict(variants=variants,seeds=worlds['seeds'],roster=worlds['roster'],scope='Retrospectively selected candidates, prospectively checked on the new development panel. Not a reserved final holdout. Cached R2 controls are not new matches.'))]:
    path=D/name;text=json.dumps(obj,indent=2)
    if path.exists():assert path.read_text()==text
    else:path.write_text(text)
print(json.dumps(dict(variants=len(variants),games=len(jobs))),flush=True)

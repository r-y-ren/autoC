"""Evaluate two corrected herd policies on the declared development panel."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1]
sha=lambda b:hashlib.sha256(b).hexdigest()
all_variants=json.loads((D/'repeat_v2_candidates.json').read_text())
variants=[all_variants[0],all_variants[2]]
spec=json.loads((D/'herd_extended_design.json').read_text());jobs=[]
for v in variants:
    assert sha((R/v['path']).read_bytes())==v['sha256']
    for op in spec['roster']:
        for seed in spec['seeds']:
            for seat in (0,1):
                j=dict(candidate=v['path'],opponent=op['path'],family=op['family'],panel=op['panel'],seed=seed,seat=seat,candidate_sha256=v['sha256'],opponent_sha256=sha((R/op['path']).read_bytes()))
                j['id']=sha(json.dumps(j,sort_keys=True).encode())[:24];jobs.append(j)
for name,data in [('v2_extended_jobs.json',jobs),('v2_extended_design.json',dict(variants=variants,seeds=spec['seeds'],roster=spec['roster'],jobs=len(jobs),baseline_ledger='herd_extended_results.jsonl',scope='Development panel. Reuse checked frozen baseline, do not count it as new games.'))]:
    p=D/name;text=json.dumps(data,indent=2)
    if p.exists():assert p.read_text()==text
    else:p.write_text(text)
print(json.dumps(dict(cases=len(jobs))),flush=True)

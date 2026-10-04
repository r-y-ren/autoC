"""Freeze a fresh uniform development panel before any outcomes are inspected."""
from pathlib import Path
import hashlib,json,random
S=Path(__file__).resolve().parent;R=S.parents[1];D=R/'research/meta_rebuild_20260927'
sha=lambda b:hashlib.sha256(b).hexdigest()
design=json.loads((D/'midgame_herd_design.json').read_text())
variants=design['variants'];roster=design['roster']
rng=random.Random(202609281332);seeds=rng.sample(range(1,2147483647),16)
for v in variants:assert sha((R/v['path']).read_bytes())==v['sha256']
jobs=[]
for v in variants:
    for op in roster:
        for seed in seeds:
            for seat in (0,1):
                j=dict(candidate=v['path'],opponent=op['path'],family=op['family'],panel=op['panel'],seed=seed,seat=seat,candidate_sha256=v['sha256'],opponent_sha256=sha((R/op['path']).read_bytes()))
                j['id']=sha(json.dumps(j,sort_keys=True).encode())[:24];jobs.append(j)
plan=dict(variants=variants,roster=roster,seeds=seeds,cases=len(jobs),scope='Uniform development worlds, chosen before outcomes. No top-ten private programs or online rating claim. Official transition functions unchanged.')
for name,data in [('extended_design.json',plan),('extended_jobs.json',jobs)]:
    p=S/name;text=json.dumps(data,indent=2)
    if p.exists():assert p.read_text()==text
    else:p.write_text(text)
print(json.dumps(dict(cases=len(jobs),seeds=seeds)),flush=True)

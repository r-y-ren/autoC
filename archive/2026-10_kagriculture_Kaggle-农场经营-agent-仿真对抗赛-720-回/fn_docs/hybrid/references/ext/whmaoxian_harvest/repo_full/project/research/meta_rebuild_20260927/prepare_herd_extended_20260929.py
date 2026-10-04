"""Fresh development worlds for herd variants; immutable source hashes."""
from pathlib import Path
import hashlib,json,random
D=Path(__file__).resolve().parent;R=D.parents[1]
O=R/'research/herd_search_20260929';O.mkdir(exist_ok=True)
design=json.loads((D/'midgame_herd_design.json').read_text())
rng=random.Random(2026092917);seeds=rng.sample(range(100000,2147000000),16)
variants=design['variants'];roster=design['roster'];jobs=[]
def digest(p):return hashlib.sha256((R/p).read_bytes()).hexdigest()
for v in variants:
    assert digest(v['path'])==v['sha256']
    for op in roster:
        for seed in seeds:
            for seat in (0,1):
                j=dict(candidate=v['path'],opponent=op['path'],family=op['family'],panel=op['panel'],seed=seed,seat=seat,candidate_sha256=v['sha256'],opponent_sha256=digest(op['path']))
                j['id']=hashlib.sha256(json.dumps(j,sort_keys=True).encode()).hexdigest()[:24];jobs.append(j)
for name,data in [('herd_extended_jobs.json',jobs),('herd_extended_design.json',dict(variants=variants,roster=roster,seeds=seeds,jobs=len(jobs),scope='Fresh development worlds. No online rating inference; not final holdout.'))]:
    p=O/name;s=json.dumps(data,indent=2)
    if p.exists():assert p.read_text()==s
    else:p.write_text(s)
print(json.dumps(dict(jobs=len(jobs),worlds=len(seeds),output=str(O))),flush=True)

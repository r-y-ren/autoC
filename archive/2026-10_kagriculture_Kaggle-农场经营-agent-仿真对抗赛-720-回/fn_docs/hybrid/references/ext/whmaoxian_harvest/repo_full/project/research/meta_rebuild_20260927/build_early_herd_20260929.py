"""Reversible herd research candidates and explicit development manifests."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1]
sha=lambda b:hashlib.sha256(b).hexdigest()
base='submissions/release_v10_r2/main.py';raw=(R/base).read_bytes()
assert sha(raw)=='b35b5b09fbec059ab7cbd2ba67a9fbb6d3e467ef5262f3e2ddba592b3e50c1c4'
assert b'_K29_HERD_' not in raw
configs=[('early72_ev',72,False),('early72_nomilk',72,True),('early120_ev',120,False),('rearm144_ev',144,False)]
variants=[dict(name='r2',path=base,sha256=sha(raw))]
for name,start,nomilk in configs:
    constants=f'\n_K29_FROM={start}\n_K29_TO=360\n_K29_NO_MILK={nomilk!r}\n_K29_RATIO=1.1\n_K29_GAIN=600\n_K29_MIN_YARN=1\n'
    source=raw+constants.encode()+(D/'early_herd_tail_20260929.txt').read_bytes()
    path=D/'candidates'/(name+'.py');compile(source,str(path),'exec')
    if path.exists():assert path.read_bytes()==source
    else:path.write_bytes(source)
    variants.append(dict(name=name,path=path.relative_to(R).as_posix(),sha256=sha(source)))
previous=json.loads((D/'herd_extended_design_20260929.json').read_text())
seeds=previous['seeds'][:8]+[1799657451];roster=previous['roster'];jobs=[]
for v in variants:
    for op in roster:
        for seed in seeds:
            for seat in (0,1):
                j=dict(candidate=v['path'],opponent=op['path'],family=op['family'],panel=op['panel'],seed=seed,seat=seat,candidate_sha256=v['sha256'],opponent_sha256=sha((R/op['path']).read_bytes()))
                j['id']=sha(json.dumps(j,sort_keys=True).encode())[:24];jobs.append(j)
jobs=[j for j in jobs if j['candidate']!=base]
design=dict(variants=variants,roster=roster,seeds=seeds,jobs=len(jobs),baseline_ledgers=['herd_extended_results_20260929.jsonl','midgame_herd_results.jsonl'],scope='Eight new-development worlds plus one known-loss world; paired frozen baseline is reused, not counted as new games.')
for name,obj in [('early_herd_jobs_20260929.json',jobs),('early_herd_design_20260929.json',design)]:
    path=D/name;data=json.dumps(obj,indent=2)
    if path.exists():assert path.read_text()==data
    else:path.write_text(data)
print(json.dumps(dict(candidates=len(variants)-1,new_cases=len(jobs),worlds=len(seeds))),flush=True)

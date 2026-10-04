"""Finite capacity-preservation ablations; keep every frozen release unchanged."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1];sha=lambda b:hashlib.sha256(b).hexdigest()
base='submissions/release_v10_r2/main.py';raw=(R/base).read_bytes()
assert sha(raw)=='b35b5b09fbec059ab7cbd2ba67a9fbb6d3e467ef5262f3e2ddba592b3e50c1c4'
assert b'_K29C_' not in raw
prior=json.loads((D/'herd_extended_design_20260929.json').read_text())
seeds=prior['seeds'][:8]+[1799657451];variants=[];jobs=[]
for name,sign,book in [('cap_cheap_book',1,True),('cap_value_book',-1,True),('cap_cheap_raw',1,False),('cap_value_raw',-1,False)]:
    constants=f'\n_K29C_PRICE_SIGN={sign}\n_K29C_BOOK={book!r}\n_K29C_FROM=360\n_K29C_WHEAT_BUFFER=2\n_K29C_FERT_RESERVE=2\n'
    source=raw+constants.encode()+(D/'capacity_guard_tail_20260929.txt').read_bytes()
    path=D/'candidates'/(name+'.py');compile(source,str(path),'exec')
    if path.exists():assert path.read_bytes()==source
    else:path.write_bytes(source)
    v=dict(name=name,path=path.relative_to(R).as_posix(),sha256=sha(source));variants.append(v)
    for op in prior['roster']:
        for seed in seeds:
            for seat in (0,1):
                j=dict(candidate=v['path'],opponent=op['path'],family=op['family'],panel=op['panel'],seed=seed,seat=seat,candidate_sha256=v['sha256'],opponent_sha256=sha((R/op['path']).read_bytes()))
                j['id']=sha(json.dumps(j,sort_keys=True).encode())[:24];jobs.append(j)
smoke=[j for j in jobs if j['seed'] in (seeds[0],1799657451) and j['family'] in ('r2','fieldcraft')]
design=dict(variants=variants,seeds=seeds,roster=prior['roster'],scope='Development only. Baseline from explicitly matched prior ledgers. Capacity is checked at the actual day boundary, not estimated from total produced goods.')
for name,obj in [('capacity_smoke_jobs_20260929.json',smoke),('capacity_jobs_20260929.json',jobs),('capacity_design_20260929.json',design)]:
    path=D/name;data=json.dumps(obj,indent=2)
    if path.exists():assert path.read_text()==data
    else:path.write_text(data)
print(json.dumps(dict(candidates=len(variants),smoke=len(smoke),full=len(jobs))),flush=True)

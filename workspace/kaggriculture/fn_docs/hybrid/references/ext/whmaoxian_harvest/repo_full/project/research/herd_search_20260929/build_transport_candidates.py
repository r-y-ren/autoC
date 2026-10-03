"""Combine repeated herd allocation with product-correct transport."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1]
sha=lambda b:hashlib.sha256(b).hexdigest()
design=json.loads((D/'repeated_design.json').read_text());variants=[];jobs=[]
for parent in design['variants']:
    if parent['name'] not in ('repeat_early','repeat_ev'):continue
    raw=(R/parent['path']).read_bytes();assert sha(raw)==parent['sha256']
    source=raw+(D/'herd_transport_tail.txt').read_bytes()
    p=D/'candidates'/(parent['name']+'_transport.py');compile(source,str(p),'exec')
    if p.exists():assert p.read_bytes()==source
    else:p.write_bytes(source)
    v=dict(name=p.stem,path=p.relative_to(R).as_posix(),sha256=sha(source),parent=parent['path']);variants.append(v)
    for op in design['roster']:
        for seed in design['seeds']:
            for seat in (0,1):
                j=dict(candidate=v['path'],opponent=op['path'],family=op['family'],panel=op['panel'],seed=seed,seat=seat,candidate_sha256=v['sha256'],opponent_sha256=sha((R/op['path']).read_bytes()))
                j['id']=sha(json.dumps(j,sort_keys=True).encode())[:24];jobs.append(j)
for name,data in [('transport_jobs.json',jobs),('transport_design.json',dict(variants=variants,seeds=design['seeds'],roster=design['roster'],scope='Development only; additional delivery requests must be verified as actual game gain.'))]:
    p=D/name;s=json.dumps(data,indent=2)
    if p.exists():assert p.read_text()==s
    else:p.write_text(s)
print(json.dumps(dict(variants=len(variants),jobs=len(jobs))),flush=True)

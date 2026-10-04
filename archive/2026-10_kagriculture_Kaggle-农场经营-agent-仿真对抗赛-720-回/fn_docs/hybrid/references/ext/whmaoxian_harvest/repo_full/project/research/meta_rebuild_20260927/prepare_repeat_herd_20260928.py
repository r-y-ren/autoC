"""Build repeated-herd candidates; no modifications to release code."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1];BASE='submissions/release_v10_r2/main.py'
sha=lambda b:hashlib.sha256(b).hexdigest()
raw=(R/BASE).read_bytes();assert sha(raw)=='b35b5b09fbec059ab7cbd2ba67a9fbb6d3e467ef5262f3e2ddba592b3e50c1c4'
assert b'_K28S_' not in raw
variants=[]
settings=[('repeat_one',1,150,600,False,False),('repeat_two',2,150,600,False,False),('repeat_three',3,150,600,False,False),('repeat_nomilk',3,150,600,True,False),('repeat_repair',3,150,600,False,True),('repeat_lowreserve',3,25,600,False,True)]
for name,limit,reserve,gain,nomilk,repair in settings:
    cfg=dict(FROM=72,TO=264,COW_FLOOR=2,LIMIT=limit,RESERVE=reserve,MIN_GAIN=gain,NO_MILK=nomilk,REPAIR=repair)
    data=raw+('\n'+''.join('_K28S_'+k+'='+repr(v)+'\n' for k,v in cfg.items())).encode()+(D/'repeat_herd_policy_20260928.txt').read_bytes()
    path=D/'candidates'/(name+'.py');compile(data,str(path),'exec')
    if path.exists():assert path.read_bytes()==data
    else:path.write_bytes(data)
    variants.append(dict(name=name,path=path.relative_to(R).as_posix(),sha256=sha(data),parameters=cfg))
jobs=[]
for v in variants:
    for seat in (0,1):
        j=dict(candidate=v['path'],opponent=BASE,family='r2',panel='mechanism_diagnostic',seed=1799657451,seat=seat,candidate_sha256=v['sha256'],opponent_sha256=sha(raw))
        j['id']=sha(json.dumps(j,sort_keys=True).encode())[:24];jobs.append(j)
for name,data in [('repeat_herd_design_20260928.json',dict(variants=variants,scope='Known-world mechanism screening. Not rating validation.')),('repeat_herd_smoke_jobs_20260928.json',jobs)]:
    p=D/name; text=json.dumps(data,indent=2)
    if p.exists():assert p.read_text()==text
    else:p.write_text(text)
print(json.dumps(dict(variants=len(variants),cases=len(jobs))),flush=True)

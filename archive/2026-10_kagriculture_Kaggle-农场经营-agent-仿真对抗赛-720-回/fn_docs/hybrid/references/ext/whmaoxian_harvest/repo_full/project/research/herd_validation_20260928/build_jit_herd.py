"""Build two bounded just-in-time livestock procurement candidates."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1]
sha=lambda b:hashlib.sha256(b).hexdigest()
parent=next(v for v in json.loads((D/'repeat_v2_candidates.json').read_text()) if v['name']=='early_two_v2')
raw=(R/parent['path']).read_bytes();assert sha(raw)==parent['sha256']
variants=[]
for reserve in (100,50):
    name='jit_herd_'+str(reserve)
    data=raw+('\n_JT28_RESERVE='+str(reserve)+'\n').encode()+(D/'jit_herd_tail.txt').read_bytes()
    p=D/(name+'.py');compile(data,str(p),'exec')
    if p.exists():assert p.read_bytes()==data
    else:p.write_bytes(data)
    variants.append(dict(name=name,path=p.relative_to(R).as_posix(),sha256=sha(data),reserve=reserve))
(D/'jit_candidates.json').write_text(json.dumps(variants,indent=2))
spec=json.loads((D/'repeat_design.json').read_text());jobs=[]
for v in variants:
    for op in spec['roster']:
        for seed in spec['seeds']:
            for seat in (0,1):
                j=dict(candidate=v['path'],opponent=op['path'],family=op['family'],panel=op['panel'],seed=seed,seat=seat,candidate_sha256=v['sha256'],opponent_sha256=sha((R/op['path']).read_bytes()))
                j['id']=sha(json.dumps(j,sort_keys=True).encode())[:24];jobs.append(j)
(D/'jit_jobs.json').write_text(json.dumps(jobs,indent=2))
(D/'jit_design.json').write_text(json.dumps(dict(variants=variants,seeds=spec['seeds'],roster=spec['roster'],scope='Development smoke: delayed payment, unchanged planned pickup and placement times.'),indent=2))
print(json.dumps(dict(cases=len(jobs),candidates=len(variants))),flush=True)

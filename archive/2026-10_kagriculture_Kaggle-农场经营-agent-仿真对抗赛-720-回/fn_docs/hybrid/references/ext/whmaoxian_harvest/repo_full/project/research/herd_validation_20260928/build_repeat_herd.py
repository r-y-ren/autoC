"""Build bounded early/repeated herd variants without modifying the frozen agent."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1]
base='submissions/release_v10_r2/main.py';raw=(R/base).read_bytes()
sha=lambda b:hashlib.sha256(b).hexdigest()
assert sha(raw)=='b35b5b09fbec059ab7cbd2ba67a9fbb6d3e467ef5262f3e2ddba592b3e50c1c4'
assert b'_HG28_' not in raw
common=dict(start=72,stop=288,max_swaps=1,no_milk=False,ratio=0,gain=-1000000,reserve=100)
settings=[('early_one',{}),('early_two',dict(max_swaps=2)),('repeat_selective',dict(max_swaps=4,ratio=1.1,gain=600)),('repeat_nomilk',dict(max_swaps=4,no_milk=True))]
variants=[dict(name='r2',path=base,sha256=sha(raw))]
for name,patch in settings:
    cfg=dict(common,**patch)
    data=raw+('\n_HG28_CFG='+repr(cfg)+'\n').encode()+(D/'repeat_herd_tail.txt').read_bytes()
    p=D/(name+'.py');compile(data,str(p),'exec')
    if p.exists():assert p.read_bytes()==data
    else:p.write_bytes(data)
    variants.append(dict(name=name,path=p.relative_to(R).as_posix(),sha256=sha(data),config=cfg))
spec=json.loads((D/'herd_extended_design.json').read_text());seeds=[1799657451]+spec['seeds'][:3];jobs=[]
for v in variants:
    for op in spec['roster']:
        for seed in seeds:
            for seat in (0,1):
                j=dict(candidate=v['path'],opponent=op['path'],family=op['family'],panel=op['panel'],seed=seed,seat=seat,candidate_sha256=v['sha256'],opponent_sha256=sha((R/op['path']).read_bytes()))
                j['id']=sha(json.dumps(j,sort_keys=True).encode())[:24];jobs.append(j)
for name,data in [('repeat_design.json',dict(variants=variants,seeds=seeds,roster=spec['roster'],jobs=len(jobs),scope='Development-only repeated substitution screen')),('repeat_jobs.json',jobs)]:
    p=D/name;text=json.dumps(data,indent=2)
    if p.exists():assert p.read_text()==text
    else:p.write_text(text)
print(json.dumps(dict(cases=len(jobs),variants=len(variants))),flush=True)

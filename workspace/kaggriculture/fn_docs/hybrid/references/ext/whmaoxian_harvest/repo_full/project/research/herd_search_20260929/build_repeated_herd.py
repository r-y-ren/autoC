"""Mechanism screening for earlier/repeated herd substitution."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1]
def sha(data):return hashlib.sha256(data).hexdigest()
raw=(R/'submissions/release_v10_r2/main.py').read_bytes()
assert sha(raw)=='b35b5b09fbec059ab7cbd2ba67a9fbb6d3e467ef5262f3e2ddba592b3e50c1c4'
assert b'_K29_' not in raw
base=dict(milk=False,start=72,end=288,min_cows=2,max_sheep=16,ratio=0,gain=-1000000,cash=650,repeat=True,care_model=False)
settings=[('early_one',dict(cash=0,repeat=False)),('repeat_safe',{}),
 ('repeat_early',dict(cash=0)),('repeat_ev',dict(ratio=1.1,gain=600)),
 ('repeat_keep4',dict(min_cows=4)),('repeat_care_ev',dict(milk=True,care_model=True,ratio=1.1,gain=600))]
folder=D/'candidates';folder.mkdir(exist_ok=True);variants=[]
for name,patch in settings:
    cfg=dict(base,**patch);source=raw+('\n_K29_CFG='+repr(cfg)+'\n').encode()+(D/'repeated_herd_tail.txt').read_bytes()
    p=folder/(name+'.py');compile(source,str(p),'exec')
    if p.exists():assert p.read_bytes()==source
    else:p.write_bytes(source)
    variants.append(dict(name=name,path=p.relative_to(R).as_posix(),sha256=sha(source),config=cfg))
prior=json.loads((D/'herd_extended_design.json').read_text());seeds=[1799657451]+prior['seeds'][:4];jobs=[]
for v in variants:
    for op in prior['roster']:
        for seed in seeds:
            for seat in (0,1):
                j=dict(candidate=v['path'],opponent=op['path'],family=op['family'],panel=op['panel'],seed=seed,seat=seat,candidate_sha256=v['sha256'],opponent_sha256=sha((R/op['path']).read_bytes()))
                j['id']=sha(json.dumps(j,sort_keys=True).encode())[:24];jobs.append(j)
for name,data in [('repeated_jobs.json',jobs),('repeated_design.json',dict(variants=variants,seeds=seeds,roster=prior['roster'],scope='Development screen; 1 known-loss world plus 4 declared development worlds.'))]:
    p=D/name;s=json.dumps(data,indent=2)
    if p.exists():assert p.read_text()==s
    else:p.write_text(s)
print(json.dumps(dict(candidates=len(variants),jobs=len(jobs))),flush=True)

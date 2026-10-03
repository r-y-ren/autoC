"""Evaluate animal retirement and pasture reuse in complete closed-loop matches."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1];sha=lambda b:hashlib.sha256(b).hexdigest()
raw=(R/'submissions/release_v10_r2/main.py').read_bytes()
assert sha(raw)=='b35b5b09fbec059ab7cbd2ba67a9fbb6d3e467ef5262f3e2ddba592b3e50c1c4'
assert b'_K29R_' not in raw
base=dict(start=20,end=25,price=25,cap=8,daily=2,forecast=3,crop='CARROT',crop_factor=.6)
settings=[('retire_only',dict(crop=None)),('retire_carrot',{}),('retire_wheat',dict(crop='WHEAT')),('retire_early',dict(start=17)),('retire_late',dict(start=23,price=40,cap=12,daily=4)),('retire_selective',dict(cap=4,forecast=5,crop_factor=.3))]
prior=json.loads((D/'herd_extended_design_20260929.json').read_text())
seeds=prior['seeds'][:6];roster=[op for op in prior['roster'] if op['family'] in ('r2','fieldcraft','dmitrii','top_style_02')]
variants=[];jobs=[]
for name,patch in settings:
    cfg=dict(base,**patch);source=raw+('\n_K29R_CFG='+repr(cfg)+'\n').encode()+(D/'retirement_tail_20260929.txt').read_bytes()
    path=D/'candidates'/(name+'.py');compile(source,str(path),'exec')
    if path.exists():assert path.read_bytes()==source
    else:path.write_bytes(source)
    v=dict(name=name,path=path.relative_to(R).as_posix(),sha256=sha(source),settings=cfg);variants.append(v)
    for op in roster:
        for seed in seeds:
            for seat in (0,1):
                j=dict(candidate=v['path'],opponent=op['path'],family=op['family'],panel=op['panel'],seed=seed,seat=seat,candidate_sha256=v['sha256'],opponent_sha256=sha((R/op['path']).read_bytes()))
                j['id']=sha(json.dumps(j,sort_keys=True).encode())[:24];jobs.append(j)
for name,obj in [('retirement_design_20260929.json',dict(variants=variants,roster=roster,seeds=seeds,scope='New structural production policy, development screening only. Retains movement, explicitly stops feeding selected loss-making sites and repurposes them.')),('retirement_jobs_20260929.json',jobs)]:
    path=D/name;text=json.dumps(obj,indent=2)
    if path.exists():assert path.read_text()==text
    else:path.write_text(text)
print(json.dumps(dict(variants=len(variants),games=len(jobs))),flush=True)

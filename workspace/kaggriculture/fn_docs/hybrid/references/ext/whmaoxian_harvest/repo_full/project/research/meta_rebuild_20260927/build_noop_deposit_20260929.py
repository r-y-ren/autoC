"""Immediate no-op-only delivery variants; zero worker rerouting."""
from pathlib import Path
import json,hashlib
D=Path(__file__).resolve().parent;R=D.parents[1];sha=lambda b:hashlib.sha256(b).hexdigest()
raw=(R/'submissions/release_v10_r2/main.py').read_bytes()
assert sha(raw)=='b35b5b09fbec059ab7cbd2ba67a9fbb6d3e467ef5262f3e2ddba592b3e50c1c4'
assert b'_K29P_' not in raw
prior=json.loads((D/'herd_extended_design_20260929.json').read_text())
seeds=prior['seeds'][:6];roster=prior['roster'];variants=[];jobs=[]
configs=[('depot_only',dict(hour=0,sell=False,book=False)),('depot_sell',dict(hour=0,sell=True,book=True)),('depot_late',dict(hour=16,sell=True,book=True)),('depot_raw',dict(hour=0,sell=True,book=False))]
for name,cfg in configs:
    source=raw+('\n_K29P_CFG='+repr(cfg)+'\n').encode()+(D/'noop_deposit_tail_20260929.txt').read_bytes()
    path=D/'candidates'/(name+'.py');compile(source,str(path),'exec')
    if path.exists():assert path.read_bytes()==source
    else:path.write_bytes(source)
    v=dict(name=name,path=path.relative_to(R).as_posix(),sha256=sha(source),settings=cfg);variants.append(v)
    for op in roster:
        for seed in seeds:
            for seat in (0,1):
                j=dict(candidate=v['path'],opponent=op['path'],family=op['family'],panel=op['panel'],seed=seed,seat=seat,candidate_sha256=v['sha256'],opponent_sha256=sha((R/op['path']).read_bytes()))
                j['id']=sha(json.dumps(j,sort_keys=True).encode())[:24];jobs.append(j)
for name,obj in [('noop_deposit_design_20260929.json',dict(variants=variants,seeds=seeds,roster=roster,scope='Every replacement requires a current physical no-op, equal post-action farm/seeds and nondecreasing commodity totals. Future market effects still require empirical evaluation.')),('noop_deposit_jobs_20260929.json',jobs)]:
    path=D/name;text=json.dumps(obj,indent=2)
    if path.exists():assert path.read_text()==text
    else:path.write_text(text)
print(json.dumps(dict(variants=len(variants),games=len(jobs))),flush=True)

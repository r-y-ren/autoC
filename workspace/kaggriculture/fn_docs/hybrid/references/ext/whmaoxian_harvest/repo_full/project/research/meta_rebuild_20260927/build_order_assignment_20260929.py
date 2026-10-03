"""Order-assignment counterfactuals; quantities and physical actions are unchanged."""
from pathlib import Path
import json,hashlib
D=Path(__file__).resolve().parent;R=D.parents[1];sha=lambda b:hashlib.sha256(b).hexdigest()
raw=(R/'submissions/release_v10_r2/main.py').read_bytes()
assert sha(raw)=='b35b5b09fbec059ab7cbd2ba67a9fbb6d3e467ef5262f3e2ddba592b3e50c1c4'
assert b'_K29O_' not in raw
prior=json.loads((D/'herd_extended_design_20260929.json').read_text())
seeds=prior['seeds'][:6];roster=prior['roster'];variants=[];jobs=[]
configs=[('order_native',dict(mode='native',gate=.9,alpha=1.,gain=2.,risk=100000)),('order_mirror',dict(mode='mirror',gate=.9,alpha=1.,gain=2.,risk=100000)),('order_mixed',dict(mode='mixed',gate=.9,alpha=1.,gain=5.,risk=100)),('order_broad',dict(mode='mixed',gate=0.,alpha=1.,gain=5.,risk=50))]
for name,cfg in configs:
    source=raw+('\n_K29O_CFG='+repr(cfg)+'\n').encode()+(D/'order_assignment_tail_20260929.txt').read_bytes()
    path=D/'candidates'/(name+'.py');compile(source,str(path),'exec')
    if path.exists():assert path.read_bytes()==source
    else:path.write_bytes(source)
    v=dict(name=name,path=path.relative_to(R).as_posix(),sha256=sha(source),settings=cfg);variants.append(v)
    for op in roster:
        for seed in seeds:
            for seat in (0,1):
                j=dict(candidate=v['path'],opponent=op['path'],family=op['family'],panel=op['panel'],seed=seed,seat=seat,candidate_sha256=v['sha256'],opponent_sha256=sha((R/op['path']).read_bytes()))
                j['id']=sha(json.dumps(j,sort_keys=True).encode())[:24];jobs.append(j)
for name,obj in [('order_assignment_design_20260929.json',dict(variants=variants,seeds=seeds,roster=roster,scope='Best response to explicit public-observation-based order scenarios. Expected gain is not observed opponent behavior or verified actual gain.')),('order_assignment_jobs_20260929.json',jobs)]:
    path=D/name;text=json.dumps(obj,indent=2)
    if path.exists():assert path.read_text()==text
    else:path.write_text(text)
print(json.dumps(dict(variants=len(variants),games=len(jobs))),flush=True)

"""Test initial herd portfolios; no extra animal count or worker movement."""
from pathlib import Path
import hashlib,json
S=Path(__file__).resolve().parent;R=S.parents[1];sha=lambda b:hashlib.sha256(b).hexdigest()
raw=(R/'submissions/release_v10_r2/main.py').read_bytes()
assert sha(raw)=='b35b5b09fbec059ab7cbd2ba67a9fbb6d3e467ef5262f3e2ddba592b3e50c1c4'
variants=[]
for delta in (-2,-1,1,2):
    name=f'opening_c{2+delta}s{2-delta}'
    data=raw+f'\n_K28O_DELTA={delta}\n'.encode()+(S/'opening_mix_overlay.txt').read_bytes()
    p=S/'candidates'/(name+'.py');compile(data,str(p),'exec')
    if p.exists():assert p.read_bytes()==data
    else:p.write_bytes(data)
    variants.append(dict(name=name,path=p.relative_to(R).as_posix(),sha256=sha(data),cows=2+delta,sheep=2-delta))
plan=json.loads((S/'extended_design.json').read_text());seeds=plan['seeds'][:4];jobs=[]
for v in variants:
    for op in plan['roster']:
        for seed in seeds:
            for seat in (0,1):
                j=dict(candidate=v['path'],opponent=op['path'],family=op['family'],panel=op['panel'],seed=seed,seat=seat,candidate_sha256=v['sha256'],opponent_sha256=sha((R/op['path']).read_bytes()))
                j['id']=sha(json.dumps(j,sort_keys=True).encode())[:24];jobs.append(j)
report=dict(variants=variants,roster=plan['roster'],seeds=seeds,cases=len(jobs),scope='Initial-portfolio development screening. Includes cash-flow effects; not an isolated estimate of animal yield.')
for suffix,data in [('jobs',jobs),('design',report)]:
    p=S/f'opening_mix_{suffix}.json';text=json.dumps(data,indent=2)
    if p.exists():assert p.read_text()==text
    else:p.write_text(text)
print(json.dumps(dict(candidates=len(variants),cases=len(jobs))),flush=True)

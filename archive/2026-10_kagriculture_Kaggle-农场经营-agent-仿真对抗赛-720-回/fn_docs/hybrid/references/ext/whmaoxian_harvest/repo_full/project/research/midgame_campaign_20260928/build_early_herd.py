"""Earlier adaptive production via the existing confirmed herd mechanism."""
from pathlib import Path
import hashlib,json
S=Path(__file__).resolve().parent;R=S.parents[1];sha=lambda b:hashlib.sha256(b).hexdigest()
raw=(R/'submissions/release_v10_r2/main.py').read_bytes()
assert sha(raw)=='b35b5b09fbec059ab7cbd2ba67a9fbb6d3e467ef5262f3e2ddba592b3e50c1c4'
settings=[('herd8',3,11,8,100),('herd12',3,11,12,100),('herd16',3,14,16,250),
          ('herd_mid',6,11,12,100),('herd_cash',3,11,12,600),('herd_growth',3,11,16,0)]
variants=[]
for name,begin,end,target,reserve in settings:
    genome={'from':begin,'to':end,'target':target,'reserve':reserve}
    data=raw+('\n_K28Y_GENOME='+repr(genome)+'\n').encode()+(S/'early_herd_overlay.txt').read_bytes()
    p=S/'candidates'/(name+'.py');compile(data,str(p),'exec')
    if p.exists():assert p.read_bytes()==data
    else:p.write_bytes(data)
    variants.append(dict(name=name,path=p.relative_to(R).as_posix(),sha256=sha(data),genome=genome))
plan=json.loads((S/'extended_design.json').read_text());seeds=[1205068858,1402772681,2095943143,2140042026]+plan['seeds'][:2]
jobs=[]
for v in variants:
    for op in plan['roster']:
        for seed in seeds:
            for seat in (0,1):
                j=dict(candidate=v['path'],opponent=op['path'],family=op['family'],panel=op['panel'],seed=seed,seat=seat,candidate_sha256=v['sha256'],opponent_sha256=sha((R/op['path']).read_bytes()))
                j['id']=sha(json.dumps(j,sort_keys=True).encode())[:24];jobs.append(j)
report=dict(variants=variants,roster=plan['roster'],seeds=seeds,cases=len(jobs),scope='Development screening: four activation worlds and two controls. R2 controls reused from extended ledger, not re-counted.')
for suffix,data in [('jobs',jobs),('design',report)]:
    p=S/f'early_herd_{suffix}.json';text=json.dumps(data,indent=2)
    if p.exists():assert p.read_text()==text
    else:p.write_text(text)
print(json.dumps(dict(candidates=len(variants),cases=len(jobs))),flush=True)

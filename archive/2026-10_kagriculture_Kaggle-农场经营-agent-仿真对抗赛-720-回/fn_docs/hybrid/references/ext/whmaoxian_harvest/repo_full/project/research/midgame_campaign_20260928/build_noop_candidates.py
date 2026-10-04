"""No-op physical-action recovery candidates, isolated from sale/route changes."""
from pathlib import Path
import hashlib,json
S=Path(__file__).resolve().parent;R=S.parents[1];sha=lambda b:hashlib.sha256(b).hexdigest()
raw=(R/'submissions/release_v10_r2/main.py').read_bytes()
assert sha(raw)=='b35b5b09fbec059ab7cbd2ba67a9fbb6d3e467ef5262f3e2ddba592b3e50c1c4'
configs=[('noop_care',('CARE',),144,85),('noop_fertilizer',('COLLECT_FERTILIZER',),144,85),
         ('noop_harvest',('HARVEST',),144,85),('noop_combined',('CARE','COLLECT_FERTILIZER','HARVEST'),144,85)]
variants=[]
for name,ops,begin,capacity in configs:
    genome=dict(ops=ops,begin=begin,capacity=capacity)
    source=raw+('\n_K28N_CFG='+repr(genome)+'\n').encode()+(S/'noop_recovery_tail.py.txt').read_bytes()
    path=S/'candidates'/(name+'.py');compile(source,str(path),'exec')
    if path.exists():assert path.read_bytes()==source
    else:path.write_bytes(source)
    variants.append(dict(name=name,path=path.relative_to(R).as_posix(),sha256=sha(source),genome=genome))
plan=json.loads((S/'extended_design.json').read_text());jobs=[]
for v in variants:
    for op in plan['roster']:
        for seed in plan['seeds'][:4]:
            for seat in (0,1):
                j=dict(candidate=v['path'],opponent=op['path'],family=op['family'],panel=op['panel'],seed=seed,seat=seat,candidate_sha256=v['sha256'],opponent_sha256=sha((R/op['path']).read_bytes()))
                j['id']=sha(json.dumps(j,sort_keys=True).encode())[:24];jobs.append(j)
for name,data in [('noop_candidates.json',variants),('noop_jobs.json',jobs)]:
    p=S/name;text=json.dumps(data,indent=2)
    if p.exists():assert p.read_text()==text
    else:p.write_text(text)
print(json.dumps(dict(candidates=len(variants),development_games=len(jobs))),flush=True)

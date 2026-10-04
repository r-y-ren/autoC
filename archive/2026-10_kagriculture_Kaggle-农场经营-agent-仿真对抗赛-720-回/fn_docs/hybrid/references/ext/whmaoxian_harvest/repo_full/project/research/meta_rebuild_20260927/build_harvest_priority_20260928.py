"""Service-transport follow-up on declared difficult development scenarios."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1];sha=lambda b:hashlib.sha256(b).hexdigest()
parent='research/meta_rebuild_20260927/candidates/sequence_v2_early3_nomilk.py'
raw=(R/parent).read_bytes()
assert sha(raw)=='cb2dbfc3d86a2dce6b36fab40b9383ab94b878b1c5557010ccd2f5afc69e5e90'
tail=(D/'sheep_harvest_priority_20260928.txt').read_text();assert tail.count(';claimed=set()')==1
tail=tail.replace(';claimed=set()',";claimed={tuple(pos) for actor,pos in enumerate(positions[:len(commands)]) if commands[actor]==['HARVEST']}")
variants=[dict(name='sequence_v2_early3_nomilk',path=parent,sha256=sha(raw))]
for ratio in (1,3,6):
    name='harvest_priority_'+str(ratio);data=raw+('\n_SH29_RATIO='+str(ratio)+'\n').encode()+tail.encode()
    path=D/'candidates'/(name+'.py');compile(data,str(path),'exec')
    if path.exists():assert path.read_bytes()==data
    else:path.write_bytes(data)
    variants.append(dict(name=name,path=path.relative_to(R).as_posix(),sha256=sha(data)))
seeds=[1799657451,1067615585,1853178855,255678238,1017976877,1920980041]
roster=json.loads((D/'herd_extension_design.json').read_text())['roster'];jobs=[]
for v in variants:
    for op in roster:
        for seed in seeds:
            for seat in (0,1):
                j=dict(candidate=v['path'],opponent=op['path'],family=op['family'],panel=op['panel'],seed=seed,seat=seat,candidate_sha256=v['sha256'],opponent_sha256=sha((R/op['path']).read_bytes()))
                j['id']=sha(json.dumps(j,sort_keys=True).encode())[:24];jobs.append(j)
for name,obj in [('harvest_priority_design.json',dict(variants=variants,roster=roster,seeds=seeds,cases=len(jobs),scope='Known development cases, including milk-demand negative controls. Repeated executions are not independent worlds.')),('harvest_priority_jobs.json',jobs)]:
    path=D/name;text=json.dumps(obj,indent=2)
    if path.exists():assert path.read_text()==text
    else:path.write_text(text)
print(json.dumps({'variants':len(variants),'cases':len(jobs)}),flush=True)

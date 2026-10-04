"""Causal midgame herd pilot; all seeds are development, never rating evidence."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent; R=D.parents[1]; baseline='submissions/release_v10_r2/main.py'
raw=(R/baseline).read_bytes(); sha=lambda b:hashlib.sha256(b).hexdigest()
assert sha(raw)=='b35b5b09fbec059ab7cbd2ba67a9fbb6d3e467ef5262f3e2ddba592b3e50c1c4'
assert b'_K28_' not in raw
configs=[('yarn_sheep',False,0,-1000000),('yarn_selective',False,1.1,600),('yarn_nomilk',True,0,-1000000)]
variants=[dict(name='r2',path=baseline,sha256=sha(raw))]
for name,nomilk,ratio,gain in configs:
    constants=f'\n_K28_NO_MILK={nomilk!r}\n_K28_RATIO={ratio!r}\n_K28_GAIN={gain!r}\n'
    data=raw+constants.encode()+(D/'midgame_herd_tail_20260928.txt').read_bytes()
    path=D/'candidates'/('midgame_'+name+'.py');compile(data,str(path),'exec')
    if path.exists():assert path.read_bytes()==data
    else:path.write_bytes(data)
    variants.append(dict(name=name,path=path.relative_to(R).as_posix(),sha256=sha(data)))
roster=json.loads((D/'value_extended_design.json').read_text())['roster']
seeds=[1799657451];jobs=[]
for v in variants:
    for op in roster:
        for seed in seeds:
            for seat in (0,1):
                j=dict(candidate=v['path'],opponent=op['path'],family=op['family'],panel=op['panel'],seed=seed,seat=seat,candidate_sha256=v['sha256'],opponent_sha256=sha((R/op['path']).read_bytes()))
                j['id']=sha(json.dumps(j,sort_keys=True).encode())[:24];jobs.append(j)
for name,data in [('midgame_herd_jobs.json',jobs),('midgame_herd_design.json',dict(variants=variants,seeds=seeds,roster=roster,scope='Known-loss world: mechanism diagnostic, not heldout validation.'))]:
    path=D/name;text=json.dumps(data,indent=2)
    if path.exists():assert path.read_text()==text
    else:path.write_text(text)
print(json.dumps(dict(candidates=len(variants)-1,cases=len(jobs))),flush=True)

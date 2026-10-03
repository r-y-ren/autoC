"""Fresh-world screening, frozen releases and old result ledgers are read-only."""
from pathlib import Path
import hashlib,json,random
D=Path(__file__).resolve().parent;R=D.parents[1];BASE='submissions/release_v10_r2/main.py'
sha=lambda data:hashlib.sha256(data).hexdigest()
raw=(R/BASE).read_bytes();assert sha(raw)=='b35b5b09fbec059ab7cbd2ba67a9fbb6d3e467ef5262f3e2ddba592b3e50c1c4'
variants=[]
for name,nomilk,ratio,gain in [('early_yarn',False,0,-1000000),('early_selective',False,1.1,600),('early_nomilk',True,0,-1000000)]:
    text=f'\n_K28E_NO_MILK={nomilk!r}\n_K28E_RATIO={ratio!r}\n_K28E_GAIN={gain!r}\n'
    data=raw+text.encode()+(D/'early_herd_20260928.txt').read_bytes()
    path=D/'candidates'/(name+'.py');compile(data,str(path),'exec')
    if path.exists():assert path.read_bytes()==data
    else:path.write_bytes(data)
    variants.append(dict(name=name,path=path.relative_to(R).as_posix(),sha256=sha(data)))
for name,path in [('r2',BASE),('late_yarn','candidates/midgame_yarn_sheep.py'),('late_selective','candidates/midgame_yarn_selective.py'),('late_nomilk','candidates/midgame_yarn_nomilk.py'),('care','candidates/late_care.py'),('pred_off','candidates/fixed_pred_off.py'),('advance_off','candidates/fixed_advance_off.py')]:
    p=R/path if path==BASE else D/path
    variants.append(dict(name=name,path=p.relative_to(R).as_posix(),sha256=sha(p.read_bytes())))
roster=json.loads((D/'midgame_herd_design.json').read_text())['roster']
seeds=random.Random(202609281204).sample(range(1,2147483647),16);jobs=[]
for v in variants:
    for op in roster:
        for seed in seeds:
            for seat in (0,1):
                j=dict(candidate=v['path'],opponent=op['path'],family=op['family'],panel=op['panel'],seed=seed,seat=seat,candidate_sha256=v['sha256'],opponent_sha256=sha((R/op['path']).read_bytes()))
                j['id']=sha(json.dumps(j,sort_keys=True).encode())[:24];jobs.append(j)
design=dict(variants=variants,seeds=seeds,roster=roster,cases=len(jobs),scope='Sixteen fresh DEVELOPMENT worlds; both seats. No online rating inference.')
for name,data in [('herd_extended_20260928_design.json',design),('herd_extended_20260928_jobs.json',jobs)]:
    p=D/name;text=json.dumps(data,indent=2)
    if p.exists():assert p.read_text()==text
    else:p.write_text(text)
print(json.dumps(dict(variants=len(variants),worlds=len(seeds),cases=len(jobs))),flush=True)

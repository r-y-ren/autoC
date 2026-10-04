"""Finite virtual-game opening procurement ablations; no online submission."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1]
base=(R/'submissions/release_v10_r2/main.py').read_bytes()
assert hashlib.sha256(base).hexdigest()=='b35b5b09fbec059ab7cbd2ba67a9fbb6d3e467ef5262f3e2ddba592b3e50c1c4'
tail=(D/'opening_delay_tail.py.txt').read_bytes();out=D/'opening_delays';out.mkdir(exist_ok=True)
configs=[(5,0)]+[(initial,due) for initial in (0,1,2,3,4) for due in (1,2,3)]
variants=[]
for initial,due in configs:
    name=f'buy{initial}_due{due}';path=out/(name+'.py')
    code=base+f'\n_OP_INITIAL={initial}\n_OP_DUE={due}\n'.encode()+tail
    compile(code,str(path),'exec');assert not path.exists();path.write_bytes(code)
    variants.append(dict(name=name,path=path.relative_to(R).as_posix(),initial=initial,due=due,sha256=hashlib.sha256(code).hexdigest()))
(D/'opening_delay_manifest.json').write_text(json.dumps(variants,indent=2))
design=json.loads((D/'broad_design.json').read_text())
roster=[o for o in design['roster'] if o['family'] in ('fieldcraft','aurax','marketshock','r2','demo_07','demo_22','demo_06','demo_04')]
seeds=design['seeds'][:2];jobs=[]
for candidate in [v['path'] for v in variants]+['submissions/release_v10_r2/main.py']:
    for opponent in roster:
        for seed in seeds:
            for seat in (0,1):
                j=dict(candidate=candidate,opponent=opponent['path'],seed=seed,seat=seat,family=opponent['family'],panel=opponent['panel'])
                for key in ('candidate','opponent'):j[key+'_sha256']=hashlib.sha256((R/j[key]).read_bytes()).hexdigest()
                j['id']=hashlib.sha256(json.dumps(j,sort_keys=True).encode()).hexdigest()[:24];jobs.append(j)
(D/'opening_delay_jobs.json').write_text(json.dumps(jobs,indent=2))
print(json.dumps(dict(variants=len(variants),games=len(jobs),worlds=len(seeds),scope='Development only.')),flush=True)

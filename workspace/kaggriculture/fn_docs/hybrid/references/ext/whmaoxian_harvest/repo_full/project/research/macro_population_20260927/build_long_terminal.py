"""Earlier final-day planning candidates; all previous release files are immutable."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1];out=D/'long_terminal';out.mkdir(exist_ok=True)
base_path='submissions/release_v10_r2/main.py';base=(R/base_path).read_bytes()
assert hashlib.sha256(base).hexdigest()=='b35b5b09fbec059ab7cbd2ba67a9fbb6d3e467ef5262f3e2ddba592b3e50c1c4'
configs=[('control',712,64,4),('start712',712,192,12),('start708',708,192,12),('start704',704,192,12),('start700',700,192,12)]
variants=[]
for name,start,budget,proposals in configs:
    constants=f'\n_LT_MODE={name!r}\n_LT_START={start}\n_LT_BUDGET={budget}\n_LT_PROPOSALS={proposals}\n'
    data=base+constants.encode()+(D/'long_terminal_tail.py.txt').read_bytes();path=out/(name+'.py');compile(data,str(path),'exec')
    if path.exists():assert path.read_bytes()==data
    else:path.write_bytes(data)
    variants.append(dict(path=path.relative_to(R).as_posix(),name=name,sha256=hashlib.sha256(data).hexdigest()))
design=json.loads((D/'route_design.json').read_text());jobs=[]
for variant in variants:
    for opponent in [r for r in design['roster'] if r['family'] in ('fieldcraft','top_style_03','r2')]:
        for seed in design['seeds'][:2]:
            for seat in (0,1):
                j=dict(candidate=variant['path'],opponent=opponent['path'],family=opponent['family'],panel=opponent['panel'],seed=seed,seat=seat)
                for key in ('candidate','opponent'):j[key+'_sha256']=hashlib.sha256((R/j[key]).read_bytes()).hexdigest()
                j['id']=hashlib.sha256(json.dumps(j,sort_keys=True).encode()).hexdigest()[:24];jobs.append(j)
(D/'long_terminal_manifest.json').write_text(json.dumps(variants,indent=2))
(D/'long_terminal_jobs.json').write_text(json.dumps(jobs,indent=2))
print(json.dumps(dict(variants=len(variants),smoke_games=len(jobs),scope='Functional development, not independent strength.')),flush=True)

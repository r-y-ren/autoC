"""Finite standalone daily-dispatch prototypes; immutable original R2 opening."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1]
base=(R/'submissions/release_v10_r2/main.py').read_bytes()
assert hashlib.sha256(base).hexdigest()=='b35b5b09fbec059ab7cbd2ba67a9fbb6d3e467ef5262f3e2ddba592b3e50c1c4'
manifest=[]
for start in (12,16):
    for workers in (11,12,13):
        name=f'day{start}_hands{workers}'
        constants=f'\n_DP_START={start}\n_DP_WORKERS={workers}\n_DP_DELIVERY=8\n_DP_PLANT_WEIGHT=.3\n_DP_FEED_WEIGHT=1\n_DP_DISTANCE_POWER=1.0\n'
        data=base+constants.encode()+(D/'dispatch.py.txt').read_bytes()
        path=D/(name+'.py');compile(data,str(path),'exec');assert not path.exists()
        path.write_bytes(data);manifest.append(dict(name=name,path=path.relative_to(R).as_posix(),sha256=hashlib.sha256(data).hexdigest()))
(D/'manifest.json').write_text(json.dumps(manifest,indent=2))
design=json.loads((R/'research/route_value_20260927/pilot_design.json').read_text())
roster=[r for r in design['roster'] if r['family'] in ('fieldcraft','r2','top_style_03')]
seeds=design['seeds'][:2];jobs=[]
for candidate in [v['path'] for v in manifest]+['submissions/release_v10_r2/main.py']:
    for opponent in roster:
        for seed in seeds:
            for seat in (0,1):
                j=dict(candidate=candidate,opponent=opponent['path'],seed=seed,seat=seat,family=opponent['family'],panel=opponent['panel'])
                for key in ('candidate','opponent'):j[key+'_sha256']=hashlib.sha256((R/j[key]).read_bytes()).hexdigest()
                j['id']=hashlib.sha256(json.dumps(j,sort_keys=True).encode()).hexdigest()[:24];jobs.append(j)
(D/'smoke_jobs.json').write_text(json.dumps(jobs,indent=2))
print(json.dumps(dict(variants=len(manifest),games=len(jobs),scope='Development prototypes, not release candidates.')),flush=True)

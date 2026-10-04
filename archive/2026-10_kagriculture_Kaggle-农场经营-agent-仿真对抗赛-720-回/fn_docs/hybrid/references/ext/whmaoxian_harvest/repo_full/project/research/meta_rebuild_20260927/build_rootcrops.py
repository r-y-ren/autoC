"""Independent production/cash ablations on an unchanged worker route."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1]
base=(R/'submissions/release_v10_r2/main.py').read_bytes()
assert hashlib.sha256(base).hexdigest()=='b35b5b09fbec059ab7cbd2ba67a9fbb6d3e467ef5262f3e2ddba592b3e50c1c4'
variants=[]
for name,crop,keep in [('temp_carrot','CARROT',False),('temp_wheat_keep','WHEAT',True)]:
    raw=base+f'\n_RC_CROP={crop!r}\n_RC_KEEP={keep}\n'.encode()+(D/'rootcrop_tail.txt').read_bytes()
    path=D/f'candidates/{name}.py';compile(raw,str(path),'exec')
    assert not path.exists();path.write_bytes(raw)
    variants.append(dict(name=name,path=path.relative_to(R).as_posix(),sha256=hashlib.sha256(raw).hexdigest(),crop=crop,keep=keep))
(D/'rootcrop_candidates.json').write_text(json.dumps(variants,indent=2))
design=json.loads((D/'pilot_design.json').read_text());jobs=[]
for v in variants:
    for opponent in design['roster']:
        for seed in design['seeds']:
            for seat in (0,1):
                j=dict(candidate=v['path'],opponent=opponent['path'],family=opponent['family'],panel=opponent['panel'],seed=seed,seat=seat,candidate_sha256=v['sha256'],opponent_sha256=hashlib.sha256((R/opponent['path']).read_bytes()).hexdigest())
                j['id']=hashlib.sha256(json.dumps(j,sort_keys=True).encode()).hexdigest()[:24];jobs.append(j)
(D/'rootcrop_jobs.json').write_text(json.dumps(jobs,indent=2))
print(json.dumps(dict(candidates=len(variants),new_games=len(jobs),controls='Use the already recorded pilot R2 controls.')),flush=True)

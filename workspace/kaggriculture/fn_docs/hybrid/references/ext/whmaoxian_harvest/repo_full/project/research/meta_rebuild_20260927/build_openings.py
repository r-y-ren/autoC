"""Bounded production variants; do not modify the frozen release."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1]
raw=(R/'submissions/release_v10_r2/main.py').read_bytes()
assert hashlib.sha256(raw).hexdigest()=='b35b5b09fbec059ab7cbd2ba67a9fbb6d3e467ef5262f3e2ddba592b3e50c1c4'
manifest=[]
for day in (2,3):
    data=raw+f'\n_PO_HARVEST_DAY={day}\n'.encode()+(D/'productive_opening.txt').read_bytes()
    target=D/f'candidates/productive_day{day}.py';compile(data,str(target),'exec')
    assert not target.exists();target.write_bytes(data)
    manifest.append(dict(path=target.relative_to(R).as_posix(),day=day,sha256=hashlib.sha256(data).hexdigest()))
(D/'opening_candidates.json').write_text(json.dumps(manifest,indent=2))
pilot=json.loads((D/'pilot_design.json').read_text());jobs=[]
for candidate in [r['path'] for r in manifest]:
    for opponent in pilot['roster']:
        for seed in pilot['seeds']:
            for seat in (0,1):
                j=dict(candidate=candidate,opponent=opponent['path'],family=opponent['family'],panel=opponent['panel'],seed=seed,seat=seat)
                for k in ('candidate','opponent'):j[k+'_sha256']=hashlib.sha256((R/j[k]).read_bytes()).hexdigest()
                j['id']=hashlib.sha256(json.dumps(j,sort_keys=True).encode()).hexdigest()[:24];jobs.append(j)
(D/'opening_pilot_jobs.json').write_text(json.dumps(jobs,indent=2))
print(json.dumps(dict(candidates=len(manifest),new_games=len(jobs),controls='Original pilot R2 rows; not new games.')),flush=True)

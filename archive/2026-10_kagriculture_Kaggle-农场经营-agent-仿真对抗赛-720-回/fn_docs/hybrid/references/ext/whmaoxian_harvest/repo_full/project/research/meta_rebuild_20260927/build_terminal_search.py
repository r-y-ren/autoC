"""Bounded terminal-search ablations, preserving original physical certificates."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1]
base=(R/'submissions/release_v10_r2/main.py').read_bytes()
assert hashlib.sha256(base).hexdigest()=='b35b5b09fbec059ab7cbd2ba67a9fbb6d3e467ef5262f3e2ddba592b3e50c1c4'
variants=[]
for limit,proposals in ((128,8),(256,16)):
    data=base+f'\n_TS_LIMIT={limit}\n_TS_PROPOSALS={proposals}\n'.encode()+(D/'terminal_search_tail.txt').read_bytes()
    path=D/f'candidates/terminal{limit}.py';compile(data,str(path),'exec')
    assert not path.exists();path.write_bytes(data)
    variants.append(dict(path=path.relative_to(R).as_posix(),sha256=hashlib.sha256(data).hexdigest(),simulations=limit,proposals=proposals))
(D/'terminal_candidates.json').write_text(json.dumps(variants,indent=2))
design=json.loads((D/'value_extended_design.json').read_text());jobs=[]
for v in variants:
    for opponent in design['roster']:
        for seed in design['seeds']:
            for seat in (0,1):
                j=dict(candidate=v['path'],opponent=opponent['path'],family=opponent['family'],panel=opponent['panel'],seed=seed,seat=seat,candidate_sha256=v['sha256'],opponent_sha256=hashlib.sha256((R/opponent['path']).read_bytes()).hexdigest())
                j['id']=hashlib.sha256(json.dumps(j,sort_keys=True).encode()).hexdigest()[:24];jobs.append(j)
(D/'terminal_jobs.json').write_text(json.dumps(jobs,indent=2))
(D/'terminal_design.json').write_text(json.dumps(dict(variants=variants,seeds=design['seeds'],roster=design['roster'],jobs=len(jobs),scope='Terminal physical-search development. Latency is recorded, not enforced by this fast runner. Official timeout validation required.'),indent=2))
print(json.dumps(dict(candidates=len(variants),new_games=len(jobs))),flush=True)

"""Finite paired Kaggriculture experiments on queued farming-task handling."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1];out=D/'weed_queue';out.mkdir(exist_ok=True)
base=(R/'submissions/release_v10_r2/main.py').read_bytes()
assert hashlib.sha256(base).hexdigest()=='b35b5b09fbec059ab7cbd2ba67a9fbb6d3e467ef5262f3e2ddba592b3e50c1c4'
variants=[]
for mode in ('control','dig_only','dedup','prune','chains','none'):
    raw=base+f'\n_WQ_MODE={mode!r}\n'.encode()+(D/'weed_queue_tail.py.txt').read_bytes()
    path=out/(mode+'.py');compile(raw,str(path),'exec')
    if path.exists():assert path.read_bytes()==raw
    else:path.write_bytes(raw)
    variants.append(dict(path=path.relative_to(R).as_posix(),mode=mode,sha256=hashlib.sha256(raw).hexdigest()))
seeds=[int.from_bytes(hashlib.sha256(f'weed-queue-20260927-iteration-1-{i}'.encode()).digest()[:4],'big')%2000000000 for i in range(8)]
known=set(sum(json.loads((D/'worlds.json').read_text()).values(),[]))|set(json.loads((D/'route_design.json').read_text())['seeds'])
assert len(set(seeds))==8 and not known.intersection(seeds)
roster=json.loads((D/'roster.json').read_text());jobs=[]
for candidate in [v['path'] for v in variants]+['submissions/release_v10_r2/main.py']:
    for opponent in roster:
        for seed in seeds:
            for seat in (0,1):
                j=dict(candidate=candidate,opponent=opponent['path'],family=opponent['family'],panel=opponent['panel'],seed=seed,seat=seat)
                for key in ('candidate','opponent'):j[key+'_sha256']=hashlib.sha256((R/j[key]).read_bytes()).hexdigest()
                j['id']=hashlib.sha256(json.dumps(j,sort_keys=True).encode()).hexdigest()[:24];jobs.append(j)

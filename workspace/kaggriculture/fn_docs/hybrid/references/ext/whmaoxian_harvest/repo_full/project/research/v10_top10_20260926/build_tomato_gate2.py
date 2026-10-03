"""Create finite cost-model ablations without altering any prior candidate."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1]
out=D/'tomato_gate2';out.mkdir(exist_ok=True)
base=(R/'submissions/release_v10_r2/main.py').read_bytes()
assert hashlib.sha256(base).hexdigest()=='b35b5b09fbec059ab7cbd2ba67a9fbb6d3e467ef5262f3e2ddba592b3e50c1c4'
tail=(D/'tomato_gate2_tail.txt').read_text(encoding='utf-8')
configs=[('r0_g500',0,500),('r80_g500',80,500),('r152_g500',152,500),('r0_g2000',0,2000),('r80_g2000',80,2000),('r152_g2000',152,2000)]
manifest=[]
for name,rival,gain in configs:
    parameters=f'\n_TG_RIVAL={rival}\n_TG_MIN_GAIN={gain}\n_TG_MIN_NET=2000\n_TG_EXPECTATION=0\n'
    raw=base+parameters.encode()+tail.encode('utf-8')
    path=out/(name+'.py');compile(raw,str(path),'exec')
    if path.exists():assert path.read_bytes()==raw
    else:path.write_bytes(raw)
    manifest.append(dict(path=path.relative_to(R).as_posix(),sha256=hashlib.sha256(raw).hexdigest(),rival_supply_assumption=rival,marginal_profit_floor=gain))
(D/'tomato_gate2_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print(json.dumps({'variants':len(manifest),'frozen_releases_changed':False}),flush=True)

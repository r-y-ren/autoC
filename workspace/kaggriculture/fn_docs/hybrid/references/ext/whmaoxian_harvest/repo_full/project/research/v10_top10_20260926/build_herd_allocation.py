"""Declared development ablations of existing livestock route alternatives."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1];out=D/'herd_allocation';out.mkdir(exist_ok=True)
base=(R/'submissions/release_v10_r2/main.py').read_bytes();tail=(D/'herd_allocation_tail.txt').read_bytes()
assert hashlib.sha256(base).hexdigest()=='b35b5b09fbec059ab7cbd2ba67a9fbb6d3e467ef5262f3e2ddba592b3e50c1c4'
configs=[('both_current',('GOOSE','SHEEP'),None,1.15,600,0),('both_expected',('GOOSE','SHEEP'),None,1.15,600,.5),('both_strict',('GOOSE','SHEEP'),None,1.3,1500,0),('goose_value',('GOOSE',),None,1.15,600,0),('sheep_value',('SHEEP',),None,1.15,600,0),('both_nomilk',('GOOSE','SHEEP'),'nomilk',1.3,600,0)]
manifest=[]
for name,opts,rule,ratio,gain,future in configs:
    parameters=f'\n_CS_OPTIONS={opts!r}\n_CS_SHOP_RULE={rule!r}\n_CS_RATIO={ratio}\n_CS_MIN_GAIN={gain}\n_HD2_FUTURE={future}\n'
    raw=base+parameters.encode()+tail;path=out/(name+'.py');compile(raw,str(path),'exec')
    if path.exists():assert path.read_bytes()==raw
    else:path.write_bytes(raw)
    manifest.append(dict(path=path.relative_to(R).as_posix(),sha256=hashlib.sha256(raw).hexdigest(),options=opts,rule=rule,ratio=ratio,gain=gain,future_expectation=future))
(D/'herd_allocation_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print(json.dumps(dict(variants=len(manifest))),flush=True)

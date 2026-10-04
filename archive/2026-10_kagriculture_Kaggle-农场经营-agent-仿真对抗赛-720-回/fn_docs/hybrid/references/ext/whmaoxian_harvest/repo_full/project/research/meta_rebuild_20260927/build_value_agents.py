"""Create isolated value candidates; frozen R2 bytes remain unchanged."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1];O=D/'candidates';O.mkdir(exist_ok=True)
base=(R/'submissions/release_v10_r2/main.py').read_bytes()
assert hashlib.sha256(base).hexdigest()=='b35b5b09fbec059ab7cbd2ba67a9fbb6d3e467ef5262f3e2ddba592b3e50c1c4'
features=R/'research/v10_top10_20260926/market_bc_features.py'
model=json.loads((D/'value_model.json').read_text())
assert hashlib.sha256(features.read_bytes()).hexdigest()==model['feature_sha256']
common=base+b'\n'+features.read_bytes()+b'\n'+(R/'research/value_policy_20260927/policy.py').read_bytes()
common+=('\n_VP_FOREST='+repr(model['forest'])+'\n').encode()
settings=[('shadow',5,.55,12,True),('value5',5,.55,12,False),('value15',15,.6,12,False),('value30',30,.7,24,False)]
manifest=[]
for name,gain,prob,cooldown,shadow in settings:
    constants=f'\n_VP_MIN_GAIN={gain}\n_VP_PROB={prob}\n_VP_COOLDOWN={cooldown}\n_VP_SHADOW={shadow}\n'
    raw=common+constants.encode()+(D/'value_tail.txt').read_bytes()
    path=O/(name+'.py');compile(raw,str(path),'exec')
    assert not path.exists();path.write_bytes(raw)
    manifest.append(dict(name=name,path=path.relative_to(R).as_posix(),sha256=hashlib.sha256(raw).hexdigest(),settings=dict(gain=gain,prob=prob,cooldown=cooldown,shadow=shadow)))
(D/'value_candidates.json').write_text(json.dumps(manifest,indent=2))
print(json.dumps(dict(candidates=len(manifest),base_unchanged=True)),flush=True)

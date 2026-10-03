"""Study independently viable 19-plot investments; preserve frozen releases."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1];out=D/'production_scale';out.mkdir(exist_ok=True)
raw=(R/'submissions/release_v10_r2/main.py').read_bytes()
assert hashlib.sha256(raw).hexdigest()=='b35b5b09fbec059ab7cbd2ba67a9fbb6d3e467ef5262f3e2ddba592b3e50c1c4'
tail=(D/'production_scale_tail.py.txt').read_text(encoding='utf-8')
configs=[('control',2,1000000000,152),('full152_net2k',2,2000,152),('full152_net5k',2,5000,152),('full240_net2k',2,2000,240),('full240_net5k',2,5000,240)]
manifest=[]
for name,shops,net,rival in configs:
    constants=f'\n_PS_MIN_SHOPS={shops}\n_PS_MIN_NET={net}\n_PS_RIVAL_UNITS={rival}\n'
    source=raw+constants.encode('utf-8')+tail.encode('utf-8');path=out/(name+'.py');compile(source,str(path),'exec')
    if path.exists():assert path.read_bytes()==source
    else:path.write_bytes(source)
    manifest.append(dict(path=path.relative_to(R).as_posix(),sha256=hashlib.sha256(source).hexdigest(),minimum_known_demand=shops,full_profit_floor=net,rival_tomato_supply_scenario=rival,scope='Absolute 152-unit revenue less all land, seed, labor and fertilizer cost; existing eligible branch unchanged. Rival scenario is an assumption, not a proven supply bound.'))
(D/'production_scale_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print(json.dumps(dict(candidates=len(manifest),new_release=False)),flush=True)

"""Bounded round-trip chores during confirmed idle intervals; development only."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1];out=D/'slack_roundtrip';out.mkdir(exist_ok=True)
base=(R/'submissions/release_v10_r2/main.py').read_bytes()
assert hashlib.sha256(base).hexdigest()=='b35b5b09fbec059ab7cbd2ba67a9fbb6d3e467ef5262f3e2ddba592b3e50c1c4'
tail=(D/'slack_roundtrip_tail.txt').read_text(encoding='utf-8')
tail=tail.replace("native=_IMPL.chassis.players.get(seat);selected=set()","native=_IMPL.chassis.players.get(seat);selected={tuple(t['site']) for t in active.values()}")
configs=[('farmer_care1',1,True,False),('all_care1',1,False,False),('farmer_care2',2,True,False),('all_care2',2,False,False),('farmer_collect2',2,True,True),('all_collect2',2,False,True)]
manifest=[]
for name,distance,farmer,collect in configs:
    params=f'\n_SD_DISTANCE={distance}\n_SD_FARMER_ONLY={farmer!r}\n_SD_COLLECT={collect!r}\n_SD_HARVEST=False\n_SD_FROM=6\n'
    raw=base+params.encode()+tail.encode('utf-8');path=out/(name+'.py');compile(raw,str(path),'exec')
    if path.exists():assert path.read_bytes()==raw
    else:path.write_bytes(raw)
    manifest.append(dict(path=path.relative_to(R).as_posix(),sha256=hashlib.sha256(raw).hexdigest(),max_distance=distance,farmer_only=farmer,collect=collect))
(D/'slack_roundtrip_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
prepare=(D/'prepare_market_value.py').read_text(encoding='utf-8').replace('market_value','slack_roundtrip')
(D/'prepare_slack_roundtrip.py').write_text(prepare,encoding='utf-8')
print(json.dumps(dict(variants=len(manifest))),flush=True)

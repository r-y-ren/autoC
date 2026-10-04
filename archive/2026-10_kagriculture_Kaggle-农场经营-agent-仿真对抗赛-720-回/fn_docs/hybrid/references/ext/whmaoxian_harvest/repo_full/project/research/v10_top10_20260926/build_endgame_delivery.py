"""Create physical-only endgame candidates with unchanged market orders."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1];out=D/'endgame_delivery';out.mkdir(exist_ok=True)
raw=(R/'submissions/release_v10_r2/main.py').read_bytes()
assert hashlib.sha256(raw).hexdigest()=='b35b5b09fbec059ab7cbd2ba67a9fbb6d3e467ef5262f3e2ddba592b3e50c1c4'
template=(D/'endgame_delivery_tail.py.txt').read_text(encoding='utf-8')
# Finish optional deposits at 717, leaving final liquidation at 718 to R2.
template=template.replace('719-step','718-step').replace('step>718','step>717')
configs=[('observe',90,0,False),('harvest90',90,2,False),('harvest100',100,3,False),('collect90',90,2,True),('collect100',100,3,True),('late_maintenance',90,2,True)]
manifest=[]
for name,capacity,workers,fertilizer in configs:
    tail=template
    if name=='late_maintenance':
        old="if c[0] not in ('PASS','DROP',*_ED_MOVES):busy.add(i)"
        new="if c[0] not in ('PASS','DROP','CARE','FEED',*_ED_MOVES):busy.add(i)"
        assert tail.count(old)==1;tail=tail.replace(old,new)
    constants=f'\n_ED_START=712\n_ED_CAPACITY={capacity}\n_ED_MAX_WORKERS={workers}\n_ED_FERTILIZER={fertilizer!r}\n_ED_MIN_VALUE=10.0\n'
    source=raw+constants.encode('utf-8')+tail.encode('utf-8');path=out/(name+'.py');compile(source,str(path),'exec')
    if path.exists():assert path.read_bytes()==source
    else:path.write_bytes(source)
    manifest.append(dict(path=path.relative_to(R).as_posix(),sha256=hashlib.sha256(source).hexdigest(),capacity=capacity,workers=workers,fertilizer=fertilizer,ignore_unproductive_last_day_maintenance=name=='late_maintenance',market_orders_modified=False,latest_optional_drop=717))
(D/'endgame_delivery_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print(json.dumps(dict(candidates=len(manifest),new_release=False,market_order_changes=False)),flush=True)

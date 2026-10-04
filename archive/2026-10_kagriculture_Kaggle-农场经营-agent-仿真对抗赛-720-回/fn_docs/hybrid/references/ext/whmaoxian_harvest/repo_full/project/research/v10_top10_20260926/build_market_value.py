"""Frozen parameter grid for a new marginal win-value market controller."""
from pathlib import Path
import hashlib,itertools,json
D=Path(__file__).resolve().parent;R=D.parents[1];out=D/'market_value';out.mkdir(exist_ok=True)
base=(R/'submissions/release_v10_r2/main.py').read_bytes()
assert hashlib.sha256(base).hexdigest()=='b35b5b09fbec059ab7cbd2ba67a9fbb6d3e467ef5262f3e2ddba592b3e50c1c4'
tail=(D/'market_value_tail.txt').read_bytes();manifest=[]
configs=[dict(horizon=h,rival_weight=w,stock_weight=s,hold=hold,min_gain=5) for h,w,s,hold in itertools.product((4,12),(.5,1.0),(.4,1.0),(False,True))]
configs.append(dict(horizon=4,rival_weight=1.,stock_weight=.4,hold=False,min_gain=1e12))
for index,c in enumerate(configs):
    name=f"v{index:02d}";params={'HORIZON':c['horizon'],'RIVAL_WEIGHT':c['rival_weight'],'STOCK_WEIGHT':c['stock_weight'],'MATURE_WEIGHT':c['horizon']/24,'HOLD':c['hold'],'ZERO_PROB':.25,'LOT':20,'MIN_GAIN':c['min_gain']}
    raw=base+('\n'+''.join('_MV_'+k+'='+repr(v)+'\n' for k,v in params.items())).encode()+tail
    path=out/(name+'.py');compile(raw,str(path),'exec')
    if path.exists():assert path.read_bytes()==raw
    else:path.write_bytes(raw)
    manifest.append(dict(path=path.relative_to(R).as_posix(),sha256=hashlib.sha256(raw).hexdigest(),parameters=c))
(D/'market_value_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print(json.dumps(dict(candidates=len(manifest),no_op_control=manifest[-1]['path'])),flush=True)

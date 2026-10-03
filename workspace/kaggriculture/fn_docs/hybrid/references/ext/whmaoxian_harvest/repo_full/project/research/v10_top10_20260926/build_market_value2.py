"""Repair the market objective by valuing remaining own inventory consistently."""
from pathlib import Path
import ast,hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1];out=D/'market_value2';out.mkdir(exist_ok=True)
base=(R/'submissions/release_v10_r2/main.py').read_bytes()
assert hashlib.sha256(base).hexdigest()=='b35b5b09fbec059ab7cbd2ba67a9fbb6d3e467ef5262f3e2ddba592b3e50c1c4'
tail=(D/'market_value_tail.txt').read_text(encoding='utf-8');lines=tail.splitlines(True)
node=next(n for n in ast.parse(tail).body if isinstance(n,ast.FunctionDef) and n.name=='_mv_quantity')
tail=''.join(lines[:node.lineno-1])+(D/'market_value2_quantity.txt').read_text(encoding='utf-8')+''.join(lines[node.end_lineno:])
manifest=[]
for horizon in (4,12):
    for beta in (.5,1.):
        for hold in (False,True):
            index=len(manifest);name=f'v{index:02d}'
            params={'HORIZON':horizon,'RIVAL_WEIGHT':beta,'STOCK_WEIGHT':.4,'MATURE_WEIGHT':horizon/24,'HOLD':hold,'ZERO_PROB':.25,'LOT':20,'MIN_GAIN':5}
            raw=base+('\n'+''.join('_MV_'+k+'='+repr(v)+'\n' for k,v in params.items())).encode()+tail.encode('utf-8')
            path=out/(name+'.py');compile(raw,str(path),'exec')
            if path.exists():assert path.read_bytes()==raw
            else:path.write_bytes(raw)
            manifest.append(dict(path=path.relative_to(R).as_posix(),sha256=hashlib.sha256(raw).hexdigest(),parameters=params))
(D/'market_value2_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
prepare=(D/'prepare_market_value.py').read_text(encoding='utf-8').replace('market_value','market_value2')
(D/'prepare_market_value2.py').write_text(prepare,encoding='utf-8')
print(json.dumps(dict(variants=len(manifest),previous_evidence_unchanged=True)),flush=True)

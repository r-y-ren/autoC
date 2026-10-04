"""Create research-only slot predictors from the frozen public-feature forest."""
from pathlib import Path
import base64,hashlib,json,zlib
D=Path(__file__).resolve().parent;R=D.parents[1];out=D/'slot_candidates';out.mkdir(exist_ok=True)
base=(R/'submissions/release_v10_r2/main.py').read_bytes()
assert hashlib.sha256(base).hexdigest()=='b35b5b09fbec059ab7cbd2ba67a9fbb6d3e467ef5262f3e2ddba592b3e50c1c4'
model_bytes=(D/'slot_model.json').read_bytes()
assert hashlib.sha256(model_bytes).hexdigest()=='5195d9032e634d9bb85a598047d4faff45efff2f2e166cc64195d435ee8c58b1'
model=json.loads(model_bytes);features=(D/'flow_features.py').read_bytes()
assert model['feature_source_sha256']==hashlib.sha256(features).hexdigest()
forest=json.dumps(model['forest'],separators=(',',':')).encode()
blob=base64.b85encode(zlib.compress(forest,9)).decode()
tail=(D/'slot_policy_tail.py.txt').read_text(encoding='utf-8')
configs=[('observe',1,1,99999),('s1_margin',1,1,216),('s2_margin',2,1,216),('s2_balanced',2,.5,216),('s2_revenue',2,0,216)]
manifest=[]
for name,scale,weight,start in configs:
    source=base.decode('utf-8')+'\n'+features.decode('utf-8')
    source+='\nimport base64,json,zlib\n_SP_FOREST=json.loads(zlib.decompress(base64.b85decode('+repr(blob)+')))\n'
    source+=f'_SP_SCALE={scale!r}\n_SP_RIVAL_WEIGHT={weight!r}\n_SP_START={start}\n_SP_MIN_GAIN=2.0\n'+tail
    target=out/(name+'.py');compile(source,str(target),'exec')
    if target.exists():assert target.read_bytes()==source.encode('utf-8')
    else:target.write_bytes(source.encode('utf-8'))
    manifest.append(dict(name=name,path=target.relative_to(R).as_posix(),sha256=hashlib.sha256(target.read_bytes()).hexdigest(),scale=scale,rival_weight=weight,start=start))
(D/'slot_candidates_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print(json.dumps(dict(candidates=len(manifest),model_bytes=len(forest),source_bytes=len(source.encode('utf-8')),release_created=False)),flush=True)

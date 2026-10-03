"""Build isolated bounded commodity-cycle candidates from a frozen numerical model."""
from pathlib import Path
import base64,hashlib,json,zlib
D=Path(__file__).resolve().parent;R=D.parents[1];out=D/'cycle_agents';out.mkdir(exist_ok=True)
base=(R/'submissions/release_v10_r2/main.py').read_bytes()
assert hashlib.sha256(base).hexdigest()=='b35b5b09fbec059ab7cbd2ba67a9fbb6d3e467ef5262f3e2ddba592b3e50c1c4'
modelraw=(D/'cycle_model.json').read_bytes();model=json.loads(modelraw)
report=json.loads((D/'cycle_model_report.json').read_text())
assert hashlib.sha256(modelraw).hexdigest()==report['model_sha256']
features=(D/'cycle_features.py').read_bytes();assert hashlib.sha256(features).hexdigest()==model['feature_sha256']
blob=base64.b85encode(zlib.compress(json.dumps(model['forest'],separators=(',',':')).encode(),9)).decode()
data=base+b'\n'+features+('\n_CY_FOREST=json.loads(zlib.decompress(base64.b85decode('+repr(blob)+')))\n').encode()+(D/'cycle_policy_tail.py.txt').read_bytes()
configs=[dict(name='shadow',threshold=.5,maximum=8,side='both',shadow=True)]
for threshold in (.25,.5,.7):
    for maximum in (8,24):configs.append(dict(name=f'p{int(threshold*100)}_q{maximum}',threshold=threshold,maximum=maximum,side='both',shadow=False))
configs.append(dict(name='sell_p15_q24',threshold=.15,maximum=24,side='sell',shadow=False))
configs.append(dict(name='buy_p15_q24',threshold=.15,maximum=24,side='buy',shadow=False))
manifest=[]
for cfg in configs:
    tail=f"\n_CY_THRESHOLD={cfg['threshold']}\n_CY_MAX={cfg['maximum']}\n_CY_SIDE={cfg['side']!r}\n_CY_SHADOW={cfg['shadow']!r}\n_CY_START=72\n_CY_END=648\n_CY_MIN_CASH=3000\n_CY_ALLOWED_ITEMS=('WHEAT','FERTILIZER')\n"
    raw=data+tail.encode();path=out/(cfg['name']+'.py');compile(raw,str(path),'exec')
    if path.exists():assert path.read_bytes()==raw
    else:path.write_bytes(raw)
    manifest.append(dict(path=path.relative_to(R).as_posix(),settings=cfg,sha256=hashlib.sha256(raw).hexdigest()))
(D/'cycle_agents_manifest.json').write_text(json.dumps(manifest,indent=2))
print(json.dumps(dict(variants=len(manifest),model_sha256=report['model_sha256'],published=False)),flush=True)

"""Build a finite working-capital ablation; preserve all releases."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1];out=D/'early_liquidity';out.mkdir(exist_ok=True)
base=(R/'submissions/release_v10_r2/main.py').read_bytes()
assert hashlib.sha256(base).hexdigest()=='b35b5b09fbec059ab7cbd2ba67a9fbb6d3e467ef5262f3e2ddba592b3e50c1c4'
configs=[]
for horizon in (4,12,24):
    configs.append(dict(name=f'grain_h{horizon}',items=['WHEAT'],horizon=horizon,maximum=3,buffer=0,cash=2000,end=288))
for horizon in (4,12):
    configs.append(dict(name=f'grain_buffer2_h{horizon}',items=['WHEAT'],horizon=horizon,maximum=8,buffer=2,cash=2000,end=288))
for horizon in (12,24):
    configs.append(dict(name=f'fert_h{horizon}',items=['FERTILIZER'],horizon=horizon,maximum=4,buffer=0,cash=2000,end=288))
    configs.append(dict(name=f'mixed_h{horizon}',items=['FERTILIZER','WOOL','MILK','STRAWBERRY','CARROT','WHEAT'],horizon=horizon,maximum=4,buffer=2,cash=2000,end=288))
configs.append(dict(name='premium',items=['WOOL','MILK','STRAWBERRY','CARROT','MELON','TOMATO','EGG'],horizon=12,maximum=8,buffer=0,cash=8000,end=288))
configs.append(dict(name='grain_opening',items=['WHEAT'],horizon=4,maximum=3,buffer=0,cash=500,end=144))
manifest=[]
for cfg in configs:
    settings=f"\n_EL_START=24\n_EL_END={cfg['end']}\n_EL_CASH={cfg['cash']}\n_EL_HORIZON={cfg['horizon']}\n_EL_MAX={cfg['maximum']}\n_EL_BUFFER={cfg['buffer']}\n_EL_ITEMS={tuple(cfg['items'])!r}\n"
    raw=base+settings.encode()+(D/'early_liquidity_tail.py.txt').read_bytes()
    path=out/(cfg['name']+'.py');compile(raw,str(path),'exec')
    if path.exists():assert path.read_bytes()==raw
    else:path.write_bytes(raw)
    manifest.append(dict(path=path.relative_to(R).as_posix(),settings=cfg,sha256=hashlib.sha256(raw).hexdigest()))
(D/'early_liquidity_manifest.json').write_text(json.dumps(manifest,indent=2))
print(json.dumps(dict(variants=len(manifest),release_created=False)),flush=True)

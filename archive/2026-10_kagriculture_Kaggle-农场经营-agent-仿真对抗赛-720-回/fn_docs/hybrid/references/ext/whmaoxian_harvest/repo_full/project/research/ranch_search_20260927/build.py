"""Create isolated Kaggriculture virtual-farm candidates; never upload submissions."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1]
base=R/'submissions/release_v10_r2/main.py';raw=base.read_bytes()
assert hashlib.sha256(raw).hexdigest()=='b35b5b09fbec059ab7cbd2ba67a9fbb6d3e467ef5262f3e2ddba592b3e50c1c4'
tail=(D/'ranch_policy.py.txt').read_bytes();out=D/'candidates';out.mkdir(exist_ok=True)
configs=[dict(name='disabled',start=30,count=3,minimum=3000,buffer=20,animals=('COW','SHEEP','GOOSE'))]
for count in (2,3,4):
    for minimum in (0,3000):
        configs.append(dict(name=f'adapt_n{count}_net{minimum}',start=12,count=count,minimum=minimum,buffer=20,animals=('COW','SHEEP','GOOSE')))
for animal in ('COW','SHEEP','GOOSE'):
    configs.append(dict(name=animal.lower()+'_n3',start=12,count=3,minimum=0,buffer=0,animals=(animal,)))
configs.append(dict(name='mechanism_only',start=12,count=3,minimum=-1000000,buffer=0,animals=('SHEEP',)))
manifest=[]
for cfg in configs:
    settings=f"\n_RN_START={cfg['start']}\n_RN_STOP=17\n_RN_COUNT={cfg['count']}\n_RN_MIN_NET={cfg['minimum']}\n_RN_STOCK_BUFFER={cfg['buffer']}\n_RN_ANIMALS={cfg['animals']!r}\n"
    data=raw+settings.encode()+tail;path=out/(cfg['name']+'.py');compile(data,str(path),'exec')
    if path.exists():assert path.read_bytes()==data
    else:path.write_bytes(data)
    manifest.append(dict(cfg,path=path.relative_to(R).as_posix(),sha256=hashlib.sha256(data).hexdigest()))
(D/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print(json.dumps(dict(candidates=len(manifest),baseline_preserved=True)),flush=True)

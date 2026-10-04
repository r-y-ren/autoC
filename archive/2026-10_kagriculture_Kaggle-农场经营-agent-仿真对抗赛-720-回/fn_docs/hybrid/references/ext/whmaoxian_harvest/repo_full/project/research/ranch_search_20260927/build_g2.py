"""Refine simulated-farm expansion; preserve every previous tested source."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1]
raw=(R/'submissions/release_v10_r2/main.py').read_bytes()
assert hashlib.sha256(raw).hexdigest()=='b35b5b09fbec059ab7cbd2ba67a9fbb6d3e467ef5262f3e2ddba592b3e50c1c4'
tail=(D/'ranch_policy.py.txt').read_text();a=tail.index("    selling=sum(int(o[2])")
b=tail.index("    for item,credit in list(state['credit'].items()):",a)
tail=tail[:a]+(D/'feed_reserve.py.txt').read_text()+tail[b:]
tail=tail.replace('inventory-=demand;inventory+=supplies[d]',"inventory-=demand+_RN_FUTURE*_hd2_future_demand_per_day(item)*min(8-len(obs['town']['unlocked_shops']),max(0,d//3-day//3));inventory+=supplies[d]")
tail=tail.replace("state['last_forecast']=choice", "state['last_forecast']=choice;_RN_REPORT['last_forecast']=choice")
tail=tail.replace("forecasts=[_rn_forecast", "state['requested']=True\n        forecasts=[_rn_forecast")
tail=tail.replace("state.update(active=True,animal=choice['animal']", "state.update(requested=False,active=True,animal=choice['animal']")
configs=[]
for future in (0,1):
    for minimum in (0,3000):
        configs.append(dict(name=f'adapt_f{future}_net{minimum}',future=future,minimum=minimum,animals=('COW','SHEEP','GOOSE')))
for animal in ('SHEEP','COW','GOOSE'):
    configs.append(dict(name='probe_'+animal.lower(),future=0,minimum=-1000000,animals=(animal,)))
out=D/'generation2';out.mkdir(exist_ok=True);manifest=[]
for cfg in configs:
    settings=f"\n_RN_START=12\n_RN_STOP=17\n_RN_COUNT=3\n_RN_MIN_NET={cfg['minimum']}\n_RN_STOCK_BUFFER=0\n_RN_ANIMALS={cfg['animals']!r}\n_RN_FUTURE={cfg['future']}\n"
    data=raw+settings.encode()+tail.encode();path=out/(cfg['name']+'.py');compile(data,str(path),'exec')
    if path.exists():assert path.read_bytes()==data
    else:path.write_bytes(data)
    manifest.append(dict(cfg,path=path.relative_to(R).as_posix(),sha256=hashlib.sha256(data).hexdigest()))
(D/'generation2_manifest.json').write_text(json.dumps(manifest,indent=2));print(json.dumps(dict(variants=len(manifest))),flush=True)

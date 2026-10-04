"""Four distinct bounded-inventory policy integrations; baseline bytes preserved."""
from pathlib import Path
import hashlib,json
B=Path(__file__).resolve().parent
source=(B/'shadow.py').read_bytes();tail=(B/'full_advice_tail.txt').read_bytes()
settings=[('conditional35',dict(mode='active',threshold=.35,max_extra=16,conditional=True,hold=False)),
          ('conditional55',dict(mode='active',threshold=.55,max_extra=16,conditional=True,hold=False)),
          ('balanced35',dict(mode='active',threshold=.35,max_extra=16,conditional=True,hold=True,max_hold=8,hold_threshold=.15)),
          ('imitate25',dict(mode='active',threshold=.25,max_extra=16,conditional=False,hold=True,max_hold=8,hold_threshold=.10))]
manifest=[]
for name,cfg in settings:
    data=source+tail+('\n_MBC_CFG.update('+repr(cfg)+')\n').encode()
    path=B/(name+'.py');compile(data,str(path),'exec')
    if path.exists():assert path.read_bytes()==data
    else:path.write_bytes(data)
    manifest.append(dict(name=name,path=path.relative_to(B.parents[2]).as_posix(),sha256=hashlib.sha256(data).hexdigest(),settings=cfg))
(B/'second_generation.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print(json.dumps(dict(variants=len(manifest),new_model_training=False,released=False)),flush=True)

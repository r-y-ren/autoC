"""Kaggriculture virtual-farm action ablations. No online submission or real trading."""
from pathlib import Path
import hashlib,json
N=Path(__file__).resolve().parent;R=N.parents[1];DEST=N/'micro_candidates';DEST.mkdir(exist_ok=True)
base=(R/'submissions/release_v10_r2/main.py').read_bytes()
assert hashlib.sha256(base).hexdigest()=='b35b5b09fbec059ab7cbd2ba67a9fbb6d3e467ef5262f3e2ddba592b3e50c1c4'
variants=[('care',('care',),0),('water',('water',),0),('harvest',('harvest',),144),
    ('fertilizer',('fertilizer',),144),('maintenance',('care','water'),0),
    ('all_care_first',('care','water','harvest','fertilizer'),144),
    ('all_harvest_first',('harvest','care','water','fertilizer'),144),
    ('late_maintenance',('care','water','harvest'),480)]
manifest=[]
for name,actions,start in variants:
    source=base+f'\n_U_ACTIONS={actions!r}\n_U_START={start}\n'.encode()+(N/'micro_opportunities_tail.txt').read_bytes()
    path=DEST/(name+'.py');path.write_bytes(source);compile(path.read_bytes(),str(path),'exec')
    manifest.append(dict(name=name,path=path.relative_to(R).as_posix(),sha256=hashlib.sha256(source).hexdigest()))
(N/'micro_candidates_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print(json.dumps(dict(candidates=len(manifest))),flush=True)

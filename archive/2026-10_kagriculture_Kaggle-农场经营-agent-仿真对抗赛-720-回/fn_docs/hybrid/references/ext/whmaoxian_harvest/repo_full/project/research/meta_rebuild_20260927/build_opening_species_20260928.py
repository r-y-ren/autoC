"""Construct two bold opening hypotheses for smoke tests, not release."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1];sha=lambda b:hashlib.sha256(b).hexdigest()
raw=(R/'submissions/release_v10_r2/main.py').read_bytes()
assert sha(raw)=='b35b5b09fbec059ab7cbd2ba67a9fbb6d3e467ef5262f3e2ddba592b3e50c1c4'
assert b'_OS29_' not in raw
variants=[]
for mode in ('GOOSE','SHEEP'):
    data=raw+('\n_OS29_MODE='+repr(mode)+'\n').encode()+(D/'opening_species_20260928.txt').read_bytes()
    path=D/'candidates'/('opening_species_'+mode.lower()+'.py');compile(data,str(path),'exec')
    if path.exists():assert path.read_bytes()==data
    else:path.write_bytes(data)
    variants.append(dict(name=mode,path=path.relative_to(R).as_posix(),sha256=sha(data)))
p=D/'opening_species_design.json';text=json.dumps(dict(variants=variants,scope='Untested opening hypotheses. Sheep financing reduces initial wheat; feeding and escape must be checked, never presumed safe.'),indent=2)
if p.exists():assert p.read_text()==text
else:p.write_text(text)
print(json.dumps({'candidates':variants}),flush=True)

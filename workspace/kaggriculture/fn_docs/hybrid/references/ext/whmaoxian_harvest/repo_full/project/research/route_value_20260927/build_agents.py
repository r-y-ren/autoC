"""Create isolated standalone research agents; never overwrite a release."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1]
base=(R/'submissions/release_v10_r2/main.py').read_bytes()
assert hashlib.sha256(base).hexdigest()=='b35b5b09fbec059ab7cbd2ba67a9fbb6d3e467ef5262f3e2ddba592b3e50c1c4'
model=json.loads((D/'model.json').read_text());source=(D/'features.py').read_text()
assert hashlib.sha256(source.encode()).hexdigest()==model['feature_sha256']
manifest=[]
for name,threshold,shadow in [('learned',model['threshold'],False),('conservative',.10,False),('shadow',model['threshold'],True)]:
    tail='\n_RV_FEATURE_NS={}\nexec('+repr(source)+',_RV_FEATURE_NS)\n'
    tail+='_RV_MODEL='+repr(model)+'\n_RV_THRESHOLD='+repr(threshold)+'\n_RV_SHADOW='+repr(shadow)+'\n'
    data=base+tail.encode()+(D/'policy_tail.py.txt').read_bytes()
    target=D/(name+'.py');compile(data,str(target),'exec');assert not target.exists()
    target.write_bytes(data);manifest.append(dict(name=name,path=target.relative_to(R).as_posix(),
        sha256=hashlib.sha256(data).hexdigest(),threshold=threshold,shadow=shadow))
(D/'agents.json').write_text(json.dumps(manifest,indent=2))
print(json.dumps(dict(agents=manifest,released=False)),flush=True)

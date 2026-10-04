"""Cost-gated expansion and independent full-cost entry; development only."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1];out=D/'tomato_gate3';out.mkdir(exist_ok=True)
base=(R/'submissions/release_v10_r2/main.py').read_bytes()
assert hashlib.sha256(base).hexdigest()=='b35b5b09fbec059ab7cbd2ba67a9fbb6d3e467ef5262f3e2ddba592b3e50c1c4'
tail=(D/'tomato_gate2_tail.txt').read_text(encoding='utf-8')+(D/'tomato_gate3_tail.txt').read_text(encoding='utf-8')
protection='''
_T3_REQUEST=_v219_request
def _v219_request(obs,action,state,native):
    if _T3_FORCED.get(int(obs['player'])) and not state.get('committed') and int(obs['step'])%24>1:
        state['eligible']=False;state['t19_enabled']=False
        return action
    return _T3_REQUEST(obs,action,state,native)
def tomato_gate3_final(observation,configuration=None):
    return tomato_gate3_agent(observation,configuration)
tomato_gate3_final.telemetry=_TG_REPORT
agent=tomato_gate3_final
kaggle_submission_agent=tomato_gate3_final
'''
manifest=[]
for rival,net in ((0,0),(0,1000),(80,0),(80,1000)):
    raw=base+f'\n_TG_RIVAL={rival}\n_TG_MIN_GAIN=500\n_TG_MIN_NET={net}\n_TG_EXPECTATION=0\n'.encode()+(tail+protection).encode('utf-8')
    path=out/f'r{rival}_net{net}.py';compile(raw,str(path),'exec');assert not path.exists();path.write_bytes(raw)
    manifest.append(dict(path=path.relative_to(R).as_posix(),sha256=hashlib.sha256(raw).hexdigest(),rival_assumption=rival,profit_floor=net))
(D/'tomato_gate3_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print(json.dumps(dict(variants=len(manifest))),flush=True)

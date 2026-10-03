"""Earlier species decisions with order-sequence-aware sale funding."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1]
raw=(R/'submissions/release_v10_r2/main.py').read_bytes();sha=lambda b:hashlib.sha256(b).hexdigest()
assert sha(raw)=='b35b5b09fbec059ab7cbd2ba67a9fbb6d3e467ef5262f3e2ddba592b3e50c1c4'
def save(path,data):
    if path.exists():assert path.read_bytes()==data
    else:path.write_bytes(data)
variants=[]
configs=[('funded2_r5',2,5,True,1.1,600),('funded2_r25',2,25,True,1.1,600),('funded4_r5',4,5,False,1.1,600),('funded4_strict',4,25,False,1.3,1500)]
for name,cap,reserve,nomilk,ratio,gain in configs:
    values=dict(REPEAT=True,BUDGET=False,NOMILK=nomilk,CAP=cap,TO=264,RATIO=ratio,GAIN=gain)
    text=raw.decode()+'\n'+''.join('_K28E_'+k+'='+repr(v)+'\n' for k,v in values.items())
    text+=(D/'early_herd_tail.txt').read_text()+f'\n_K28S_RESERVE={reserve}\n'+(D/'funded_plan_tail.txt').read_text()
    text+='\n_K28S_ENTRY=agent\n_MP_REPORT={"early":_K28E_REPORT,"funding":_K28S_REPORT}\n'
    text+='\ndef funded_agent(observation,configuration=None):\n    if int(observation["step"])==0:\n        for key in _K28S_REPORT:_K28S_REPORT[key]=0\n    return _K28S_ENTRY(observation,configuration)\nfunded_agent.telemetry=_MP_REPORT\nagent=funded_agent\nkaggle_submission_agent=funded_agent\n'
    path=D/'candidates'/(name+'.py');compile(text,str(path),'exec');save(path,text.encode())
    variants.append(dict(name=name,path=path.relative_to(R).as_posix(),sha256=sha(text.encode()),reserve=reserve,parameters=values))
prior=json.loads((D/'herd_stage1_design.json').read_text());seeds=[1799657451]+prior['seeds'][:8]
def job(v,op,seed,seat):
    j=dict(candidate=v['path'],opponent=op['path'],family=op['family'],panel=op['panel'],seed=seed,seat=seat,candidate_sha256=v['sha256'],opponent_sha256=sha((R/op['path']).read_bytes()))
    j['id']=sha(json.dumps(j,sort_keys=True).encode())[:24];return j
jobs=[job(v,op,seed,seat) for v in variants for op in prior['roster'] for seed in seeds for seat in (0,1)]
diagnostic=[job(v,op,op['seed'],op['seat']) for v in variants for op in json.loads((D/'replay_opponents.json').read_text())]
for name,data in [('funded_design.json',dict(variants=variants,seeds=seeds,roster=prior['roster'])),('funded_jobs.json',jobs),('funded_diagnostic_jobs.json',diagnostic)]:
    save(D/name,json.dumps(data,indent=2).encode())
print(json.dumps(dict(variants=len(variants),league=len(jobs),diagnostic=len(diagnostic))),flush=True)

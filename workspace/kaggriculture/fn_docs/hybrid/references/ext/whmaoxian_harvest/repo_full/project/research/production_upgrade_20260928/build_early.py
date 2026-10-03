"""Reproducible earlier-herd population and public-replay diagnostic opponents."""
from pathlib import Path
import gzip,hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1];M=R/'research/meta_rebuild_20260927'
sha=lambda raw:hashlib.sha256(raw).hexdigest()
base_path='submissions/release_v10_r2/main.py';raw=(R/base_path).read_bytes()
assert sha(raw)=='b35b5b09fbec059ab7cbd2ba67a9fbb6d3e467ef5262f3e2ddba592b3e50c1c4'
assert b'_K28E_' not in raw
(D/'candidates').mkdir(exist_ok=True);(D/'replay_opponents').mkdir(exist_ok=True)
def save(path,data):
    if path.exists():assert path.read_bytes()==data
    else:path.write_bytes(data)
configs=[('early_single',False,True,False,1,216,1.1,600),('early_repeat2',True,True,False,2,264,1.1,600),('early_repeat4',True,True,False,4,264,1.1,600),('early_nomilk4',True,True,True,4,264,1.1,600),('early_force2',True,False,True,2,264,0,-1000000),('early_strict4',True,True,False,4,264,1.3,1500)]
variants=[]
for name,repeat,budget,nomilk,cap,to,ratio,gain in configs:
    values=dict(REPEAT=repeat,BUDGET=budget,NOMILK=nomilk,CAP=cap,TO=to,RATIO=ratio,GAIN=gain)
    constants='\n'+''.join('_K28E_'+k+'='+repr(v)+'\n' for k,v in values.items())
    data=raw+constants.encode()+(D/'early_herd_tail.txt').read_bytes()
    path=D/'candidates'/(name+'.py');compile(data,str(path),'exec');save(path,data)
    variants.append(dict(name=name,path=path.relative_to(R).as_posix(),sha256=sha(data),parameters=values))
def job(v,op,seed,seat):
    j=dict(candidate=v['path'],opponent=op['path'],family=op['family'],panel=op['panel'],seed=seed,seat=seat,candidate_sha256=v['sha256'],opponent_sha256=sha((R/op['path']).read_bytes()))
    j['id']=sha(json.dumps(j,sort_keys=True).encode())[:24];return j
prior=json.loads((D/'herd_stage1_design.json').read_text())
seeds=[1799657451]+prior['seeds'][:4]
jobs=[job(v,op,seed,seat) for v in variants for op in prior['roster'] for seed in seeds for seat in (0,1)]
save(D/'early_jobs.json',json.dumps(jobs,indent=2).encode())
save(D/'early_design.json',json.dumps(dict(variants=variants,seeds=seeds,roster=prior['roster'],scope='Development screen; not final validation.'),indent=2).encode())
diagnostic=[];replay_manifest=[]
for row in json.loads((M/'r2_feedback/selection.json').read_text()):
    game=json.loads(gzip.decompress((M/'r2_feedback'/f"{row['episode']}.json.gz").read_bytes()))
    tape=[game['steps'][t+1][1-row['seat']]['action'] for t in range(719)]
    text='import copy\n_TAPE='+repr(tape)+'\ndef agent(observation,configuration=None):\n    step=int(observation["step"])\n    return copy.deepcopy(_TAPE[step]) if step<len(_TAPE) else {"farmer":["PASS"],"hands":[],"market":[]}\n'
    path=D/'replay_opponents'/f"episode_{row['episode']}.py";compile(text,str(path),'exec');save(path,text.encode())
    op=dict(path=path.relative_to(R).as_posix(),family='replay_'+str(row['episode']),panel='fixed_replay_diagnostic')
    replay_manifest.append(dict(op,episode=row['episode'],seat=row['seat'],seed=game['info']['seed'],recorded_margin=row['margin'],sha256=sha(text.encode())))
    for v in variants+prior['variants'][:1]+[prior['variants'][2]]:
        diagnostic.append(job(v,op,game['info']['seed'],row['seat']))
save(D/'replay_diagnostic_jobs.json',json.dumps(diagnostic,indent=2).encode())
save(D/'replay_opponents.json',json.dumps(replay_manifest,indent=2).encode())
print(json.dumps(dict(new_variants=len(variants),development_cases=len(jobs),diagnostic_cases=len(diagnostic),diagnostic_warning='Recorded opponents cannot adapt to interventions.')),flush=True)

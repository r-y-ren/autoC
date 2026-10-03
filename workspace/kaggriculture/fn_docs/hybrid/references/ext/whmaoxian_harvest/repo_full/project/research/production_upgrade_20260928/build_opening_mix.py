"""Initial mix ablations; compare on the same full-game opponent panel."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1]
source=D/'candidates/fused_finish.py';raw=source.read_bytes()
assert hashlib.sha256(raw).hexdigest()=='71ed6dacfa1b196c5b6c6329bef22c9133e523db53b5215175f23db1dd7c2971'
def save(path,data):
    if path.exists():assert path.read_bytes()==data
    else:path.write_bytes(data)
variants=[]
for count in (1,2):
    text=raw.decode()+f'\n_K28O_COUNT={count}\n'+(D/'opening_goose_tail.txt').read_text()
    path=D/'candidates'/f'opening_goose{count}.py';compile(text,str(path),'exec');save(path,text.encode())
    variants.append(dict(name=path.stem,path=path.relative_to(R).as_posix(),sha256=hashlib.sha256(text.encode()).hexdigest()))
prior=json.loads((D/'fusion_design.json').read_text());seeds=prior['seeds']
def job(v,op,seed,seat):
    j=dict(candidate=v['path'],opponent=op['path'],family=op['family'],panel=op['panel'],seed=seed,seat=seat,candidate_sha256=v['sha256'],opponent_sha256=hashlib.sha256((R/op['path']).read_bytes()).hexdigest())
    j['id']=hashlib.sha256(json.dumps(j,sort_keys=True).encode()).hexdigest()[:24];return j
jobs=[job(v,op,seed,seat) for v in variants for op in prior['roster'] for seed in seeds for seat in (0,1)]
diagnostic=[job(v,op,op['seed'],op['seat']) for v in variants for op in json.loads((D/'replay_opponents.json').read_text())]
for name,data in [('opening_mix_jobs.json',jobs),('opening_mix_diagnostic_jobs.json',diagnostic),('opening_mix_design.json',dict(variants=variants,seeds=seeds,roster=prior['roster'],scope='Capital and earlier-production experiment; not a release.'))]:
    save(D/name,json.dumps(data,indent=2).encode())
print(json.dumps(dict(variants=len(variants),games=len(jobs),diagnostic=len(diagnostic))),flush=True)

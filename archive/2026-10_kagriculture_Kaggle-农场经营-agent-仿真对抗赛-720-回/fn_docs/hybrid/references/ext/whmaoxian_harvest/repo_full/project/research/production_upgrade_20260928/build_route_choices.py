"""Existing-route ablations on the declared Yarn development stratum."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1];M=R/'research/meta_rebuild_20260927'
sha=lambda raw:hashlib.sha256(raw).hexdigest()
raw=(D/'candidates/fused_finish.py').read_bytes()
assert sha(raw)=='71ed6dacfa1b196c5b6c6329bef22c9133e523db53b5215175f23db1dd7c2971'
def save(path,data):
    if path.exists():assert path.read_bytes()==data
    else:path.write_bytes(data)
variants=[]
for route in (3,5,6,7,8,9,10,11,12,109,126,127,128,'oldmap'):
    text=raw.decode()+f'\n_K28R_MODE={"oldmap" if route=="oldmap" else "fixed"!r}\n_K28R_ROUTE={route if isinstance(route,int) else 9}\n'
    text+=(D/'route_choice_tail.txt').read_text()
    path=D/'candidates'/f'route_{route}.py';compile(text,str(path),'exec');save(path,text.encode())
    variants.append(dict(name=path.stem,path=path.relative_to(R).as_posix(),route=route,sha256=sha(text.encode())))
prior=json.loads((D/'herd_stage1_design.json').read_text())
old=[json.loads(line) for line in (M/'midgame_herd_results.jsonl').read_text().splitlines()]
new=[json.loads(line) for line in (D/'herd_stage1_results.jsonl').read_text().splitlines()]
seed_shops={r['seed']:r['shops'][:2] for r in old+new if r.get('valid')}
seeds=sorted(s for s,shops in seed_shops.items() if 'YARN_STORE' in shops)
def job(v,op,seed,seat):
    j=dict(candidate=v['path'],opponent=op['path'],family=op['family'],panel=op['panel'],seed=seed,seat=seat,candidate_sha256=v['sha256'],opponent_sha256=sha((R/op['path']).read_bytes()))
    j['id']=sha(json.dumps(j,sort_keys=True).encode())[:24];return j
jobs=[job(v,op,seed,seat) for v in variants for op in prior['roster'] for seed in seeds for seat in (0,1)]
smoke=[j for j in jobs if j['seed']==1799657451 and j['family']=='r2']
replays=json.loads((D/'replay_opponents.json').read_text())
diagnostic=[job(v,op,op['seed'],op['seat']) for v in variants for op in replays]
for name,data in [('route_choice_design.json',dict(variants=variants,seeds=seeds,seed_shops={s:seed_shops[s] for s in seeds},roster=prior['roster'],scope='Yarn-focused DEVELOPMENT stratum from previously declared worlds; non-Yarn routes are unchanged.')),('route_choice_jobs.json',jobs),('route_preflight_jobs.json',smoke),('route_diagnostic_jobs.json',diagnostic)]:
    save(D/name,json.dumps(data,indent=2).encode())
print(json.dumps(dict(variants=len(variants),worlds=len(seeds),games=len(jobs),preflight=len(smoke),diagnostic=len(diagnostic))),flush=True)

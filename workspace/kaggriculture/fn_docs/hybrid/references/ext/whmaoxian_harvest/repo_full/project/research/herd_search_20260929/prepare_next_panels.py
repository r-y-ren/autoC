"""Finish declared development worlds and add archived style diversity."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1]
sha=lambda b:hashlib.sha256(b).hexdigest()
wide=json.loads((D/'herd_extended_design.json').read_text())
repeat=json.loads((D/'repeated_design.json').read_text())
proxies=json.loads((D/'archived_opponents.json').read_text())
base=next(v for v in wide['variants'] if v['name']=='r2')
def job(v,op,seed,seat):
    assert sha((R/v['path']).read_bytes())==v['sha256']
    j=dict(candidate=v['path'],opponent=op['path'],family=op['family'],panel=op['panel'],seed=seed,seat=seat,candidate_sha256=v['sha256'],opponent_sha256=sha((R/op['path']).read_bytes()))
    j['id']=sha(json.dumps(j,sort_keys=True).encode())[:24];return j
jobs=[job(v,op,seed,seat) for v in repeat['variants'] for op in wide['roster'] for seed in wide['seeds'][4:] for seat in (0,1)]
selected=[base]+[v for v in repeat['variants'] if v['name'] in ('early_one','repeat_early','repeat_ev')]
archived=[job(v,op,seed,seat) for v in selected for op in proxies for seed in [op['seed']]+wide['seeds'][:3] for seat in (0,1)]
for name,data in [('repeated_extended_jobs.json',jobs),('archived_panel_jobs.json',archived),('next_panel_design.json',dict(repeated_worlds=wide['seeds'][4:],repeated_variants=repeat['variants'],archived_variants=selected,archived_roster=proxies,archived_extra_seeds=wide['seeds'][:3],scope='Development only. Archived proxies are not current private leaders.'))]:
    p=D/name;s=json.dumps(data,indent=2)
    if p.exists():assert p.read_text()==s
    else:p.write_text(s)
print(json.dumps(dict(extended=len(jobs),archived=len(archived))),flush=True)

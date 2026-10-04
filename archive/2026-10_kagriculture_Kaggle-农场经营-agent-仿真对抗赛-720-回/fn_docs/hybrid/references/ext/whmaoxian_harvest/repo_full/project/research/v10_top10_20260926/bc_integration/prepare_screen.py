"""Predeclare finite development jobs. No held-out replays are opened."""
from pathlib import Path
import hashlib,json
B=Path(__file__).resolve().parent; D=B.parent; R=B.parents[2]
manifest=json.loads((B/'candidates.json').read_text())
design=json.loads((D/'route_expansion_design.json').read_text())
base='submissions/release_v10_r2/main.py'
candidates=[m['path'] for m in manifest]+[base]
seeds=design['seeds'][:2]; jobs=[]
for candidate in candidates:
    for opponent in design['roster']:
        for seed in seeds:
            for seat in (0,1):
                job=dict(candidate=candidate,opponent=opponent['path'],seed=seed,seat=seat,
                         family=opponent['family'],panel=opponent['panel'])
                for key in ('candidate','opponent'):
                    job[key+'_sha256']=hashlib.sha256((R/job[key]).read_bytes()).hexdigest()
                job['id']=hashlib.sha256(json.dumps(job,sort_keys=True).encode()).hexdigest()[:24]
                jobs.append(job)
shadow=manifest[0]['path']
smoke=[j for j in jobs if j['candidate'] in (base,shadow) and j['family'] in ('fieldcraft','top_style_03')]
assert len(smoke)==16 and len(jobs)==396
for name,data in [('shadow_jobs.json',smoke),('screen_jobs.json',jobs)]:
    path=B/name
    if path.exists():assert json.loads(path.read_text())==data
    else:path.write_text(json.dumps(data,indent=2),encoding='utf-8')
(B/'screen_protocol.json').write_text(json.dumps(dict(seeds=seeds,roster=design['roster'],candidates=manifest,baseline=base,scope='Two previously seen development worlds; no ranking estimate or final confirmation.'),indent=2),encoding='utf-8')
print(json.dumps(dict(shadow_games=len(smoke),screen_games=len(jobs),heldout_used=False)),flush=True)

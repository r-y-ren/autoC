"""Paired development runs for the reservation-protected holding policies."""
from pathlib import Path
import hashlib,json
B=Path(__file__).resolve().parent;R=B.parents[2]
manifest=json.loads((B/'guarded_candidates.json').read_text())
design=json.loads((B/'extended_protocol.json').read_text());jobs=[]
for spec in manifest:
    candidate=spec['path']
    assert hashlib.sha256((R/candidate).read_bytes()).hexdigest()==spec['sha256']
    for opponent in design['roster']:
        for seed in design['seeds']:
            for seat in (0,1):
                job=dict(candidate=candidate,opponent=opponent['path'],family=opponent['family'],panel=opponent['panel'],seed=seed,seat=seat)
                for key in ('candidate','opponent'):job[key+'_sha256']=hashlib.sha256((R/job[key]).read_bytes()).hexdigest()
                job['id']=hashlib.sha256(json.dumps(job,sort_keys=True).encode()).hexdigest()[:24];jobs.append(job)
assert len(jobs)==528
path=B/'guarded_jobs.json'
if path.exists():assert json.loads(path.read_text())==jobs
else:path.write_text(json.dumps(jobs,indent=2),encoding='utf-8')
(B/'guarded_protocol.json').write_text(json.dumps(dict(variants=manifest,seeds=design['seeds'],roster=design['roster'],new_games=528,baseline_reference='extended_results.jsonl',scope='Development safety revision, not independent confirmation. Unguarded holding variants are not release-eligible.'),indent=2),encoding='utf-8')
print(json.dumps(dict(new_games=528,baseline_games_reused_later=176)),flush=True)

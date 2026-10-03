"""Matched local simulation jobs for same-position farm improvements."""
from pathlib import Path
import hashlib,json
N=Path(__file__).resolve().parent;R=N.parents[1]
manifest=json.loads((N/'micro_candidates_manifest.json').read_text())
design=json.loads((N/'flow_screen_v2_design.json').read_text());jobs=[]
for candidate in manifest:
    path=R/candidate['path'];assert hashlib.sha256(path.read_bytes()).hexdigest()==candidate['sha256']
    for opponent in design['roster']:
        for seed in design['seeds']:
            for seat in (0,1):
                job=dict(candidate=candidate['path'],opponent=opponent['path'],family=opponent['family'],
                    panel=opponent['panel'],seed=seed,seat=seat,candidate_sha256=candidate['sha256'],
                    opponent_sha256=hashlib.sha256((R/opponent['path']).read_bytes()).hexdigest())
                job['id']=hashlib.sha256(json.dumps(job,sort_keys=True).encode()).hexdigest()[:24]
                jobs.append(job)
(N/'micro_screen_jobs.json').write_text(json.dumps(jobs,indent=2),encoding='utf-8')
print(json.dumps(dict(candidates=len(manifest),games=len(jobs))),flush=True)

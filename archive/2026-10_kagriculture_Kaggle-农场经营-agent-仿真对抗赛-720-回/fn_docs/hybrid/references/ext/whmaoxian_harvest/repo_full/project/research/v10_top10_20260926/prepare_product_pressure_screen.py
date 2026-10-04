"""Two-world pilot on the existing development design, never a holdout test."""
from pathlib import Path
import hashlib, json
D=Path(__file__).resolve().parent; R=D.parents[1]
variants=json.loads((D/'product_pressure_manifest.json').read_text())
design=json.loads((D/'route_expansion_design.json').read_text())
controls=['submissions/release_v10_r2/main.py','research/v10_top10_20260926/micro_candidates/all_care_first.py']
jobs=[]
for candidate in [v['path'] for v in variants]+controls:
    for opponent in design['roster']:
        for seed in design['seeds'][:2]:
            for seat in (0,1):
                job=dict(candidate=candidate,opponent=opponent['path'],family=opponent['family'],panel=opponent['panel'],seed=seed,seat=seat)
                for key in ('candidate','opponent'):job[key+'_sha256']=hashlib.sha256((R/job[key]).read_bytes()).hexdigest()
                job['id']=hashlib.sha256(json.dumps(job,sort_keys=True).encode()).hexdigest()[:24];jobs.append(job)
expected={j['id']:j for j in jobs}; cached=[]
for line in (D/'route_expansion_results.jsonl').read_text(encoding='utf-8').splitlines():
    row=json.loads(line)
    if row['id'] in expected and row.get('valid'):
        assert all(row.get(k)==v for k,v in expected[row['id']].items());cached.append(row)
ledger=D/'product_pressure_screen_results.jsonl'; assert not ledger.exists()
ledger.write_text(''.join(json.dumps(r)+'\n' for r in cached),encoding='utf-8')
(D/'product_pressure_screen_jobs.json').write_text(json.dumps(jobs,indent=2),encoding='utf-8')
(D/'product_pressure_screen_design.json').write_text(json.dumps(dict(variants=variants,seeds=design['seeds'][:2],roster=design['roster'],total=len(jobs),cached=len(cached),scope='Pilot development; not independent validation.'),indent=2),encoding='utf-8')
print(json.dumps(dict(total=len(jobs),cached=len(cached),fresh=len(jobs)-len(cached))),flush=True)

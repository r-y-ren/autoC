"""Finite development screen; reused controls and known-trigger diagnostics are separate."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1]
variants=json.loads((D/'production_quote_manifest.json').read_text())
design=json.loads((D/'route_expansion_design.json').read_text())
roster=[r for r in design['roster'] if r['panel']=='public_program' or r['family'] in ('top_style_02','top_style_03')]
candidates=[r['path'] for r in variants]+['submissions/release_v10_r2/main.py']
jobs=[]
for candidate in candidates:
    for opponent in roster:
        for seed in design['seeds']:
            for seat in (0,1):
                job=dict(candidate=candidate,opponent=opponent['path'],family=opponent['family'],panel=opponent['panel'],seed=seed,seat=seat)
                for key in ('candidate','opponent'):job[key+'_sha256']=hashlib.sha256((R/job[key]).read_bytes()).hexdigest()
                job['id']=hashlib.sha256(json.dumps(job,sort_keys=True).encode()).hexdigest()[:24];jobs.append(job)
    for seat in (0,1):
        opponent='submissions/release_v10_r2/main.py'
        job=dict(candidate=candidate,opponent=opponent,family='known_trigger_r2',panel='known_trigger_diagnostic',seed=688041503,seat=seat)
        for key in ('candidate','opponent'):job[key+'_sha256']=hashlib.sha256((R/job[key]).read_bytes()).hexdigest()
        job['id']=hashlib.sha256(json.dumps(job,sort_keys=True).encode()).hexdigest()[:24];jobs.append(job)
assert len(jobs)==910
prior_path=D/'route_expansion_results.jsonl'
prior=[json.loads(s) for s in prior_path.read_text(encoding='utf-8').splitlines() if s.strip()]
needed={j['id']:j for j in jobs};cached=[]
for row in prior:
    if row['id'] in needed and row.get('valid'):
        assert all(row.get(k)==v for k,v in needed[row['id']].items())
        cached.append(row)
target=D/'production_screen_results.jsonl'
assert not target.exists(),'Do not overwrite an existing development ledger'
target.write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in cached),encoding='utf-8')
(D/'production_screen_jobs.json').write_text(json.dumps(jobs,indent=2),encoding='utf-8')
record=dict(variants=variants,seeds=design['seeds'],roster=roster,total_jobs=len(jobs),reused_controls=len(cached),fresh_required=len(jobs)-len(cached),known_trigger_jobs=14,scope='Development. Known trigger is never used for population win rates. Cash, physical routing, time feasibility and the 500-coin modeled profit gate remain unchanged.')
(D/'production_screen_design.json').write_text(json.dumps(record,indent=2),encoding='utf-8')
print(json.dumps({k:record[k] for k in ('total_jobs','reused_controls','fresh_required','known_trigger_jobs')}),flush=True)

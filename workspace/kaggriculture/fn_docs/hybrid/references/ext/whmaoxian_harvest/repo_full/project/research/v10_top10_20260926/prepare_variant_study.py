"""Prepare one finite, hash-locked development study from existing variants."""
from pathlib import Path
import hashlib,json,re,sys
D=Path(__file__).resolve().parent;R=D.parents[1]
name=sys.argv[1];assert re.fullmatch('[a-z][a-z0-9_]*',name)
variants=json.loads((D/(name+'_manifest.json')).read_text())
design=json.loads((D/'route_expansion_design.json').read_text())
controls=['submissions/release_v10_r2/main.py','research/v10_top10_20260926/micro_candidates/all_care_first.py']
candidates=[v['path'] for v in variants]+controls
for v in variants:assert hashlib.sha256((R/v['path']).read_bytes()).hexdigest()==v['sha256']
jobs=[]
for candidate in candidates:
    for opponent in design['roster']:
        for seed in design['seeds']:
            for seat in (0,1):
                job=dict(candidate=candidate,opponent=opponent['path'],family=opponent['family'],panel=opponent['panel'],seed=seed,seat=seat)
                for key in ('candidate','opponent'):job[key+'_sha256']=hashlib.sha256((R/job[key]).read_bytes()).hexdigest()
                job['id']=hashlib.sha256(json.dumps(job,sort_keys=True).encode()).hexdigest()[:24];jobs.append(job)
needed={j['id']:j for j in jobs};assert len(needed)==len(jobs)
cached=[]
for line in (D/'route_expansion_results.jsonl').read_text(encoding='utf-8').splitlines():
    row=json.loads(line)
    if row['id'] in needed and row.get('valid'):
        assert all(row.get(k)==v for k,v in needed[row['id']].items());cached.append(row)
output=D/(name+'_results.jsonl');assert not output.exists(),'Existing ledger must not be overwritten'
output.write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in cached),encoding='utf-8')
(D/(name+'_jobs.json')).write_text(json.dumps(jobs,indent=2),encoding='utf-8')
record=dict(variants=variants,controls=controls,seeds=design['seeds'],roster=design['roster'],total_jobs=len(jobs),reused_controls=len(cached),fresh_required=len(jobs)-len(cached),scope='Development only, on the previously declared eight-world design; not independent confirmation.')
(D/(name+'_design.json')).write_text(json.dumps(record,indent=2),encoding='utf-8')
print(json.dumps({k:record[k] for k in ('total_jobs','reused_controls','fresh_required')}),flush=True)

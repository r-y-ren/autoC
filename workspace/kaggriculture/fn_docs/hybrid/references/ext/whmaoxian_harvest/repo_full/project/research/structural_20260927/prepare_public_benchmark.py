"""Benchmark reviewed exact public releases against the same local field as R2."""
from pathlib import Path
import hashlib,json
P=Path(__file__).resolve().parent;R=P.parents[1]
review=json.loads((P/'public_notebooks/runtime_review.json').read_text())
assert all(not r['present'] and all(not e['review_calls'] for e in r['embedded']) for r in review)
sources=json.loads((P/'public_notebooks/source_review.json').read_text())
variants=[s['path'] for s in sources];base='submissions/release_v10_r2/main.py'
design=json.loads((P/'plan_extended_design.json').read_text());seeds=design['seeds'][:8];jobs=[]
for candidate in variants+[base]:
    for rival in design['roster']:
        for seed in seeds:
            for seat in (0,1):
                row=dict(candidate=candidate,opponent=rival['path'],family=rival['family'],panel=rival['panel'],seed=seed,seat=seat)
                for key in ('candidate','opponent'):row[key+'_sha256']=hashlib.sha256((R/row[key]).read_bytes()).hexdigest()
                row['id']=hashlib.sha256(json.dumps(row,sort_keys=True).encode()).hexdigest()[:24];jobs.append(row)
expected={j['id']:j for j in jobs};old=[json.loads(s) for s in (P/'plan_extended_results.jsonl').read_text().splitlines()]
cached=[r for r in old if r['id'] in expected and r['candidate']==base]
for row in cached:assert row['valid'] and all(row.get(k)==v for k,v in expected[row['id']].items())
output=P/'public_benchmark_results.jsonl'
if not output.exists():output.write_text(''.join(json.dumps(r)+'\n' for r in cached))
for name,data in [('public_benchmark_jobs.json',jobs),('public_benchmark_design.json',dict(variants=variants,seeds=seeds,roster=design['roster'],total=len(jobs),reused_controls=len(cached),fresh=len(jobs)-len(cached),scope='Reviewed original public code. Historical advertised ratings are not current calibrated strength.'))]:
    path=P/name
    if path.exists():assert json.loads(path.read_text())==data
    else:path.write_text(json.dumps(data,indent=2))
print(json.dumps(dict(jobs=len(jobs),reused=len(cached),new_games=len(jobs)-len(cached))),flush=True)

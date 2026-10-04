"""Paired early-capital development on declared route-screen worlds."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1]
variants=json.loads((D/'early_liquidity_manifest.json').read_text())
design=json.loads((D/'route_design.json').read_text());base='submissions/release_v10_r2/main.py'
jobs=[]
for candidate in [v['path'] for v in variants]+[base]:
    for opponent in design['roster']:
        for seed in design['seeds']:
            for seat in (0,1):
                j=dict(candidate=candidate,opponent=opponent['path'],family=opponent['family'],panel=opponent['panel'],seed=seed,seat=seat)
                for key in ('candidate','opponent'):j[key+'_sha256']=hashlib.sha256((R/j[key]).read_bytes()).hexdigest()
                j['id']=hashlib.sha256(json.dumps(j,sort_keys=True).encode()).hexdigest()[:24];jobs.append(j)
expected={j['id']:j for j in jobs}
controls=[json.loads(s) for s in (D/'route_results.jsonl').read_text().splitlines()]
controls=[r for r in controls if r['candidate']==base and r['id'] in expected]
for row in controls:
    assert row['valid'] and all(row.get(k)==v for k,v in expected[row['id']].items())
output=D/'early_liquidity_results.jsonl';assert not output.exists()
output.write_text(''.join(json.dumps(r)+'\n' for r in controls))
(D/'early_liquidity_jobs.json').write_text(json.dumps(jobs,indent=2))
(D/'early_liquidity_design.json').write_text(json.dumps(dict(seeds=design['seeds'],roster=design['roster'],variants=variants,total=len(jobs),reused_controls=len(controls),fresh=len(jobs)-len(controls),scope='Development, not independent final confirmation.'),indent=2))
print(json.dumps(dict(jobs=len(jobs),reused=len(controls),fresh=len(jobs)-len(controls))),flush=True)

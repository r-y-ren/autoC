"""Prepare explicit finite shadow and closed-loop development manifests."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1]
variants=json.loads((D/'cycle_agents_manifest.json').read_text());design=json.loads((D/'route_design.json').read_text())
base='submissions/release_v10_r2/main.py';jobs=[]
for candidate in [v['path'] for v in variants]+[base]:
    for opponent in design['roster']:
        for seed in design['seeds']:
            for seat in (0,1):
                j=dict(candidate=candidate,opponent=opponent['path'],family=opponent['family'],panel=opponent['panel'],seed=seed,seat=seat)
                for key in ('candidate','opponent'):j[key+'_sha256']=hashlib.sha256((R/j[key]).read_bytes()).hexdigest()
                j['id']=hashlib.sha256(json.dumps(j,sort_keys=True).encode()).hexdigest()[:24];jobs.append(j)
shadow=[j for j in jobs if (j['candidate']==base or j['candidate'].endswith('/shadow.py')) and j['family'] in ('fieldcraft','top_style_03') and j['seed'] in design['seeds'][:2]]
old=[json.loads(s) for s in (D/'route_results.jsonl').read_text().splitlines()]
for name,selected in [('cycle_shadow',shadow),('cycle_screen',jobs)]:
    expected={j['id']:j for j in selected}
    cached=[r for r in old if r['candidate']==base and r['id'] in expected]
    for row in cached:assert row['valid'] and all(row.get(k)==v for k,v in expected[row['id']].items())
    output=D/(name+'_results.jsonl');assert not output.exists()
    output.write_text(''.join(json.dumps(r)+'\n' for r in cached))
    (D/(name+'_jobs.json')).write_text(json.dumps(selected,indent=2))
    print(json.dumps(dict(batch=name,total=len(selected),reused=len(cached),fresh=len(selected)-len(cached))),flush=True)
(D/'cycle_screen_design.json').write_text(json.dumps(dict(variants=variants,seeds=design['seeds'],roster=design['roster'],heldout_used=False,scope='Development; public implementations and reconstructed proxies kept separate.'),indent=2))

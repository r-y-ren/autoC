"""Prospective paired screening; no leaderboard scores inferred from proxies."""
from pathlib import Path
import hashlib,json
P=Path(__file__).resolve().parent;R=P.parents[1]
variants=json.loads((P/'plan_manifest.json').read_text())
roster=json.loads((R/'research/macro_population_20260927/roster.json').read_text())
roster=[r for r in roster if r['family'] in ('fieldcraft','aurax','top_style_03','r2')]
seeds=[int.from_bytes(hashlib.sha256(f'structural-screen-20260927-{i}'.encode()).digest()[:4],'big')%2000000000 for i in range(3)]
assert len(set(seeds))==3
paths=[v['path'] for v in variants]+['submissions/release_v10_r2/main.py']
jobs=[]
for candidate in paths:
    for rival in roster:
        for seed in seeds:
            for seat in (0,1):
                row=dict(candidate=candidate,opponent=rival['path'],family=rival['family'],panel=rival['panel'],seed=seed,seat=seat)
                for key in ('candidate','opponent'):row[key+'_sha256']=hashlib.sha256((R/row[key]).read_bytes()).hexdigest()
                row['id']=hashlib.sha256(json.dumps(row,sort_keys=True).encode()).hexdigest()[:24];jobs.append(row)
for name,data in [('plan_screen_jobs.json',jobs),('plan_screen_design.json',dict(seeds=seeds,roster=roster,variants=variants,total=len(jobs),scope='First-stage development, not final confirmation.'))]:
    p=P/name
    if p.exists():assert json.loads(p.read_text())==data
    else:p.write_text(json.dumps(data,indent=2),encoding='utf-8')
print(json.dumps(dict(jobs=len(jobs),worlds=len(seeds),candidates=len(paths))),flush=True)

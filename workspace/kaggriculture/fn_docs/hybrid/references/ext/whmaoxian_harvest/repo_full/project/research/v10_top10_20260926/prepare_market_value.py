"""Screen on a declared hard development panel; no held-out access."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1]
variants=json.loads((D/'market_value_manifest.json').read_text())
base='submissions/release_v10_r2/main.py'
design=json.loads((D/'route_expansion_design.json').read_text())
roster=[r for r in design['roster'] if r['family'] in ('fieldcraft','marketshock','top_style_02','top_style_03','r2')]
roster.append(dict(path='research/v10_rebuild_20260926/continuation/generation5/advance36.py',family='counter_phase_a',panel='counter_population'))
assert len({r['path'] for r in roster})==len(roster)==6
seeds=design['seeds'][:2];jobs=[]
for candidate in [v['path'] for v in variants]+[base]:
    for opponent in roster:
        for seed in seeds:
            for seat in (0,1):
                j=dict(candidate=candidate,opponent=opponent['path'],family=opponent['family'],panel=opponent['panel'],seed=seed,seat=seat)
                for key in ('candidate','opponent'):j[key+'_sha256']=hashlib.sha256((R/j[key]).read_bytes()).hexdigest()
                j['id']=hashlib.sha256(json.dumps(j,sort_keys=True).encode()).hexdigest()[:24];jobs.append(j)
assert len({j['id'] for j in jobs})==len(jobs)
(D/'market_value_jobs.json').write_text(json.dumps(jobs,indent=2),encoding='utf-8')
(D/'market_value_design.json').write_text(json.dumps(dict(variants=variants,seeds=seeds,roster=roster,total_jobs=len(jobs),scope='Development screen only; public implementations, reconstructions and self-derived counters are distinct evidence types.'),indent=2),encoding='utf-8')
print(json.dumps(dict(jobs=len(jobs),candidates=len(variants)+1,unique_opponents=len(roster))),flush=True)

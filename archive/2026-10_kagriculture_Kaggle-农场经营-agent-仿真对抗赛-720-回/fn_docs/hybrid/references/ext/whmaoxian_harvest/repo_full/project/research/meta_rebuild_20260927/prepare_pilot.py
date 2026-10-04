"""Freeze a small two-seat development panel before observing any new results."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os
D=Path(__file__).resolve().parent;R=D.parents[1]
assert not os.environ.get('V92_SELL_LIB'),'External optional library must be absent'
old=json.loads((R/'research/macro_population_20260927/roster.json').read_text())
roster=[r for r in old if r['family'] in ('fieldcraft','r2')]
roster += [dict(path=(D/f'public_agents/{n}.py').relative_to(R).as_posix(),family=n,panel='new_public_program') for n in ('pipe16','dmitrii')]
variants=json.loads((D/'value_candidates.json').read_text())
paths=[v['path'] for v in variants]+['submissions/release_v10_r2/main.py']
paths += [(D/f'public_agents/{n}.py').relative_to(R).as_posix() for n in ('pipe16','metav4','dmitrii')]
seeds=[int.from_bytes(hashlib.sha256(f'meta-rebuild-development-20260927-{i}'.encode()).digest()[:4],'big')%2000000000 for i in range(2)]
jobs=[]
for candidate in paths:
    for opponent in roster:
        for seed in seeds:
            for seat in (0,1):
                job=dict(candidate=candidate,opponent=opponent['path'],family=opponent['family'],panel=opponent['panel'],seed=seed,seat=seat)
                for k in ('candidate','opponent'):job[k+'_sha256']=hashlib.sha256((R/job[k]).read_bytes()).hexdigest()
                job['id']=hashlib.sha256(json.dumps(job,sort_keys=True).encode()).hexdigest()[:24];jobs.append(job)
assert len(jobs)==len({j['id'] for j in jobs})
assert not (D/'pilot_jobs.json').exists()
(D/'pilot_jobs.json').write_text(json.dumps(jobs,indent=2))
(D/'pilot_design.json').write_text(json.dumps(dict(captured_utc=datetime.now(timezone.utc).isoformat(),seeds=seeds,roster=roster,candidates=paths,jobs=len(jobs),scope='Development. Public originals are reacting code, not current private leaders. No rating calibration.'),indent=2))
print(json.dumps(dict(jobs=len(jobs),candidates=len(paths),worlds=len(seeds))),flush=True)

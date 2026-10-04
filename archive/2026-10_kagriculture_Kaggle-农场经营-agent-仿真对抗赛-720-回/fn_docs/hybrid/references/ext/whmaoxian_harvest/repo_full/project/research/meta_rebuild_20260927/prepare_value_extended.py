"""Prospective multi-world outcome-policy development, preserving every old result."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1]
source=(D/'candidates/value5.py').read_bytes()+b'\n_VP_MIN_GAIN=1\n_VP_PROB=0.3\n_VP_COOLDOWN=24\n'
target=D/'candidates/value1.py';assert not target.exists();target.write_bytes(source)
roster=json.loads((R/'research/macro_population_20260927/roster.json').read_text())
roster=[r for r in roster if r['family']!='marketshock']
roster += [dict(path=(D/f'public_agents/{name}.py').relative_to(R).as_posix(),family=name,panel='new_public_program') for name in ('pipe16','dmitrii')]
paths=[(D/f'candidates/{name}.py').relative_to(R).as_posix() for name in ('value1','value5','value15')]
paths+=['submissions/release_v10_r2/main.py',(D/'public_agents/dmitrii.py').relative_to(R).as_posix()]
seeds=[int.from_bytes(hashlib.sha256(f'meta-value-wide-20260927-{i}'.encode()).digest()[:4],'big')%2000000000 for i in range(8)]
used=set(json.loads((D/'pilot_design.json').read_text())['seeds'])
used.update(json.loads((R/'research/value_policy_20260927/training_design.json').read_text())['worlds'])
assert not set(seeds)&used
jobs=[]
for candidate in paths:
    for opponent in roster:
        for seed in seeds:
            for seat in (0,1):
                job=dict(candidate=candidate,opponent=opponent['path'],family=opponent['family'],panel=opponent['panel'],seed=seed,seat=seat)
                for k in ('candidate','opponent'):job[k+'_sha256']=hashlib.sha256((R/job[k]).read_bytes()).hexdigest()
                job['id']=hashlib.sha256(json.dumps(job,sort_keys=True).encode()).hexdigest()[:24];jobs.append(job)
assert not (D/'value_extended_jobs.json').exists()
(D/'value_extended_jobs.json').write_text(json.dumps(jobs,indent=2))
(D/'value_extended_design.json').write_text(json.dumps(dict(captured_utc=datetime.now(timezone.utc).isoformat(),seeds=seeds,roster=roster,candidates=paths,jobs=len(jobs),scope='Prospective development, not final confirmation or a rating calibration.'),indent=2))
print(json.dumps(dict(jobs=len(jobs),worlds=len(seeds))),flush=True)

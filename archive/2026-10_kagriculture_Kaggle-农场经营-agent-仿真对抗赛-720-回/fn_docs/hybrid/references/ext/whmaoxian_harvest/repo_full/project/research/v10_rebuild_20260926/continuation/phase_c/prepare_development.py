"""Freeze a finite diagnostic-development batch. No final holdout outcomes used."""
from pathlib import Path
import hashlib,json
C=Path(__file__).resolve().parent;D=C.parent;W=D.parent;R=W.parents[1]
selection=json.loads((D/'phase_b/selection.json').read_text())
variants=json.loads((C/'candidates.json').read_text())
candidates=[v['path'] for v in variants]+[selection['candidate'],'submissions/release_v10/main.py']
prior=json.loads((D/'generation7_jobs.json').read_text())
seeds=sorted({j['seed'] for j in prior})[:8]
roster=json.loads((D/'phase_b/generation7_design.json').read_text())['roster']
roster=roster+[dict(path=p,family=n,panel='direct_reference') for n,p in (
 ('v9','submissions/release_v9/main.py'),('v10','submissions/release_v10/main.py'),
 ('phase_b',selection['candidate']))]
probes=[p for p in json.loads((W/'probe_roster.json').read_text()) if p['role'] in ('actual_v10_loss','unseen_trace')]
jobs=[]
def add(candidate,opponent,seed,seat,family,panel,**extra):
    job=dict(candidate=candidate,opponent=opponent,seed=seed,seat=seat,family=family,panel=panel,**extra)
    for key in ('candidate','opponent'):
        job[key+'_sha256']=hashlib.sha256((R/job[key]).read_bytes()).hexdigest()
    job['id']=hashlib.sha256(json.dumps(job,sort_keys=True).encode()).hexdigest()[:24]
    jobs.append(job)
for candidate in candidates:
    for opponent in roster:
        for seed in seeds:
            for seat in (0,1):
                add(candidate,opponent['path'],seed,seat,opponent['family'],opponent['panel'])
    for probe in probes:
        add(candidate,probe['path'],probe['seed'],1-probe['seat'],str(probe['episode']),probe['role'],episode=probe['episode'])
assert len({j['id'] for j in jobs})==len(jobs)
(C/'development_jobs.json').write_text(json.dumps(jobs,indent=2),encoding='utf-8')
(C/'DEVELOPMENT_PROTOCOL.md').write_text(
 'Phase C tests public-state cargo readiness. Phase A/B outcomes are now seen diagnostic data. '
 'The batch includes all six public programs, three adversarial variants, three direct references, '
 'and fixed-replay diagnostics. Replays are not equivalent to reactive private agents. '
 'Any revised source needs fresh frozen final worlds; do not reuse prior holdouts as unseen.\n',encoding='utf-8')
print(json.dumps(dict(jobs=len(jobs),candidates=len(candidates),worlds=len(seeds),roster=len(roster),probes=len(probes))),flush=True)

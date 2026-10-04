"""Post-freeze counterfactual replay probes; never rating or private-agent evidence."""
from pathlib import Path
import hashlib,json
B=Path(__file__).resolve().parent;D=B.parent;W=D.parent;R=W.parents[1]
selection=json.loads((B/'selection.json').read_text())
probes=[p for p in json.loads((W/'probe_roster.json').read_text()) if p['role'] in ('actual_v10_loss','unseen_trace')]
candidates=[selection['candidate'],'submissions/release_v9/main.py','submissions/release_v10/main.py']
jobs=[]
for candidate in candidates:
 for probe in probes:
  seat=1-probe['seat']
  job=dict(candidate=candidate,opponent=probe['path'],seed=probe['seed'],seat=seat,
   family=str(probe['episode']),panel='known_loss_recheck' if probe['role']=='actual_v10_loss' else 'current_ladder_fixed_replay',
   episode=probe['episode'],recorded_agent_submission=probe['submission'],
   replay_seat=probe['seat'],source_role=probe['role'],
   recorded_rewards=list(probe['rewards']),rating_at_capture=probe.get('rating'),
   candidate_sha256=hashlib.sha256((R/candidate).read_bytes()).hexdigest(),opponent_sha256=probe['sha256'])
  assert hashlib.sha256((R/probe['path']).read_bytes()).hexdigest()==probe['sha256']
  job['id']=hashlib.sha256(json.dumps(job,sort_keys=True).encode()).hexdigest()[:24];jobs.append(job)
assert len(jobs)==78
(B/'replay_recheck_jobs.json').write_text(json.dumps(jobs,indent=2),encoding='utf-8')
(B/'REPLAY_RECHECK_SCOPE.md').write_text('These are fixed-action counterfactual diagnostics. The original private agents cannot react to a changed market in these tests. Outcomes are not primary promotion points or evidence of defeating the currently ranked private programs. The source was frozen before these probes, and their seed values and opponent identities are not encoded in the candidate.\n',encoding='utf-8')
print('Prepared',len(jobs),'post-freeze diagnostic replay games; no change to candidate or acceptance gates')

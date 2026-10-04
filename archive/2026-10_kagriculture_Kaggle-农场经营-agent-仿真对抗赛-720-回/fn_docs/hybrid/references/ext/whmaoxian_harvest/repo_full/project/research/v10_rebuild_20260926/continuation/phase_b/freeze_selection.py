"""Freeze one Phase-B candidate from completed development results only."""
from pathlib import Path
import datetime,hashlib,json,sys
B=Path(__file__).resolve().parent;D=B.parent;W=D.parent;R=W.parents[1]
sys.path.insert(0,str(D));from assess import load,desc
rows=load(D/'generation7_results.jsonl');direct=load(D/'generation7_direct_results.jsonl')
assert len(rows)==1152 and len(direct)==128
assert all(r.get('valid') for r in rows+direct)
names=[(B/'generation6'/f'similarity{k}.py').relative_to(R).as_posix() for k in (90,95)]
ranked=[]
for name in names:
 public=[r for r in rows if r['candidate']==name and r['panel']=='public_program']
 counter=[r for r in rows if r['candidate']==name and r['panel']=='counter_population']
 dd={v:desc([r for r in direct if r['candidate']==name and r['family']==v]) for v in ('v9','v10')}
 assert len(public)==192 and len(counter)==96
 if any(value['points']<.65 for value in dd.values()):continue
 eligible=True
 for family in {r['family'] for r in public}:
  ca=desc([r for r in public if r['family']==family])
  old=desc([r for r in rows if r['candidate']=='submissions/release_v10/main.py' and r['family']==family])
  if ca['points']-old['points']<-.05:eligible=False
 if eligible:ranked.append((desc(public)['points'],desc(counter)['points'],min(v['points'] for v in dd.values()),desc(public)['mean_margin'],name,dd))
assert ranked,'No eligible development candidate; do not open new confirmation'
ranked.sort(reverse=True);best=ranked[0];name=best[4]
sha=hashlib.sha256((R/name).read_bytes()).hexdigest()
assert all(r['candidate_sha256']==sha for r in rows+direct if r['candidate']==name)
selection=dict(candidate=name,sha256=sha,entry='phase_b_agent',
 selected_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
 settings=dict(public_layout_similarity_gate=.90 if 'similarity90' in name else .95,
  aggressive_observed_stock_threshold=4,aggressive_advance_horizon=36,conservative_advance_horizon=12,
  conservative_sellnow_disabled=True,safe_initial_net_wheat=5,decay_correction=False,floor_correction=False),
 reason='Highest complete public-program win points among candidates satisfying all development family and direct-reference gates; counter-policy results and margin used as tie-breaks.',
 development_public=desc([r for r in rows if r['candidate']==name and r['panel']=='public_program']),
 development_counter=desc([r for r in rows if r['candidate']==name and r['panel']=='counter_population']),
 development_direct=best[5],style_outcomes_used_for_selection=False,
 rejected_phase_a_sha256='e03333c6bef0c83764d56f1cc958782f032c5bbdc0684bae1cc2ccd6b61f3e7c',
 evidence_hashes={tag:hashlib.sha256((D/f'{tag}_results.jsonl').read_bytes()).hexdigest() for tag in ('generation6','demand_dev','generation7','generation7_direct')})
target=B/'selection.json';assert not target.exists()
target.write_text(json.dumps(selection,indent=2),encoding='utf-8')
print(json.dumps(selection),flush=True)

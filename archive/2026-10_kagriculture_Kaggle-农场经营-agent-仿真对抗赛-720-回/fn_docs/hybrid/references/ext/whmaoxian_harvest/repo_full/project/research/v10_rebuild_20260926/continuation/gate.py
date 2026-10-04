"""Enforce the predeclared V10-R2 gate on complete frozen confirmation records."""
from pathlib import Path
import hashlib,json
from assess import load,desc,paired
D=Path(__file__).resolve().parent; R=D.parents[2]
def check():
 spec=json.loads((D/'selection.json').read_text()); name=spec['candidate']
 jobs=json.loads((D/'confirmation_jobs.json').read_text()); rows=load(D/'confirmation_results.jsonl')
 assert len(rows)==len(jobs)==1920
 assert {r['id'] for r in rows}=={r['id'] for r in jobs}
 assert len({r['id'] for r in rows})==len(rows)
 for p in {r[k]:r[k+'_sha256'] for r in jobs for k in ('candidate','opponent')}.items():
  assert hashlib.sha256((R/p[0]).read_bytes()).hexdigest()==p[1],p[0]
 candidate=[r for r in rows if r['candidate']==name and r['panel']=='public_program']
 public={v:[r for r in rows if r['candidate']==f'submissions/release_{v}/main.py' and r['panel']=='public_program'] for v in ('v9','v10')}
 reasons=[]
 if not all(r.get('valid') for r in rows):reasons.append('invalid_games')
 gains={v:paired(candidate,group) for v,group in public.items()}
 if not gains['v10'].get('complete') or gains['v10']['world_bootstrap_95'][0]<=0:reasons.append('no_positive_paired_lower_bound')
 families={}
 for family in sorted({r['family'] for r in candidate}):
  ca=[r for r in candidate if r['family']==family]
  old=[r for r in public['v10'] if r['family']==family]
  gain=paired(ca,old)
  families[family]=dict(candidate=desc(ca),v10=desc(old),v9=desc([r for r in public['v9'] if r['family']==family]),gain=gain)
  if not gain.get('complete') or gain['point_gain'] < -0.05:reasons.append('family_regression_'+family)
 direct={f:desc([r for r in rows if r['candidate']==name and r['panel']=='direct_reference' and r['family']==f]) for f in ('release_v9','release_v10')}
 for family,value in direct.items():
  if value['games']!=96 or value['points'] is None or value['points']<.65:reasons.append('direct_regression_'+family)
 if desc(candidate)['points']<0.80:reasons.append('absolute_public_strength_floor')
 for family,value in families.items():
  if value['candidate']['points']<0.50:reasons.append('absolute_family_strength_floor_'+family)
 return {'passed':not reasons,'reasons':reasons,'paired_gains':gains,
         'families':families,'direct':direct,'candidate_public':desc(candidate),
         'v9_public':desc(public['v9']),'v10_public':desc(public['v10'])}

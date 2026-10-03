"""Apply the Phase-B preregistered acceptance criteria without changing thresholds."""
from pathlib import Path
import hashlib,json,random,statistics,sys
B=Path(__file__).resolve().parent; D=B.parent; W=D.parent; R=W.parents[1]
sys.path.insert(0,str(D));from assess import load,desc,paired,point

def check():
 spec=json.loads((B/'selection.json').read_text());name=spec['candidate']
 design=json.loads((B/'validation_design.json').read_text())
 assert hashlib.sha256((B/'VALIDATION_PROTOCOL.md').read_bytes()).hexdigest()==design['protocol_sha256']
 jobs=json.loads((B/'validation_jobs.json').read_text()); rows=load(B/'validation_results.jsonl')
 assert len(jobs)==len(rows)==2352
 assert len({r['id'] for r in rows})==len(rows)
 byid={r['id']:r for r in rows};assert set(byid)=={j['id'] for j in jobs}
 for job in jobs:
  assert all(byid[job['id']].get(k)==v for k,v in job.items()),job['id']
 for path,digest in design['source_hashes'].items():
  assert hashlib.sha256((R/path).read_bytes()).hexdigest()==digest,path
 reasons=[]
 if not all(r.get('valid') for r in rows):reasons.append('invalid_games')
 def group(candidate,panel,family=None):
  return [r for r in rows if r['candidate']==candidate and r['panel']==panel and (family is None or r['family']==family)]
 original={v:f'submissions/release_{v}/main.py' for v in ('v9','v10')}
 candidate=group(name,'public_program');assert len(candidate)==576
 comparisons={v:paired(candidate,group(path,'public_program')) for v,path in original.items()}
 if not comparisons['v10'].get('complete') or comparisons['v10']['world_bootstrap_95'][0]<=0:
  reasons.append('no_positive_primary_gain')
 if desc(candidate)['points']<.80:reasons.append('primary_strength_floor')
 families={}
 for family in sorted({r['family'] for r in candidate}):
  ca=group(name,'public_program',family);old=group(original['v10'],'public_program',family)
  assert len(ca)==len(old)==96
  gain=paired(ca,old)
  families[family]=dict(candidate=desc(ca),v10=desc(old),v9=desc(group(original['v9'],'public_program',family)),gain=gain)
  if gain['point_gain']<-.05:reasons.append('family_regression_'+family)
  if desc(ca)['points']<.50:reasons.append('family_strength_floor_'+family)
 direct={}
 for version in ('release_v9','release_v10'):
  ca=group(name,'direct_reference',version);assert len(ca)==96
  direct[version]=desc(ca)
  if direct[version]['points']<.65:reasons.append('direct_reference_'+version)
 styles={}
 for family in sorted({r['family'] for r in group(name,'style_stress')}):
  ca=group(name,'style_stress',family);old=group(original['v10'],'style_stress',family)
  assert len(ca)==len(old)==24
  gain=paired(ca,old)
  styles[family]=dict(candidate=desc(ca),v10=desc(old),v9=desc(group(original['v9'],'style_stress',family)),gain=gain)
  if desc(ca)['points']<.50:reasons.append('style_strength_floor_'+family)
  if gain['point_gain']<-.10:reasons.append('style_regression_'+family)
 assert len(styles)==6
 old={(r['opponent_sha256'],r['seed'],r['seat']):r for r in group(original['v10'],'public_program')}
 worlds={}
 for row in candidate:
  worlds.setdefault(row['seed'],[]).append(point(row)-point(old[(row['opponent_sha256'],row['seed'],row['seat'])]))
 values=[statistics.mean(worlds[s]) for s in sorted(worlds)]
 rng=random.Random(20260926)
 boot=sorted(statistics.mean(rng.choices(values,k=len(values))) for _ in range(8000))
 report=dict(passed=not reasons,reasons=reasons,selection=spec,total_full_games=len(rows),
  invalid_games=sum(not r.get('valid') for r in rows),families=families,styles=styles,direct=direct,
  paired_primary=comparisons,primary_gain_interval_975=[boot[100],boot[7899]],
  primary={v:desc(group(path,'public_program')) for v,path in [('candidate',name),*original.items()]},
  style={v:desc(group(path,'style_stress')) for v,path in [('candidate',name),*original.items()]},
  observed_max_candidate_seconds=max(r['max_seconds'] for r in rows if r['candidate']==name),
  candidate_residual_inventory_cases=sum(bool(r.get('final_carried')) or any(r.get('final_inventory',{}).values()) for r in rows if r['candidate']==name),
  ledger_sha256=hashlib.sha256((B/'validation_results.jsonl').read_bytes()).hexdigest(),
  online_rating=None,online_submission=False)
 (B/'gate_result.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
 print(json.dumps({'passed':report['passed'],'reasons':reasons,'primary':report['primary'],
  'primary_gain':comparisons['v10'],'interval_975':report['primary_gain_interval_975'],
  'direct':direct,'style':report['style']}),flush=True)
 return report
if __name__=='__main__':check()

"""Read-only statistical audit of the frozen, prospective component test."""
from pathlib import Path
from collections import defaultdict
import hashlib,json,random,statistics
D=Path(__file__).resolve().parent;R=D.parents[1]
design=json.loads((D/'herd_confirmation_design.json').read_text())
manifest=json.loads((D/'herd_confirmation_jobs.json').read_text())
rows=[json.loads(line) for line in (D/'herd_confirmation_results.jsonl').read_text().splitlines() if line.strip()]
expected={job['id']:job for job in manifest}
assert len(rows)==len(expected)==len({row['id'] for row in rows}), 'Incomplete or duplicate results'
for row in rows:
    assert row['valid'] and all(row.get(k)==v for k,v in expected[row['id']].items())
    assert row['cash_identity_checked']
for variant in design['variants']:
    assert hashlib.sha256((R/variant['path']).read_bytes()).hexdigest()==variant['sha256']
def pairkey(row):return row['family'],row['seed'],row['seat']
basepath=next(v['path'] for v in design['variants'] if v['name']=='r2')
baseline={pairkey(row):row for row in rows if row['candidate']==basepath}
candidate=[row for row in rows if row['candidate']!=basepath]
assert len(candidate)==len(baseline)==512
pairs=[];worlds=defaultdict(list);inactive=[]
for row in candidate:
    old=baseline[pairkey(row)]
    diff=int(row['margin']>0)-int(old['margin']>0)
    worlds[row['seed']].append(diff)
    if row['macro']['_MP_REPORT'].get('eligible_turns')==0:
        inactive.append(row['action_hash']==old['action_hash'])
    current_score=1.0 if row['margin']>0 else 0.5 if row['margin']==0 else 0.0
    old_score=1.0 if old['margin']>0 else 0.5 if old['margin']==0 else 0.0
    worlds[row['seed']][-1]=current_score-old_score
    pairs.append(dict(family=row['family'],seed=row['seed'],seat=row['seat'],baseline_margin=old['margin'],candidate_margin=row['margin'],win_delta=diff,score_delta=current_score-old_score,margin_delta=row['margin']-old['margin'],same_shops=row['shops']==old['shops'],candidate_id=row['id'],baseline_id=old['id']))
values=[statistics.mean(worlds[seed]) for seed in design['seeds']]
rng=random.Random(20260928)
boot=sorted(statistics.mean(rng.choices(values,k=len(values))) for _ in range(10000))
def counts(data):
    return dict(games=len(data),wins=sum(r['margin']>0 for r in data),losses=sum(r['margin']<0 for r in data),ties=sum(r['margin']==0 for r in data))
report=dict(scope=design['scope'],complete=True,new_executions=len(rows),worlds=len(worlds),baseline=counts(list(baseline.values())),candidate=counts(candidate),net_wins=sum(p['win_delta'] for p in pairs),gained_wins=sum(p['win_delta']>0 for p in pairs),lost_wins=sum(p['win_delta']<0 for p in pairs),mean_margin_delta=statistics.mean(p['margin_delta'] for p in pairs),mean_score_delta=statistics.mean(values),world_bootstrap_95_score_delta=[boot[249],boot[9749]],same_shop_pairs=sum(p['same_shops'] for p in pairs),inactive_pairs=len(inactive),inactive_action_hash_mismatches=sum(not value for value in inactive),maximum_action_seconds=max(r['max_seconds'] for r in candidate),broken_plan_games=sum(r['macro']['_CS_REPORT'].get('cs_broken',0)>0 for r in candidate),source_hashes={v['name']:v['sha256'] for v in design['variants']})
report['by_family']={family:dict(baseline=counts([r for r in baseline.values() if r['family']==family]),candidate=counts([r for r in candidate if r['family']==family])) for family in sorted({r['family'] for r in rows})}
report['disagreeing_pairs']=[p for p in pairs if p['score_delta']!=0]
(D/'herd_confirmation_audit.json').write_text(json.dumps(report,indent=2))
(D/'herd_confirmation_pairs.json').write_text(json.dumps(pairs,indent=2))
print(json.dumps({k:v for k,v in report.items() if k!='disagreeing_pairs'}),flush=True)
selected=[row for row in candidate if str(row['macro']['_CS_REPORT'].get('cs_decision','')).startswith('SHEEP@')]
report['sheep_selected_games']=len(selected)
report['selected_without_harvest_credit']=[row['id'] for row in selected if row['macro']['_CS_REPORT'].get('cs_credit',0)==0]
report['unplaced_sheep_cases']=[dict(id=row['id'],seed=row['seed'],seat=row['seat'],family=row['family'],units=row['final_inventory'].get('SHEEP',0)) for row in candidate if row['final_inventory'].get('SHEEP',0)>baseline[pairkey(row)]['final_inventory'].get('SHEEP',0)]
(D/'herd_confirmation_audit.json').write_text(json.dumps(report,indent=2))
print(json.dumps({'sheep_selected_games':len(selected),'selected_without_harvest_credit':len(report['selected_without_harvest_credit']),'unplaced_sheep_cases':len(report['unplaced_sheep_cases'])}),flush=True)

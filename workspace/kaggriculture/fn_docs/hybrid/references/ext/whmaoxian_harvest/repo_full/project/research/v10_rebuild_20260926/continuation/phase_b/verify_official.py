"""Compare the separately collected real file-path games with frozen screening."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent; R=D.parents[3]
selection=json.loads((D/'selection.json').read_text())
assert hashlib.sha256((R/selection['candidate']).read_bytes()).hexdigest()==selection['sha256']
observed=json.loads((D/'official_cases.json').read_text())
assert observed['complete'] and len(observed['games'])==12
rows=[json.loads(x) for x in (D/'validation_results.jsonl').read_text().splitlines()]
assert len(rows)==2352 and all(r.get('valid') for r in rows)
key=lambda r:(r['candidate_sha256'],r['opponent_sha256'],r['seed'],r['seat'])
index={key(r):r for r in rows}; comparison=[]
for official in observed['games']:
 prior=index[key(official)]
 item=dict(family=official['family'],seed=official['seed'],seat=official['seat'],
  money=official['money'],money_matches=official['money']==prior['money'],
  action_hash_matches=official['action_hash']==prior['action_hash'],
  official_valid=official['valid'],max_candidate_seconds=official['max_candidate_seconds'])
 item['passed']=item['official_valid'] and item['money_matches'] and item['action_hash_matches']
 comparison.append(item)
result=dict(complete=len(comparison)==12,all_passed=all(r['passed'] for r in comparison),
 games=comparison,engine=observed['engine'],candidate_sha256=selection['sha256'])
(D/'official_crosscheck.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result),flush=True)
assert result['complete'] and result['all_passed'],'A real-run discrepancy remains; do not publish'

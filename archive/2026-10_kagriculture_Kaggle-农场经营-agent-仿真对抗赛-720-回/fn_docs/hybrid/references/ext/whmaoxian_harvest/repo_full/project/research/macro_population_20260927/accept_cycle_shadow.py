"""Require whole-game shadow identity before executing active variants."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent;base='submissions/release_v10_r2/main.py'
rows=[json.loads(s) for s in (D/'cycle_shadow_results.jsonl').read_text().splitlines()]
assert len(rows)==16 and all(r['valid'] for r in rows)
controls={(r['opponent'],r['seed'],r['seat']):r for r in rows if r['candidate']==base}
shadow=[r for r in rows if r['candidate']!=base]
assert len(shadow)==8
for row in shadow:
    before=controls[(row['opponent'],row['seed'],row['seat'])]
    assert row['action_hash']==before['action_hash'] and row['money']==before['money']
    assert row['economics']==before['economics']
    assert row['macro']['_MP_REPORT']['buy_cycles']==row['macro']['_MP_REPORT']['sell_cycles']==0
output=D/'cycle_screen_results.jsonl';prior=[json.loads(s) for s in output.read_text().splitlines()]
assert len(prior)==48
with output.open('a',encoding='utf-8') as handle:
    for row in shadow:handle.write(json.dumps(row)+'\n')
report=dict(passed=True,paired_cases=8,matching_shadow_actions=8*719,model_predictions=sum(r['macro']['_MP_REPORT']['predictions'] for r in shadow),added_cached_shadow_rows=8,scope='Whole-game identity check only; no strength claim.')
(D/'cycle_shadow_receipt.json').write_text(json.dumps(report,indent=2));print(json.dumps(report),flush=True)

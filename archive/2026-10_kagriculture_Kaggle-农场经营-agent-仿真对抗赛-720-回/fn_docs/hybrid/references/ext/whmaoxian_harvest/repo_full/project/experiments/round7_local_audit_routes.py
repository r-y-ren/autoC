"""Read-only audit of original study observations against generic stock guards."""
import gzip
import json
import runpy
from collections import Counter
from pathlib import Path

root = Path(__file__).resolve().parents[1]
rows = json.loads((root / 'research/round7/top2/index.json').read_text())
report = []
for row in rows:
    if row['split'] != 'study':
        continue
    name = ('vadim' if row['team'].startswith('Vadim') else 'dsm') + '_' + str(row['episode_id'])
    ns = runpy.run_path(str(root / 'experiments/round7_routes' / (name + '.py')))
    tape = ns['_DEMO_TAPE']
    game = json.loads(gzip.decompress((root / f"research/round7/top2/{row['episode_id']}.json.gz").read_bytes()))
    future = {'WHEAT':0, 'FERTILIZER':0}
    sell_suffix = []
    for action in reversed(tape):
        for order in action.get('market', []):
            if len(order) >= 3 and order[0] == 'SELL' and order[1] in future:
                future[order[1]] += int(order[2])
        sell_suffix.append(dict(future))
    sell_suffix.reverse()
    examples = []
    for step, states in enumerate(game['steps'][:-1]):
        obs = states[row['seat']]['observation']
        stock = obs['private']['shed']
        # This is a conservative static warning: ignore current field actions
        # and current sales, and require substantial spare stock.
        for item in future:
            remaining_sales = sell_suffix[step][item]
            if step < 696 and stock.get(item, 0) >= remaining_sales + 2:
                examples.append({'step':step,'item':item,'stock':stock[item], 'remaining_sales':remaining_sales})
    report.append({'name':name,'op_counts':dict(Counter(o[0] for a in tape for o in a.get('market',[]) if o)),
                   'input_sale_risks_on_original_observations':examples[:20], 'risk_count':len(examples)})
(root / 'results/round7-local-route-static-audit.json').write_text(json.dumps(report, indent=2))
for row in report:
    print(row['name'], 'risk_count', row['risk_count'], 'first', row['input_sale_risks_on_original_observations'][:2])

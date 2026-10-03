"""Paired, source-hashed Round 10 exact-SELL development screen audit."""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from compare_round8 import compare, read  # noqa: E402

baseline = read([ROOT / 'results/round10_v9_development.json'])
candidate = read([ROOT / 'results/round10_exact_sell_screen.json'])
keys = baseline.keys() & candidate.keys()
base = {key: baseline[key] for key in keys}
new = {key: candidate[key] for key in keys}
paired = compare(base, new, familywise_candidates=12)
paired['base_points'] = sum(row['points'] for row in base.values()) / len(base)
paired['new_points'] = sum(row['points'] for row in new.values()) / len(new)
paired['different_final_shops'] = sum(base[k]['shops'] != new[k]['shops'] for k in keys)
paired['shop_divergence_by_opponent'] = {
    opp: sum(base[k]['shops'] != new[k]['shops'] for k in keys
             if new[k]['opponent'] == opp)
    for opp in sorted({new[key]['opponent'] for key in keys})
}
paired['candidate_manifest'] = json.loads(
    (ROOT / 'results/round10_exact_sell_screen.manifest.json').read_text(encoding='utf-8')
)
paired['confirmation_used'] = False
output = ROOT / 'results/round10_exact_sell_screen_compare.json'
output.write_text(json.dumps(paired, indent=2), encoding='utf-8')
print(json.dumps({k: paired[k] for k in
                  ['paired_games', 'invalid_pairs', 'base_points',
                   'new_points', 'different_final_shops']}, indent=2))
for name, group in paired['opponents'].items():
    print(name, json.dumps(group))

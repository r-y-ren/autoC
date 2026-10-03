"""Paired screen audit; small screens are diagnostic, never a release gate."""
import json
from pathlib import Path

from compare_round8 import read, compare

root = Path(__file__).resolve().parent
baseline = read([root / 'results/round10_v9_development.json'])
variants = ['credit_flush', 'ongoing_flush', 'crop_flush', 'no_final_reorder']
report = {'screen_worlds': 8, 'confirmation_used': False, 'familywise_candidates': len(variants), 'variants': {}}
for name in variants:
    path = root / f'results/round10_{name}_screen.json'
    ledger = path.with_suffix('.jsonl')
    if not ledger.exists():
        continue
    candidate = read([path])
    keys = baseline.keys() & candidate.keys()
    base = {k: baseline[k] for k in keys}
    new = {k: candidate[k] for k in keys}
    row = compare(base, new, len(variants))
    row['base_points'] = sum(x['points'] for x in base.values()) / len(base) if base else None
    row['new_points'] = sum(x['points'] for x in new.values()) / len(new) if new else None
    row['final_shops_differ'] = sum(base[k]['shops'] != new[k]['shops'] for k in keys if 'shops' in new[k])
    report['variants'][name] = row
out = root / 'results/round10_screen_assessment.json'
out.write_text(json.dumps(report, indent=2), encoding='utf-8')
for name, row in report['variants'].items():
    print(name, row['paired_games'], 'invalid', row['invalid_pairs'],
          'V9', row['base_points'], 'new', row['new_points'],
          'point_gain', row['metrics']['points_change']['mean'],
          'margin_gain', row['metrics']['margin_change']['mean'],
          'shop_divergence', row['final_shops_differ'])

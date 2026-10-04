"""Evaluate frozen panels under the predeclared round-8 selection protocol.

This script never promotes a submission. Confirmation is an explicit mode;
development must finish before any confirmation fitness is read.
"""
import argparse
import hashlib
import json
import statistics
from pathlib import Path

from compare_round8 import compare, read
from league_round8 import freeze_seeds

ROOT = Path(__file__).resolve().parent
CONFIG = {
    'primary': {
        'source': 'experiments/round8_bounded_production.py',
        'sha256': '9fa83701138e80e3e5f9a6479cc2fa1c7e8a8965c4bd85d4e45d05ec5d4ffd4e',
        'development': 'round8_combined_development20',
        'confirmation': 'round8_candidate_confirmation',
        'stage': 'submissions/candidate_v8',
    },
    'dsm': {
        'source': 'experiments/round8_top2_dsm_contract_entry.py',
        'sha256': '23768116945ebd7500b2e2298616ff6dd974d27ce2c839643cc7d3e3d4cada57',
        'development': 'round8_dsm_contract_entry_development20',
        'confirmation': 'round8_dsm_contract_entry_confirmation',
        'stage': 'submissions/candidate_v8_dsm',
    },
}
V7_HASH = '273ca38d83d110166af4e2f2c6748892328488d5292f39fdbe4ef87b11350197'
OPPONENTS = {
    'submissions/release_v6/main.py': '10f58185b916392ca39697c83f67f455df81a74dfb6eb1aacd60fd81d50c9970',
    'submissions/release_v7/main.py': V7_HASH,
    'external/orderbook.py': 'a16e0e9b40c489972630a0b9d04f30e9c1cab03159fa78676db74277d84d82ab',
    'external/round8/master2965/main.py': '93831c18a43c49312a71fa67171224681c52c3fade0259403e8d8fae7973565f',
    'experiments/round8_top2_dsm_strict.py': '8340cedac73c4a54ca6f1a440385514ef2a9c4fd613c6c86cf14312fc19b9e3f',
    'external/round8/fieldcraft/main.py': '4aa771451850e68892fc1a847211f0bebffd511d6d3a508a7bb9969e5b881091',
}


def load(name):
    return read([ROOT / 'results' / (name + '.jsonl')])


def validate(rows, source_hash, worlds):
    split = 'development' if worlds == 20 else 'confirmation'
    assert worlds in (20, 40)
    seeds = freeze_seeds()[split]
    expected = {(seed, seat, opponent_hash) for seed in seeds for seat in (0, 1) for opponent_hash in OPPONENTS.values()}
    assert rows.keys() == expected, 'Panel does not match frozen worlds, seats and opponent hashes'
    assert len(rows) == worlds * 12, f'Incomplete panel: {len(rows)}/{worlds*12}'
    assert len({r['seed'] for r in rows.values()}) == worlds
    assert {r['candidate_sha256'] for r in rows.values()} == {source_hash}
    seed_cases = {}
    opponents = set()
    for r in rows.values():
        assert r['split'] == split and r['seat'] in (0, 1)
        assert OPPONENTS.get(r['opponent']) == r['opponent_sha256']
        assert r['valid'] and r['states'] == 720 and r['statuses'] == ['DONE', 'DONE']
        assert not r['stderr'] and not any(t['nonzero'] for t in r['telemetry'])
        seed_cases.setdefault(r['seed'], set()).add((r['seat'], r['opponent_sha256']))
        opponents.add(r['opponent_sha256'])
    assert len(opponents) == 6
    assert all(len(v) == 12 for v in seed_cases.values())


def totals(rows):
    values = list(rows.values())
    result = {
        'games': len(values), 'worlds': len({r['seed'] for r in values}),
        'wins': sum(r['delta'] > 0 for r in values),
        'losses': sum(r['delta'] < 0 for r in values),
        'ties': sum(r['delta'] == 0 for r in values),
        'points': statistics.mean(r['points'] for r in values),
    }
    result['opponents'] = {}
    for opp in sorted({r['opponent'] for r in values}):
        group = [r for r in values if r['opponent'] == opp]
        result['opponents'][opp] = {
            'games': len(group), 'wins': sum(r['delta'] > 0 for r in group),
            'losses': sum(r['delta'] < 0 for r in group),
            'ties': sum(r['delta'] == 0 for r in group),
            'points': statistics.mean(r['points'] for r in group),
            'mean_margin': statistics.mean(r['delta'] for r in group),
        }
    return result


def development():
    panels = {}
    for label, c in CONFIG.items():
        assert hashlib.sha256((ROOT / c['source']).read_bytes()).hexdigest() == c['sha256']
        panels[label] = load(c['development'])
        validate(panels[label], c['sha256'], 20)
    assert panels['primary'].keys() == panels['dsm'].keys()
    summary = {label: totals(rows) for label, rows in panels.items()}
    return {
        'phase': 'development', 'sources': CONFIG,
        'totals': summary,
        'dsm_advances': summary['dsm']['points'] >= summary['primary']['points'],
        'dsm_vs_primary': compare(panels['primary'], panels['dsm']),
        'warning': 'Development data participates in selection; no independent strength claim.',
    }


def confirmation(dev):
    labels = ['primary', 'dsm'] if dev['dsm_advances'] else ['primary']
    multiplicity = 3 if len(labels) == 2 else 1
    base = load('round8_v7_confirmation')
    validate(base, V7_HASH, 40)
    panels, technical, summaries, comparisons = {}, {}, {'v7': totals(base)}, {}
    for label in labels:
        c = CONFIG[label]
        panels[label] = load(c['confirmation'])
        validate(panels[label], c['sha256'], 40)
        assert panels[label].keys() == base.keys()
        summaries[label] = totals(panels[label])
        comparisons[label + '_vs_v7'] = compare(base, panels[label], multiplicity)
        stage = ROOT / c['stage']
        report = json.loads((stage / 'validation.json').read_text(encoding='utf-8'))
        assert report['source_sha256'] == c['sha256']
        assert hashlib.sha256((stage / 'main.py').read_bytes()).hexdigest() == c['sha256']
        assert hashlib.sha256((stage / 'submission.tar.gz').read_bytes()).hexdigest() == report['archive_sha256']
        technical[label] = bool(report['technical_acceptance_passed'])
    if len(labels) == 2:
        comparisons['dsm_vs_primary'] = compare(panels['primary'], panels['dsm'], multiplicity)
    eligible = [label for label in labels if technical[label] and comparisons[label + '_vs_v7']['metrics']['points_change']['world_bootstrap_familywise_95'][0] > 0]
    selected = max(eligible, key=lambda label: summaries[label]['points']) if eligible else None
    return {
        'phase': 'confirmation', 'sources': CONFIG, 'tested': labels,
        'familywise_comparisons': multiplicity, 'totals': summaries,
        'comparisons': comparisons, 'technical_pass': technical,
        'eligible': eligible, 'selected': selected,
        'online_submitted': False, 'online_rating': None,
        'warning': 'Local proxy opponents are not the original private leaderboard agents.',
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--phase', choices=['development', 'confirmation'], default='development')
    args = parser.parse_args()
    dev = development()
    result = dev if args.phase == 'development' else confirmation(dev)
    target = ROOT / 'results' / ('round8_selection_' + args.phase + '.json')
    target.write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps({k: v for k, v in result.items() if k in ('phase', 'dsm_advances', 'totals', 'eligible', 'selected', 'familywise_comparisons')}, indent=2))


if __name__ == '__main__':
    main()

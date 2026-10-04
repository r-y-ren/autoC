"""Round 10 official-engine league on prospectively frozen, disjoint seeds."""
import hashlib
import json
from pathlib import Path

import league_round9 as previous

ROOT = Path(__file__).resolve().parent


def freeze_seeds():
    path = ROOT / 'research/round10/league_seeds.json'
    expected = {
        split: [
            int.from_bytes(hashlib.sha256(f'kaggriculture-r10-{split}-{i}'.encode()).digest()[:4], 'big') % 2000000000
            for i in range(count)
        ]
        for split, count in [('development', 24), ('confirmation', 48), ('reserve', 48)]
    }
    prior = json.loads((ROOT / 'research/round9/league_seeds.json').read_text(encoding='utf-8'))
    old = {seed for values in prior.values() for seed in values}
    new = [seed for values in expected.values() for seed in values]
    assert len(new) == len(set(new)) and not old.intersection(new)
    if path.exists():
        assert json.loads(path.read_text(encoding='utf-8')) == expected
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(expected, indent=2), encoding='utf-8')
    return expected


previous.freeze_seeds = freeze_seeds

if __name__ == '__main__':
    previous.main()

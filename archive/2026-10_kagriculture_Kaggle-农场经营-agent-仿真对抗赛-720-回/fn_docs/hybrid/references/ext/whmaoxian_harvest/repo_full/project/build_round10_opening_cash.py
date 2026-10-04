"""Build isolated opening-cash ablation from frozen V9 bytes."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
BASE = ROOT / 'experiments/round9_market_slack.py'
SUFFIX = ROOT / 'experiments/round10_opening_cash_suffix.txt'
OUTPUT = ROOT / 'experiments/round10_opening_cash.py'
MANIFEST = ROOT / 'research/round10/opening_cash_build.json'
EXPECTED_V9 = '6b13532fbc2b55b59c6cae8ed8d5cd29fe82d18a7d7e044ed130217e3d1c09d3'


def main():
    source = BASE.read_bytes()
    assert hashlib.sha256(source).hexdigest() == EXPECTED_V9, 'Frozen V9 changed'
    text = source.decode('utf-8') + SUFFIX.read_text(encoding='utf-8')
    compile(text, str(OUTPUT), 'exec')
    payload = text.encode('utf-8')
    if OUTPUT.exists():
        assert OUTPUT.read_bytes() == payload, 'Candidate differs; use a new version name'
    else:
        OUTPUT.write_bytes(payload)
    record = {
        'parent': str(BASE.relative_to(ROOT)).replace('\\', '/'),
        'parent_sha256': EXPECTED_V9,
        'candidate': str(OUTPUT.relative_to(ROOT)).replace('\\', '/'),
        'candidate_sha256': hashlib.sha256(payload).hexdigest(),
        'candidate_bytes': len(payload),
        'suffix_sha256': hashlib.sha256(SUFFIX.read_bytes()).hexdigest(),
        'entry': 'round10_opening_cash_agent',
    }
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    if MANIFEST.exists():
        assert json.loads(MANIFEST.read_text(encoding='utf-8')) == record
    else:
        MANIFEST.write_text(json.dumps(record, indent=2), encoding='utf-8')
    print(json.dumps(record, indent=2))


if __name__ == '__main__':
    main()

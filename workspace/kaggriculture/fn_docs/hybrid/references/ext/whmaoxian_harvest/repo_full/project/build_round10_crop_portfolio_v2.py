"""Build one immutable round-10 day-11 crop portfolio candidate from frozen V9."""

from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parent
BASE = ROOT / 'submissions/release_v9/main.py'
SUFFIX = ROOT / 'experiments/round10_crop_portfolio_v2_suffix.txt'
OUTPUT = ROOT / 'experiments/round10_crop_portfolio_v2.py'
MANIFEST = ROOT / 'research/round10/crop_portfolio_v2_build.json'
EXPECTED_V9 = '6b13532fbc2b55b59c6cae8ed8d5cd29fe82d18a7d7e044ed130217e3d1c09d3'


def main():
    source = BASE.read_bytes()
    assert hashlib.sha256(source).hexdigest() == EXPECTED_V9, 'Frozen V9 changed'
    suffix = SUFFIX.read_bytes()
    payload = source + suffix
    compile(payload, str(OUTPUT), 'exec')
    if OUTPUT.exists():
        assert OUTPUT.read_bytes() == payload, 'Candidate bytes differ; choose a new name'
    else:
        OUTPUT.write_bytes(payload)
    record = {
        'parent': str(BASE.relative_to(ROOT)).replace('\\', '/'),
        'parent_sha256': EXPECTED_V9,
        'suffix': str(SUFFIX.relative_to(ROOT)).replace('\\', '/'),
        'suffix_sha256': hashlib.sha256(suffix).hexdigest(),
        'candidate': str(OUTPUT.relative_to(ROOT)).replace('\\', '/'),
        'candidate_sha256': hashlib.sha256(payload).hexdigest(),
        'candidate_bytes': len(payload),
        'entry': 'round10_crop_portfolio_agent',
    }
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    if MANIFEST.exists():
        assert json.loads(MANIFEST.read_text(encoding='utf-8')) == record
    else:
        MANIFEST.write_text(json.dumps(record, indent=2), encoding='utf-8')
    print(json.dumps(record, indent=2))


if __name__ == '__main__':
    main()

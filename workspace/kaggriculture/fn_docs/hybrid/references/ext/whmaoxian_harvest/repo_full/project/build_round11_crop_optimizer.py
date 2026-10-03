"""Rebuild the isolated R11 melon-versus-strawberry candidate from frozen V9."""

from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parent
BASE = ROOT / 'submissions/release_v9/main.py'
SUFFIX = ROOT / 'experiments/round11_crop_optimizer_suffix.txt'
TARGET = ROOT / 'experiments/round11_crop_optimizer.py'
MANIFEST = ROOT / 'research/round11_crop_optimizer_build.json'
EXPECTED_V9 = '6b13532fbc2b55b59c6cae8ed8d5cd29fe82d18a7d7e044ed130217e3d1c09d3'


def main():
    base = BASE.read_bytes()
    assert hashlib.sha256(base).hexdigest() == EXPECTED_V9, 'Frozen V9 changed'
    suffix = SUFFIX.read_bytes()
    payload = base + suffix
    compile(payload, str(TARGET), 'exec')
    if TARGET.exists():
        assert TARGET.read_bytes() == payload, 'Candidate differs; choose a new name'
    else:
        TARGET.write_bytes(payload)
    record = {
        'base': str(BASE.relative_to(ROOT)).replace('\\','/'),
        'base_sha256': EXPECTED_V9,
        'suffix': str(SUFFIX.relative_to(ROOT)).replace('\\','/'),
        'suffix_sha256': hashlib.sha256(suffix).hexdigest(),
        'candidate': str(TARGET.relative_to(ROOT)).replace('\\','/'),
        'candidate_sha256': hashlib.sha256(payload).hexdigest(),
        'entry': 'round11_crop_optimizer_agent',
    }
    if MANIFEST.exists():
        assert json.loads(MANIFEST.read_text(encoding='utf-8')) == record
    else:
        MANIFEST.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(record, indent=2))


if __name__ == '__main__':
    main()

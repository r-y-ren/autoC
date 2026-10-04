"""Create an isolated exact SELL-block experiment without changing frozen V9."""
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent
base_path = ROOT / 'submissions/release_v9/main.py'
expected_v9_sha256 = '6b13532fbc2b55b59c6cae8ed8d5cd29fe82d18a7d7e044ed130217e3d1c09d3'
assert hashlib.sha256(base_path.read_bytes()).hexdigest() == expected_v9_sha256
base = base_path.read_text(encoding='utf-8')
suffix = (ROOT / 'experiments/round10_exact_sell_suffix.py').read_text(encoding='utf-8')
target = ROOT / 'experiments/round10_exact_sell.py'
candidate = base + '\n\n' + suffix
if target.exists():
    assert target.read_text(encoding='utf-8') == candidate, 'Frozen candidate differs; use a new filename'
else:
    target.write_text(candidate, encoding='utf-8')
print(target, hashlib.sha256(target.read_bytes()).hexdigest())

"""Freeze three independent physical-labor hypotheses from the V9 baseline."""
import hashlib
from pathlib import Path

root = Path(__file__).resolve().parent
v9_path = root / 'submissions/release_v9/main.py'
assert hashlib.sha256(v9_path.read_bytes()).hexdigest() == '6b13532fbc2b55b59c6cae8ed8d5cd29fe82d18a7d7e044ed130217e3d1c09d3'
v9 = v9_path.read_text(encoding='utf-8')
crop = (root / 'experiments/round10_crop_slack.py').read_text(encoding='utf-8')
suffix = (root / 'experiments/round10_credit_flush_suffix.txt').read_text(encoding='utf-8')

variants = {
    'round10_credit_flush.py': v9 + suffix,
    'round10_crop_flush.py': crop + suffix,
    'round10_ongoing_flush.py': crop.replace(
        "crop not in ('WHEAT','CARROT','TOMATO','STRAWBERRY','MELON')",
        "crop not in ('TOMATO','STRAWBERRY')") + suffix,
}
assert variants['round10_ongoing_flush.py'] != variants['round10_crop_flush.py']
for name, content in variants.items():
    target = root / 'experiments' / name
    if target.exists(): assert target.read_text(encoding='utf-8') == content
    else: target.write_text(content, encoding='utf-8')
    print(target.relative_to(root), hashlib.sha256(target.read_bytes()).hexdigest())

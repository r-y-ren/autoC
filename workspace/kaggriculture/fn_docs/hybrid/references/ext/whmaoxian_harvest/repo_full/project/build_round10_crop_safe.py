"""Protect future native crop maintenance before opportunistic harvest."""
import hashlib
from pathlib import Path

root = Path(__file__).resolve().parent
source = (root / 'experiments/round10_crop_flush.py').read_text(encoding='utf-8')
target = root / 'experiments/round10_crop_safe_flush.py'
old = "if c[0] in ('CARE','HARVEST','COLLECT_FERTILIZER'):reserved.add((tuple(positions[i]),c[0]))"
assert source.count(old) == 1
source = source.replace(old, "if c[0] in ('CARE','HARVEST','COLLECT_FERTILIZER','WATER','FERTILIZE'):reserved.add((tuple(positions[i]),c[0]))")
old = "if i<len(positions) and c and c[0] in ('CARE','HARVEST','COLLECT_FERTILIZER'):reserved.add((tuple(positions[i]),c[0]))"
assert source.count(old) == 1
source = source.replace(old, "if i<len(positions) and c and c[0] in ('CARE','HARVEST','COLLECT_FERTILIZER','WATER','FERTILIZE'):reserved.add((tuple(positions[i]),c[0]))")
old = "if (site,'HARVEST') in reserved or site in targets:continue"
assert source.count(old) == 1
source = source.replace(old, "if site in targets or any((site,op) in reserved for op in ('HARVEST','WATER','FERTILIZE')):continue")
if target.exists(): assert target.read_text(encoding='utf-8') == source
else: target.write_text(source, encoding='utf-8')
print(target.relative_to(root), hashlib.sha256(target.read_bytes()).hexdigest())

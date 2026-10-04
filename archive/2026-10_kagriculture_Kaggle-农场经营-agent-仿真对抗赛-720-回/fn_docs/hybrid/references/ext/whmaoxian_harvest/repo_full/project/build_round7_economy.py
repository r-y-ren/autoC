"""Evidence-based wheat conservation experiment from recent online close losses."""
from pathlib import Path

root = Path(__file__).parent
source = (root / 'submissions/release_v6/main.py').read_text(encoding='utf-8')
old = "action = _alt_sell_extra(action,'WHEAT',amount)"
assert source.count(old) == 1
source = source.replace(old, "# Modified 2026-09-22: retain this opening wheat for feeding instead of selling and rebuying.\n            pass")
(root / 'experiments/round7_keep_wheat.py').write_text(source, encoding='utf-8')
print('Built wheat retention candidate')

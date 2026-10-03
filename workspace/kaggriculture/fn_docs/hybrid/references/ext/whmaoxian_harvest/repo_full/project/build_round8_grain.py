"""Ablate the opening sale/rebuy cycle on v7 without changing its final layers."""
import hashlib
import json
from pathlib import Path

root=Path(__file__).resolve().parent
source=(root/'submissions/release_v7/main.py').read_text(encoding='utf-8')
old="action = _alt_sell_extra(action,'WHEAT',amount)"
assert source.count(old)==1
source=source.replace(old,"# Local round8 ablation: retain the three opening wheat for feed.\n            pass",1)
p=root/'experiments/round8_grain.py'
p.write_text(source,encoding='utf-8',newline='\n')
print(json.dumps({'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}))

"""Separate ADV timing gains from unconditional order-frontloading."""
import hashlib
import json
from pathlib import Path

root=Path(__file__).resolve().parent
p=root/'experiments/round8_fullfusion.py'
assert hashlib.sha256(p.read_bytes()).hexdigest().startswith('8fd54efa')
target=root/'experiments/round8_no_front.py'
target.write_bytes(p.read_bytes()+b'\n# Local round8 ablation: retain parent order policy; advance sales still enabled.\n_ADV_FRONT=False\n')
print(json.dumps({'path':str(target),'sha256':hashlib.sha256(target.read_bytes()).hexdigest()}))

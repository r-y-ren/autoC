"""Build exact v7 plus a separately auditable round8 market suffix."""
from pathlib import Path
import hashlib
root=Path(__file__).resolve().parents[1]
base=(root/'submissions/release_v7/main.py').read_bytes()
assert hashlib.sha256(base).hexdigest()=='273ca38d83d110166af4e2f2c6748892328488d5292f39fdbe4ef87b11350197'
suffix=(root/'experiments/round8_market_recurrence_suffix.txt').read_text(encoding='utf-8-sig')
source=base+b'\n'+suffix.encode()
compile(source,'round8_market_recurrence','exec')
out=root/'experiments/round8_market_recurrence.py'
out.write_bytes(source)
print(out,hashlib.sha256(source).hexdigest())

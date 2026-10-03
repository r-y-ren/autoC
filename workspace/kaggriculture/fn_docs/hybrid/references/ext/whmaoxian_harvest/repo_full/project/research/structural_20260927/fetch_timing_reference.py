"""Fetch an additional public notebook; keep its code inert for review."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,requests
P=Path(__file__).resolve().parent;out=P/'public_notebooks'
slug='tetsutani/demand-preserving-turn-sale-timing'
url='https://www.kaggle.com/api/v1/kernels/pull/'+slug
response=requests.get(url,timeout=45);response.raise_for_status()
raw=response.content;assert len(raw)<30000000
obj=json.loads(raw);path=out/'tetsutani__demand-preserving-turn-sale-timing.json'
if path.exists():assert path.read_bytes()==raw
else:path.write_bytes(raw)
record=dict(slug=slug,url=url,captured_utc=datetime.now(timezone.utc).isoformat(),path=str(path),sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw))
(out/'timing_receipt.json').write_text(json.dumps(record,indent=2))
print(json.dumps(record),flush=True)

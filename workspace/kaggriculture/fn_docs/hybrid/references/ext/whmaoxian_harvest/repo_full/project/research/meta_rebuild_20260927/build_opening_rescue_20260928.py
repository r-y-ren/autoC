"""Test a one-day fertilizer-to-feed rescue, without claiming stronger play."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1];sha=lambda b:hashlib.sha256(b).hexdigest()
meta=next(v for v in json.loads((D/'opening_species_design.json').read_text())['variants'] if v['name']=='SHEEP')
base=(R/meta['path']).read_bytes();assert sha(base)==meta['sha256']
assert b'_OF29_' not in base
source=base+(D/'opening_feed_rescue_20260928.txt').read_bytes()
path=D/'candidates/opening_sheep_feed_rescue.py';compile(source,str(path),'exec')
if path.exists():assert path.read_bytes()==source
else:path.write_bytes(source)
print(json.dumps({'path':path.relative_to(R).as_posix(),'sha256':sha(source)}),flush=True)

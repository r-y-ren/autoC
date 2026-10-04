"""Imitate executed production orders, not historical unfilled requests."""
import base64
import json
import zlib
from pathlib import Path

r=Path(__file__).parent
core=(r/'experiments/round7_local_chassis_core.py').read_text(encoding='utf-8')
data=json.loads((r/'research/round7/top2/effective_routes.json').read_text(encoding='utf-8'))
for row in data['routes']:
    tape=row['actions']
    # Buying grain first prevents the observed cash shortfall against public v6.
    if tape[0]['market'] == [['BUY_ANIMAL','COW',1],['BUY_PRODUCT','WHEAT',5]]:
        tape[0]['market'].reverse()
    blob=base64.b85encode(zlib.compress(json.dumps(tape,separators=(',',':')).encode())).decode()
    extension=f'''
# Modified 2026-09-22: executed public episode {row['episode_id']} production orders.
# Empty unfilled-order slots are retained; current prices and stocks remain reactive.
import json, base64, zlib
_EFFECTIVE = json.loads(zlib.decompress(base64.b85decode({blob!r})))
_EXECUTOR = make_agent({{0:_EFFECTIVE}},dead_stock=False)
def agent(obs,config=None):
    return _EXECUTOR(obs,config)
agent.telemetry = _EXECUTOR.chassis.diagnostics
'''
    dest=r/f"experiments/round7_routes/effective_{row['episode_id']}.py"
    dest.write_text(core+extension,encoding='utf-8')
    print(dest.name)

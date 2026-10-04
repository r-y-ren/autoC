"""Study-only route imitation using public action records and a reactive chassis."""
import ast
import base64
import gzip
import json
import zlib
from pathlib import Path

ROOT = Path(__file__).parent
source = (ROOT / 'submissions/release_v6/main.py').read_text(encoding='utf-8')
node = next(n for n in ast.parse(source).body if isinstance(n, ast.FunctionDef) and n.name == 'make_agent')
chassis = '\n'.join(source.splitlines()[:node.end_lineno]) + '\n'
index = json.loads((ROOT / 'research/round7/top2/index.json').read_text())
out = ROOT / 'experiments/round7_routes'
out.mkdir(exist_ok=True)
for row in index:
    if row['split'] != 'study':
        continue
    game = json.loads(gzip.decompress((ROOT / f"research/round7/top2/{row['episode_id']}.json.gz").read_bytes()))
    tape = [s[row['seat']]['action'] for s in game['steps'][1:]]
    blob = base64.b85encode(zlib.compress(json.dumps(tape,separators=(',',':')).encode())).decode()
    # Version candidate paths so older reports remain tied to immutable source.
    name = ('vadim' if row['team'].startswith('Vadim') else 'dsm') + '_' + str(row['episode_id']) + '_v2'
    extension = f'''
# Modified 2026-09-22: public {row['team']} episode {row['episode_id']} action data.
# This is an imitation experiment, not the author's private decision algorithm.
import base64, zlib, json
_DEMO_TAPE = json.loads(zlib.decompress(base64.b85decode({blob!r})))
# The generic dead-stock heuristic considers future SALES only. It does not
# preserve wheat/fertilizer required by PICKUP/FEED/FERTILIZE, so it must be
# disabled for a new production route whose input contracts are not modeled.
_DEMO_IMPL = make_agent({{0: _DEMO_TAPE}}, dead_stock=False)
def agent(obs, config=None):
    return _DEMO_IMPL(obs, config)
agent.telemetry = _DEMO_IMPL.chassis.diagnostics
'''
    (out / (name + '.py')).write_text(chassis + extension, encoding='utf-8')
    print(name, len(tape))

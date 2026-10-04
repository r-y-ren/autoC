"""Append V56's two input-economy mechanisms to the frozen Orderbook agent."""
import ast
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EXPECTED = {
    'orderbook': 'a16e0e9b40c489972630a0b9d04f30e9c1cab03159fa78676db74277d84d82ab',
    'ahmed_v56': 'a1ad0fd1d174477ee2cbdd561a812bcb7029647ce34599e79d6b79e9057eff6c',
}
raw = {name:(ROOT / f'external/{name}.py').read_bytes() for name in EXPECTED}
for name, data in raw.items():
    assert hashlib.sha256(data).hexdigest() == EXPECTED[name]
sources = {name:data.decode('utf-8') for name,data in raw.items()}
trees = {name:ast.parse(source) for name,source in sources.items()}
definitions = {name:{n.name:ast.dump(n,include_attributes=False) for n in tree.body if isinstance(n,ast.FunctionDef)} for name,tree in trees.items()}
for function in ('_ca_visits', '_ca_yield_path', '_v219_native_day'):
    assert definitions['orderbook'][function] == definitions['ahmed_v56'][function], function
embedded = {name:[ast.literal_eval(n.args[0]) for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='exec'] for name,tree in trees.items()}
assert embedded['orderbook'] == embedded['ahmed_v56'], 'Physical planner interfaces changed'

tail = sources['ahmed_v56'].split('# EXP402: cap late seed purchases',1)[1]
tail = '# EXP402: cap late seed purchases' + tail
assert tail.count('_E402_PARENT=final_price_guard') == 1
tail = tail.replace('_E402_PARENT=final_price_guard', '_E402_PARENT=_cxd_agent', 1)
notice = '''

# Local integration modification, 2026-09-22, Apache-2.0.
# Base is shiiin9's public Orderbook strategy, retained byte-for-byte above,
# including its V55 ancestry, tomato gate, ordering layer and four constants.
# Append only Ahmed Berat Ozer's V56 EXP402 remaining-planting seed budget
# and EXP410 harvest-aware fertilizer cap. Their helper/physical interfaces
# were checked for AST/source equality against the Orderbook base.
# The only upstream tail edit rebinds EXP402's parent to _cxd_agent so the
# existing Orderbook pipeline remains active. No further constants are tuned.
# This is an independently testable integration, not a claimed new online score.
'''
entry = '''

_R7_FUSED_REPORT = {}
def round7_orderbook_v56_agent(observation, configuration=None):
    result = e410_agent(observation, configuration)
    if int(observation.get('step', 0)) == 0:
        _R7_FUSED_REPORT.clear()
    _R7_FUSED_REPORT.update({'seed_' + k:v for k,v in _E402_REPORT.items()})
    _R7_FUSED_REPORT.update({'fertilizer_' + k:v for k,v in _E410_REPORT.items()})
    _R7_FUSED_REPORT.update(_CXD_REPORT)
    _R7_FUSED_REPORT.update({k:v for k,v in _CXTB_REPORT.items() if k != 'cxtb_features'})
    return result

round7_orderbook_v56_agent.telemetry = _R7_FUSED_REPORT
agent = round7_orderbook_v56_agent
'''
data = raw['orderbook'] + (notice + tail + entry).encode('utf-8')
path = ROOT / 'experiments/round7_orderbook_v56.py'
compile(data.decode('utf-8'), str(path), 'exec')
path.write_bytes(data)
manifest = {'candidate':str(path.relative_to(ROOT)),'sha256':hashlib.sha256(data).hexdigest(),
            'bytes':len(data),'sources':EXPECTED,'parent_rebinding':'_E402_PARENT=_cxd_agent',
            'mechanisms':['EXP402 remaining-planting seed budget','EXP410 harvest-aware fertilizer cap'],
            'validation':'Static build and interface checks only; no performance claim.'}
(ROOT / 'research/round7/orderbook_v56_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print(json.dumps(manifest,indent=2))

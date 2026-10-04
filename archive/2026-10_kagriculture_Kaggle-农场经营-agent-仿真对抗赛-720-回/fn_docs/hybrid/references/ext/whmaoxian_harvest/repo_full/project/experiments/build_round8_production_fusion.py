"""Attach the frozen production overlay to an audited fullfusion entry.

Example: python experiments/build_round8_production_fusion.py --base
experiments/round8_fullfusion.py --output experiments/round8_fullfusion_production.py
This performs source/interface checks and initialization, never a game.
"""
import argparse
import ast
import hashlib
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser()
parser.add_argument('--base',required=True)
parser.add_argument('--output',required=True)
args=parser.parse_args()
frozen=ROOT/'experiments/round8_production_delivery.py'
assert hashlib.sha256(frozen.read_bytes()).hexdigest()=='05d9d50dd489f78a0561c717e483adef022d0fef1c52af604aed43e85508c02b'
reference=(ROOT/'submissions/release_v7/main.py').read_text(encoding='utf-8')
base_path=ROOT/args.base;output=ROOT/args.output
base=base_path.read_text(encoding='utf-8')
def definitions(source):
    return {n.name:ast.dump(n,include_attributes=False) for n in ast.parse(source).body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
a,b=definitions(reference),definitions(base)
interfaces=('_v219_request','_v219_worker','_v219_qualifies','_v219_native_day','_v219_fib','_v219_walk','_v219_home','_ca_spawn','FarmView','projected_shed','_r37_market_price')
assert all(a[n]==b[n] for n in interfaces),'Physical/investment interface differs; do not apply blindly'
marker='# Local production repair, 2026-09-22;'
frozen_text=frozen.read_text(encoding='utf-8')
assert frozen_text.count(marker)==1
suffix=frozen_text[frozen_text.index(marker):]
assert suffix.count('_T19_PARENT = round7_orderbook_v56_agent')==1
suffix=suffix.replace('_T19_PARENT = round7_orderbook_v56_agent',
    '_T19_PARENT = [v for v in list(globals().values()) if callable(v)][-1]')
footer='''
# Aggregate the complete market stack and production diagnostics. No action is
# modified here; all R148 / ADV / IG final-order safeguards remain active.
_P8_FUSION_REPORT = {}
def round8_production_fusion_agent(observation, configuration=None):
    result = round8_production_agent(observation, configuration)
    _P8_FUSION_REPORT.clear()
    _P8_FUSION_REPORT.update(getattr(_T19_PARENT, 'telemetry', {}))
    _P8_FUSION_REPORT.update({'production.'+k:v for k,v in _T19_REPORT.items()})
    return result
round8_production_fusion_agent.telemetry = _P8_FUSION_REPORT
agent = round8_production_fusion_agent
kaggle_submission_agent = round8_production_fusion_agent
'''
source=base+'\n\n'+suffix+'\n'+footer
ns={};exec(compile(source,str(output),'exec'),ns)
entry=[v for v in ns.values() if callable(v)][-1]
assert entry.__name__=='round8_production_fusion_agent'
expected='round8_fullfusion_bounded_agent' if 'bounded' in base_path.stem else 'round8_fullfusion_agent'
assert ns['_T19_PARENT'].__name__==expected,(expected,ns['_T19_PARENT'].__name__)
assert ns['_CXTB_MIN_REVENUE']==9000 and ns['_R148_OVERFLOW'] and not ns['_R148_SEEDS']
assert all(n in ns for n in ('_R148_REPORT','_ADV_REPORT','_IG_REPORT','_RACE_STATE'))
output.write_text(source,encoding='utf-8')
record={'base':str(base_path.relative_to(ROOT)),'base_sha256':hashlib.sha256(base_path.read_bytes()).hexdigest(),
        'production_source_sha256':hashlib.sha256(frozen.read_bytes()).hexdigest(),'interfaces_equal':list(interfaces),
        'captured_parent':ns['_T19_PARENT'].__name__,'final_entry':entry.__name__,
        'output':str(output.relative_to(ROOT)),'sha256':hashlib.sha256(output.read_bytes()).hexdigest(),
        'changes_to_frozen_suffix':['capture actual last callable','append diagnostics aggregator'],
        'validation_scope':'AST interface equality and initialization only; gameplay validation still required'}
output.with_suffix('.manifest.json').write_text(json.dumps(record,indent=2),encoding='utf-8')
print(json.dumps(record))

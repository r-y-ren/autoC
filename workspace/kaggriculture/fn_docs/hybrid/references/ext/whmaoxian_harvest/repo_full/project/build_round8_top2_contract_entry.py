"""Preserve the frozen contract policy; expose an unambiguous official entry."""
import hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).parent
SOURCE=ROOT/'experiments/round8_top2_dsm_contract.py'
DEST=ROOT/'experiments/round8_top2_dsm_contract_entry.py'
source_hash=hashlib.sha256(SOURCE.read_bytes()).hexdigest()
assert source_hash=='7735d6f4293495a0942a21fb92f6ff6aaec339dc759375e1ecdbe6226c6f2c53'
suffix='''

# Engineering-only entry repair, 2026-09-22. Kaggle get_last_callable selects
# the last inserted callable name. Redefining an old name does not move its
# dictionary insertion position; use a new final name instead.
def round8_dsm_contract_agent(observation, configuration=None):
    return agent(observation, configuration)
round8_dsm_contract_agent.telemetry=agent.telemetry
round8_dsm_contract_agent.routing_telemetry=agent.routing_telemetry
round8_dsm_contract_agent.contract_telemetry=agent.contract_telemetry
'''
generated=SOURCE.read_text(encoding='utf-8')+suffix
if '--check' in sys.argv:
    assert DEST.read_text(encoding='utf-8')==generated
    print('Entry source matches reproducible build: '+hashlib.sha256(DEST.read_bytes()).hexdigest())
    raise SystemExit(0)
DEST.write_text(generated,encoding='utf-8')
report={'source_path':str(SOURCE.relative_to(ROOT)),'source_sha256':source_hash,
        'candidate':str(DEST.relative_to(ROOT)),
        'candidate_sha256':hashlib.sha256(DEST.read_bytes()).hexdigest(),
        'entry_name':'round8_dsm_contract_agent',
        'policy_changes':[],
        'fix':'New final callable name so official get_last_callable selects the public two-argument entry',
        'old_source_preserved':True}
(ROOT/'research/round8/top2/contract_entry_build.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report),flush=True)

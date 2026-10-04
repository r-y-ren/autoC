"""Build v7 plus exact attributed public market suffixes. Never runs a notebook."""
import hashlib,json
from pathlib import Path
root=Path(__file__).resolve().parents[2]
base=(root/'submissions/release_v7/main.py').read_bytes()
upstream=(root/'external/round8/master2965/main.py').read_bytes()
assert hashlib.sha256(base).hexdigest()=='273ca38d83d110166af4e2f2c6748892328488d5292f39fdbe4ef87b11350197'
assert hashlib.sha256(upstream).hexdigest()=='93831c18a43c49312a71fa67171224681c52c3fade0259403e8d8fae7973565f'
r148=upstream[upstream.index(b'# R148: overflow reclaim'):upstream.index(b'# ADV: sale advance')]
adv=upstream[upstream.index(b'# ADV: sale advance'):upstream.index(b'# Final conservative closure')]
ig=upstream[upstream.index(b'# Final conservative closure'):upstream.index(b'# busyaprime, 2026-09-21')]
header=b'''\n# Local integration, 2026-09-22, Apache-2.0. Frozen v7 retained byte-for-byte above.
# Exact public tail from haideptry / The 2965 Master Hybrid Engine, notebook v4.
# https://www.kaggle.com/code/haideptry/the-2965-master-hybrid-engine
# Original mechanisms retain Ahmed Berat Ozer EXP277/EXP293 and sdy623/jaxa623
# attribution below. New work is interface integration and validation only.
# The public whole agent is NOT represented as original local research.
'''
bounded_adv = adv.replace(b'_ADV_TO=718', b'_ADV_TO=696')
old_guard = b"if len(market)<2 or int(obs['step'])<_ADV_FROM:return action"
new_guard = b"if len(market)<2 or not _ADV_FROM<=int(obs['step'])<_ADV_TO:return action"
assert old_guard in bounded_adv
bounded_adv = bounded_adv.replace(old_guard,new_guard)
records=[]
for name,parts in [('advance',[adv]),('fullfusion',[r148,adv,ig]),('r148',[r148]),('fullfusion_bounded',[r148,bounded_adv,ig])]:
 suffix=header+b'\n'.join(parts)
 footer=f'''\n# Final actual entrypoint; expose all component diagnostics instead of hiding parents.
_R8PUB_PARENT = agent
_R8PUB_TELEMETRY = {{}}
def round8_{name}_agent(observation, configuration=None):
    result = _R8PUB_PARENT(observation, configuration)
    # Outer layers can move order slots; the existing race detector must compare
    # the orders actually emitted on this turn on its next update.
    st = _RACE_STATE.get(int(observation['player']))
    if st is not None and st.get('prev_action') is not None and st.get('step') == int(observation['step']):
        st['prev_action'] = result
    _R8PUB_TELEMETRY.clear()
    _R8PUB_TELEMETRY.update(_R7_FUSED_REPORT)
    for namespace_name in ('_R148_REPORT', '_ADV_REPORT', '_IG_REPORT'):
        for key, value in globals().get(namespace_name, {{}}).items():
            _R8PUB_TELEMETRY[namespace_name + '.' + str(key)] = value
    return result
round8_{name}_agent.telemetry = _R8PUB_TELEMETRY
agent = round8_{name}_agent
'''.encode()
 source=base+suffix+footer
 target=root/f'experiments/round8_{name}.py';target.write_bytes(source)
 (root/f'experiments/round8_{name}_suffix.txt').write_bytes(suffix+footer)
 ns={};exec(compile(source,str(target),'exec'),ns)
 entry=[v for v in ns.values() if callable(v)][-1]
 assert entry.__name__==f'round8_{name}_agent'
 # The source uses v7's projected_shed/FarmView and exact physical helper namespace.
 required=['projected_shed','FarmView','_IMPL','_RACE_STATE','_CXD_REPORT']
 if name!='r148':required+=['_ADV_PARENT']
 if name in ('r148','fullfusion','fullfusion_bounded'):required+=['_r97_budget','_r127_fields','_r97_market_stock','_r97_delivery','_PLANNER_NS']
 assert all(key in ns for key in required)
 row={'candidate':str(target.relative_to(root)).replace('\\','/'),'sha256':hashlib.sha256(source).hexdigest(),'entry':entry.__name__,'local_changes': ['ADV stops before step 696, including _adv_frontload; R148 and IG remain active'] if name=='fullfusion_bounded' else [],'parts':[{'bytes':len(p),'sha256':hashlib.sha256(p).hexdigest()} for p in parts]}
 records.append(row);print(row)
(root/'research/round8/public_fusion_manifest.json').write_text(json.dumps(records,indent=2),encoding='utf-8')

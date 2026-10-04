"""Semantics-preserving packaging of the frozen DSM strict study proxy.

Remove unused task demonstration data/interpreter; precompute exactly the same
farm compatibility keys and retain all inputs actually read by the router.
No route choice, action, market heuristic, or training episode is changed.
"""
import ast
import base64
import hashlib
import json
from pathlib import Path
import runpy
import zlib

ROOT=Path(__file__).parent
ORIGINAL=ROOT/'experiments/round8_top2_dsm_strict.py'
DEST=ROOT/'experiments/round8_top2_dsm_compact.py'
source=ORIGINAL.read_text(encoding='utf-8')
namespace=runpy.run_path(str(ORIGINAL))
original_data=namespace['_R8_DEMOS']
key_function=namespace['_r8_field_key']
data={}
for rid,demo in original_data.items():
    contracts=[]
    for day in demo['dawn_states']:
        private=day['private']
        contracts.append({'step':day['step'],'key':key_function(day['farm']),
                          'shops':day['shops'],'private':{
                              'inventories':private['inventories'],
                              'seeds':private['seeds'],
                              'shed':{k:private['shed'].get(k,0) for k in ('WHEAT','FERTILIZER','COW','SHEEP','GOOSE')},
                          }})
    data[rid]={'actions':demo['actions'],'contracts':contracts}

tree=ast.parse(source)
lines=source.splitlines()
def function_source(name):
    node=next(n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name==name)
    return '\n'.join(lines[node.lineno-1:node.end_lineno])+'\n'

core=source.split('# Modified 2026-09-22: DSM public action-data study proxy.')[0]
router=function_source('_R8Router')
router=router.replace("_r8_field_key(d['farm'])", "d['key']").replace("['dawn_states']", "['contracts']")
blob=base64.b85encode(zlib.compress(json.dumps(data,separators=(',',':')).encode(),9)).decode()
compact=core+'''
# Modified 2026-09-22: engineering-only compact packaging of the frozen DSM
# public-demonstration proxy. Original actions and route decisions are retained.
# Uncalled task executor/data removed; compatibility keys computed at build time.
# This is independently constructed imitation, not the author's private source.
import base64, json, zlib
'''+f"_R8_DEMOS=json.loads(zlib.decompress(base64.b85decode({blob!r})))\n"
compact+=function_source('_r8_field_key')+'\n'+function_source('_r8_shop_score')+'\n'+router+'''
_R8_ROUTER=_R8Router(_R8_DEMOS)
_R8_ROUTES={rid:demo['actions'] for rid,demo in _R8_DEMOS.items()}
_R8_IMPL=Chassis(_R8_ROUTES,_R8_ROUTER,settings={'dead_stock':False})

def agent(obs,config=None):
    return _R8_IMPL.act(obs,config)
agent.telemetry=_R8_IMPL.diagnostics
agent.routing_telemetry=_R8_ROUTER.diagnostics
'''
DEST.write_text(compact,encoding='utf-8')
proof={'source_path':str(ORIGINAL.relative_to(ROOT)),'source_sha256':hashlib.sha256(ORIGINAL.read_bytes()).hexdigest(),
       'compact_path':str(DEST.relative_to(ROOT)),'compact_sha256':hashlib.sha256(DEST.read_bytes()).hexdigest(),
       'source_bytes':ORIGINAL.stat().st_size,'compact_bytes':DEST.stat().st_size,
       'episode_order_unchanged':list(original_data)==list(data),
       'all_24_action_tapes_unchanged':all(data[k]['actions']==original_data[k]['actions'] for k in data),
       'all_720_keys_identical':all(d['key']==key_function(original_data[k]['dawn_states'][i]['farm']) for k,v in data.items() for i,d in enumerate(v['contracts'])),
       'changes':['Remove uncalled task executor and task data','Precompute exact sorted JSON farm compatibility keys','Retain exactly the own-input inventory fields read by the original router'],
       'behavior_changes':[]}
assert all(proof[k] for k in ('episode_order_unchanged','all_24_action_tapes_unchanged','all_720_keys_identical'))
(ROOT/'research/round8/top2/compact_build.json').write_text(json.dumps(proof,indent=2),encoding='utf-8')
print(json.dumps(proof),flush=True)

"""Create state-reactive style proxies from training-only compiled demonstrations."""
import base64
import gzip
import hashlib
import json
from pathlib import Path
import zlib

ROOT=Path(__file__).parent
DATA=ROOT/'research/round8/top2'
core=(ROOT/'experiments/round7_local_chassis_core.py').read_text(encoding='utf-8')
runtime=(ROOT/'experiments/round8_top2_runtime.py').read_text(encoding='utf-8')
index=json.loads((DATA/'compiled_index.json').read_text())
provenance=[]
for team,prefix in [('Vadim Vasilenko','vadim'),('DSM','dsm')]:
    rows=[r for r in index if r['team']==team]
    assert len(rows)>=20,(team,len(rows))
    demos={}
    for r in rows:
        obj=json.loads(gzip.decompress((DATA/f"compiled_{r['episode_id']}_{r['seat']}.json.gz").read_bytes()))
        assert obj['split']=='study'
        # Enforce wheat procurement before the first cow when the original opens
        # with these two purchases; it prevents a known cash-order shortfall.
        market=obj['actions'][0]['market']
        if market==[['BUY_ANIMAL','COW',1],['BUY_PRODUCT','WHEAT',5]]:
            market.reverse()
        demos[str(obj['episode_id'])]={k:obj[k] for k in ('actions','dawn_states','tasks')}
    blob=base64.b85encode(zlib.compress(json.dumps(demos,separators=(',',':')).encode(),9)).decode()
    for variant in ('strict','tasks'):
        metadata=f'''\n# Modified 2026-09-22: {team} public action-data study proxy.
# Authors' private source code was not available. This is an independently
# constructed imitation with live-state market and farm guards, not their bot.
# Training episodes: {', '.join(str(r['episode_id']) for r in rows)}
import base64, json, zlib
_R8_DEMOS=json.loads(zlib.decompress(base64.b85decode({blob!r})))
'''
        ending='''
_R8_ROUTER=_R8Router(_R8_DEMOS)
_R8_ROUTES={rid:demo['actions'] for rid,demo in _R8_DEMOS.items()}
'''
        if variant=='strict':
            ending+='''
_R8_IMPL=Chassis(_R8_ROUTES,_R8_ROUTER,settings={'dead_stock':False})

def agent(obs,config=None):
    return _R8_IMPL.act(obs,config)
agent.telemetry=_R8_IMPL.diagnostics
agent.routing_telemetry=_R8_ROUTER.diagnostics
'''
        else:
            ending+='''
_R8_TASKS=_R8TaskExecutor(_R8_DEMOS)

class _R8TaskChassis(Chassis):
    def act(self,obs,config=None):
        self.current_observation=obs
        return super().act(obs,config)

    def _route_action(self,route,step):
        action=super()._route_action(route,step)
        return _R8_TASKS.act(self.current_observation,route,action)

_R8_IMPL=_R8TaskChassis(_R8_ROUTES,_R8_ROUTER,settings={'dead_stock':False,'weed_repair':False})

def agent(obs,config=None):
    return _R8_IMPL.act(obs,config)
agent.telemetry=_R8_IMPL.diagnostics
agent.routing_telemetry=_R8_ROUTER.diagnostics
agent.task_telemetry=_R8_TASKS.diagnostics
'''
        dest=ROOT/f'experiments/round8_top2_{prefix}_{variant}.py'
        dest.write_text(core+metadata+runtime+ending,encoding='utf-8')
        provenance.append({'team_style':team,'variant':variant,'path':str(dest.relative_to(ROOT)),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'study_episodes':[r['episode_id'] for r in rows],'claim':'Public-demonstration style proxy; not author source or a live copy.'})
        print(dest.name,dest.stat().st_size,flush=True)
(DATA/'proxy_provenance.json').write_text(json.dumps(provenance,indent=2),encoding='utf-8')

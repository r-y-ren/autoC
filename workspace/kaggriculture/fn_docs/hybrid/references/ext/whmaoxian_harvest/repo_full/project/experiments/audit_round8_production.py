"""Persistent replay equality plus bounded affordability request assertions."""
import contextlib
import copy
import gzip
import io
import json
import hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
with contextlib.redirect_stdout(io.StringIO()):
    from kaggle_environments.agent import get_last_callable
source=ROOT/'experiments/round8_production_delivery.py'
agent=get_last_callable(source.read_text(encoding='utf-8'),path=str(source))
g=json.loads(gzip.decompress((ROOT/'results/round8_production_delivery_function-seed688041503.json.gz').read_bytes()))
differences=[];snapshot=None
for t in range(719):
    obs=copy.deepcopy(g['steps'][t][0]['observation']);obs['step']=t
    action=agent(obs,g['configuration'])
    if action!=g['steps'][t+1][0]['action']:differences.append(t)
    if t==602:
        ns=agent.__globals__
        snapshot=(copy.deepcopy(ns['_V219_STATES'][0]),copy.deepcopy(ns['_IMPL'].chassis.players[0]))
ns=agent.__globals__
nonzero_errors={name:{k:v for k,v in value.items() if isinstance(v,(int,float)) and v>0 and ('error' in k.lower() or 'shortfall' in k.lower())}
                for name,value in ns.items() if isinstance(value,dict) and name.endswith('REPORT')}
nonzero_errors={k:v for k,v in nonzero_errors.items() if v}
report={'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'matching_persistent_actions':719-len(differences),
        'different_steps':differences,'normal_telemetry':dict(agent.telemetry),'nonzero_error_counters':nonzero_errors,
        'synthetic_request_checks':[]}
for money in (800,1200,2400):
    obs=copy.deepcopy(g['steps'][603][0]['observation']);obs['step']=603;obs['farms'][0]['money']=money
    action=copy.deepcopy(g['steps'][604][0]['action'])
    # Remove only the five orders added by the tested production layer.
    assert action['market'][-5:]==[['BUY_PRODUCT','FERTILIZER',19]]+[['HIRE']]*4
    action['market']=action['market'][:-5]
    state,native=copy.deepcopy(snapshot)
    proposed=ns['_v219_request'](obs,action,state,native)
    pending=state.get('t19_pending')
    assert pending and pending['count']>=1,(money,proposed)
    assert len(proposed['market'])<=10
    groups=pending['groups'];flat=[tuple(p) for group in groups for p in group]
    assert len(flat)==len(set(flat))==19
    report['synthetic_request_checks'].append({'kind':'modified_cash_observation_not_game_result','money':money,
        'maintenance_workers':pending['count'],'fertilizer_purchase':pending['fertilize'],
        'all_19_targets_retained_once':True,'market_orders':len(proposed['market'])})
assert not differences,differences
assert not nonzero_errors,nonzero_errors
(ROOT/'research/round8/production_final_audit.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report))

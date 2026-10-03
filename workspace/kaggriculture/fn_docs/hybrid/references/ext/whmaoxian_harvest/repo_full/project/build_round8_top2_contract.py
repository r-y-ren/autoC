"""Independent, bounded repair of fixed-cost cash/seed execution contracts.

Keep the frozen compact proxy byte-for-byte as the prefix. This does not modify
any original demonstration, route chooser, travel command or worker schedule.
"""
import hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).parent
SOURCE=ROOT/'experiments/round8_top2_dsm_compact.py'
DEST=ROOT/'experiments/round8_top2_dsm_contract.py'
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()=='1cc9732b115dcd1612b3ce848484c88701ac21071ed52f0c00a9571ffbcc0475'
suffix=r'''

# Local 2026-09-22 research experiment: fixed-cost execution contracts.
# See research/round8/top2/compact_NOTICE.txt and compact_LICENSE.txt.
# This is a public-demonstration proxy, not DSM's private agent source.
_R8_CONTRACT_PARENT=agent
_R8_CONTRACT_REPORT={'cash_order_repaired':0}

def _r8_contract(obs,configuration,action):
    step=int(obs['step']); player=int(obs['player'])
    if step==0:
        for key in _R8_CONTRACT_REPORT:_R8_CONTRACT_REPORT[key]=0
    standard=configuration is None or all(configuration.get(k,v)==v for k,v in
        [('boardSize',10),('turnsPerDay',24),('maxMarketOrdersPerTurn',10),
         ('farmHandCostMult',1),('shedCapacity',100)])
    if not standard:return action
    view=_View(obs,player,_R8_IMPL.cfg)
    market=action.setdefault('market',[])
    projected=_R8_IMPL._projected_shed(action,view)
    # Preserve all unit travel and all existing order quantities. When cash
    # cannot pay the fixed hires/seeds, move existing sales of presently owned
    # shed goods before those purchases. This funds the ORIGINAL hire turn,
    # preserving worker indices and their original spawn-and-travel schedule.
    required=0;hired=view.hires_today
    for order in market:
        if not order:continue
        if order[0]=='HIRE':required+=_fib(hired);hired+=1
        elif order[0]=='BUY_SEED' and len(order)>2:
            required+=SEED_PRICE.get(order[1],0)*int(order[2])
    if required>view.money:
        eligible=[];others=[];reserve=dict(projected)
        for order in market:
            if (len(order)>2 and order[0]=='SELL' and int(order[2])>0
                    and reserve.get(order[1],0)>=int(order[2])):
                eligible.append(order);reserve[order[1]]-=int(order[2])
            else:others.append(order)
        if eligible and eligible+others!=market:
            action['market']=eligible+others
            _R8_CONTRACT_REPORT['cash_order_repaired']+=1
    return action

def agent(obs,config=None):
    return _r8_contract(obs,config,_R8_CONTRACT_PARENT(obs,config))
agent.telemetry=_R8_CONTRACT_PARENT.telemetry
agent.routing_telemetry=_R8_CONTRACT_PARENT.routing_telemetry
agent.contract_telemetry=_R8_CONTRACT_REPORT
'''
generated=SOURCE.read_text(encoding='utf-8')+suffix
if '--check' in sys.argv:
    assert DEST.read_text(encoding='utf-8')==generated,'Frozen candidate differs from build'
    print('Frozen candidate matches the reproducible builder: '+hashlib.sha256(DEST.read_bytes()).hexdigest())
    raise SystemExit(0)
DEST.write_text(generated,encoding='utf-8')
report={'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        'candidate':str(DEST.relative_to(ROOT)),
        'candidate_sha256':hashlib.sha256(DEST.read_bytes()).hexdigest(),
        'changes':['Same-turn existing sales fund fixed hire/seed orders when cash is short; no other changes'],
        'forbidden_inputs':['hidden seed','unrevealed shops','evaluation outcome fingerprints'],
        'max_new_matches':5,
        'jobs':[{'seed':733556107,'seat':0,'opponent':'external/round8/fieldcraft/main.py'},
                {'seed':733556107,'seat':0,'opponent':'external/round8/master2965/main.py'},
                {'seed':800459488,'seat':0,'opponent':'submissions/release_v6/main.py'},
                {'seed':82003,'seat':1,'opponent':'submissions/release_v7/main.py'},
                {'seed':82005,'seat':0,'opponent':'submissions/release_v7/main.py'}]}
(ROOT/'research/round8/top2/contract_build.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report),flush=True)

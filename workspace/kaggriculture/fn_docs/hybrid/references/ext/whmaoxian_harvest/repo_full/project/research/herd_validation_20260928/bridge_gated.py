_BR28_R2_SHA='b35b5b09fbec059ab7cbd2ba67a9fbb6d3e467ef5262f3e2ddba592b3e50c1c4'
_BR28_NEW_SHA='f512593ca68514c82efa3450bb8392f5c90d20a7512e099f67e076b0348e46bd'
_BR28_MODE='gated'
_BR28_GATE=2000
"""Compatible two-turn opening and public-observation policy selection."""
import copy as _br_copy
import hashlib as _br_hash
from pathlib import Path as _BrPath
import inspect as _br_inspect
_BR28_FOLDER=_BrPath(_br_inspect.currentframe().f_code.co_filename).resolve().parent

def _br28_load(filename,expected):
    path=_BR28_FOLDER/filename;source=path.read_bytes()
    if _br_hash.sha256(source).hexdigest()!=expected:raise ValueError('Core hash mismatch')
    namespace={'__name__':'k28_core_'+filename,'__file__':str(path)}
    exec(compile(source,str(path),'exec'),namespace)
    return namespace['agent'],namespace

_BR28_R2,_BR28_R2_NS=_br28_load('bridge_r2_core.py',_BR28_R2_SHA)
_BR28_NEW,_BR28_NEW_NS=_br28_load('bridge_new_core.py',_BR28_NEW_SHA)
_BR28_STATE={}
_BR28_REPORT={'r2_choices':0,'new_choices':0,'errors':0}
_MP_REPORT=_BR28_REPORT
_BR28_CORE_REPORTS={label:{k:v for k,v in ns.items() if 'REPORT' in k or 'STATS' in k} for label,ns in (('r2',_BR28_R2_NS),('new',_BR28_NEW_NS))}

def _br28_virtual_r2(obs):
    virtual=_br_copy.deepcopy(obs);seat=int(obs['player'])
    virtual['farms'][seat]['money']+=1400
    virtual['private']['shed']['COW']-=1
    virtual['private']['shed']['SHEEP']-=2
    return virtual

def compatible_opening_agent(observation,configuration=None):
    step=int(observation['step']);seat=int(observation['player'])
    if step==0:
        _BR28_STATE[seat]={'mode':None,'prebought_seed':1}
        for key in _BR28_REPORT:_BR28_REPORT[key]=0
        original=_BR28_R2(observation,configuration)
        _BR28_NEW(observation,configuration)
        if original.get('farmer')!=['PASS']:raise ValueError('Unexpected R2 opening')
        return {'farmer':['PASS'],'hands':[],'market':[['BUY_PRODUCT','WHEAT',5],['BUY_SEED','WHEAT',1],['BUY_ANIMAL','COW',1],['BUY_ANIMAL','SHEEP',2]]}
    state=_BR28_STATE[seat]
    if step==1:
        rival=observation['farms'][1-seat]
        modern=not rival['hands'] and rival['farmer']==[4,4] and rival['money']<_BR28_GATE
        if _BR28_MODE=='r2':modern=False
        if _BR28_MODE=='new':modern=True
        state['mode']='new' if modern else 'r2'
        _BR28_REPORT[state['mode']+'_choices']+=1
        if modern:
            action=_BR28_NEW(observation,configuration)
            orders=[list(o) for o in action.get('market',[])]
            if len(orders)>=10:raise ValueError('No sheep procurement slot')
            orders.append(['BUY_ANIMAL','SHEEP',1])
            return dict(action,market=orders)
        state['prebought_seed']=0
        action=_BR28_R2(_br28_virtual_r2(observation),configuration)
        if action.get('farmer')!=['NORTH']:raise ValueError('Unexpected R2 continuation')
        orders=[list(o) for o in action.get('market',[])]
        expected={'COW':1,'SHEEP':2}
        for order in orders:
            if len(order)>=3 and order[0]=='BUY_ANIMAL' and order[1] in expected:
                deduction=min(expected[order[1]],int(order[2]))
                order[2]-=deduction;expected[order[1]]-=deduction
        if any(expected.values()):raise ValueError('Missing pre-purchased batch')
        return dict(action,farmer=['NORTH'],market=orders)
    action=(_BR28_NEW if state['mode']=='new' else _BR28_R2)(observation,configuration)
    if state['mode']=='new' and state['prebought_seed']:
        orders=[list(o) for o in action.get('market',[])]
        for o in orders:
            if len(o)>2 and o[:2]==['BUY_SEED','WHEAT']:
                q=min(int(o[2]),state['prebought_seed']);o[2]-=q;state['prebought_seed']-=q
        action=dict(action,market=orders)
    return action
compatible_opening_agent.telemetry=_BR28_REPORT
agent=compatible_opening_agent
kaggle_submission_agent=compatible_opening_agent

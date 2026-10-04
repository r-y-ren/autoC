"""Compile successful historical purchases, preserving original order slots."""
from collections import Counter
import contextlib
import copy
import gzip
import importlib
import io
import json
from pathlib import Path
from benchmark_replays import tape_policy
with contextlib.redirect_stdout(io.StringIO()):
    from kaggle_environments import make
engine=importlib.import_module('kaggle_environments.envs.kaggriculture.kaggriculture')
ROOT=Path(__file__).parent
OUT=ROOT/'research/round7/top2'
original={name:getattr(engine,name) for name in ['_process_market','_parse_order','_commit_unit','_do_hire','_do_buy_land']}
ctx={}

def market(state,env):
    ctx['turn']+=1
    ctx['farms']=[id(f) for f in state[0].observation.farms]
    ctx['order_positions']={id(order):i for s in state for i,order in enumerate(s.action.get('market',[])[:10])}
    return original['_process_market'](state,env)

def parse(order):
    if id(order) in ctx['order_positions']:
        ctx['order_index']=ctx['order_positions'][id(order)]
    return original['_parse_order'](order)

def record(farm):
    p=ctx['farms'].index(id(farm))
    ctx['success'][(ctx['turn'],p,ctx['order_index'])]+=1

def commit(op,item,price,farm,private,market,shed_capacity=100):
    ok=original['_commit_unit'](op,item,price,farm,private,market,shed_capacity)
    if ok:
        record(farm)
    return ok

def hire(farm,private,board_size,mult=1):
    before=len(farm['hands'])
    result=original['_do_hire'](farm,private,board_size,mult)
    if len(farm['hands'])>before:
        record(farm)
    return result

def land(farm,board_size):
    before=len(farm['unlocked_quadrants'])
    result=original['_do_buy_land'](farm,board_size)
    if len(farm['unlocked_quadrants'])>before:
        record(farm)
    return result

for name,fn in [('_process_market',market),('_parse_order',parse),('_commit_unit',commit),('_do_hire',hire),('_do_buy_land',land)]:
    setattr(engine,name,fn)
routes=[]
try:
    for row in json.loads((OUT/'index.json').read_text()):
        if row['split']!='study':
            continue
        game=json.loads(gzip.decompress((OUT/f"{row['episode_id']}.json.gz").read_bytes()))
        ctx.update(turn=-1,success=Counter())
        env=make('kaggriculture',configuration=dict(game['configuration'],seed=game['info']['seed']),debug=True)
        env.run([tape_policy([s[p]['action'] for s in game['steps'][1:]]) for p in range(2)])
        assert [s.status for s in env.steps[-1]]==['DONE','DONE']
        assert not [v.get('stderr') for logs in env.logs for v in logs if v.get('stderr')]
        actual=[s.reward for s in env.steps[-1]]
        assert actual==game['rewards'],(row['episode_id'],actual,game['rewards'])
        actions=[]
        requested,successful=Counter(),Counter()
        seat=row['seat']
        for t,s in enumerate(game['steps'][1:]):
            a=copy.deepcopy(s[seat]['action'])
            compiled=[]
            for i,order in enumerate(a.get('market',[])[:10]):
                qty=ctx['success'][(t,seat,i)]
                if not order:
                    compiled.append([])
                elif order[0]=='SELL':
                    compiled.append(order)
                elif order[0] in ('HIRE','BUY_LAND'):
                    requested[order[0]]+=1
                    successful[order[0]]+=qty
                    compiled.append([order[0]] if qty else [])
                elif order[0] in ('BUY_SEED','BUY_PRODUCT','BUY_ANIMAL'):
                    requested[f'{order[0]}:{order[1]}']+=int(order[2])
                    successful[f'{order[0]}:{order[1]}']+=qty
                    compiled.append([order[0],order[1],qty] if qty else [])
                else:
                    compiled.append([])
            a['market']=compiled
            actions.append(a)
        result={**row,'seed':game['info']['seed'],'shops':game['steps'][-1][seat]['observation']['town']['unlocked_shops'],'original_rewards':game['rewards'],'reconstructed_rewards':actual,'original_reproduced_exactly':True,'actions':actions,'requested_counts':dict(requested),'successful_counts':dict(successful),'semantics':'Non-SELL requests replaced by successful historical quantity. Failed orders are empty list placeholders to preserve order slots. SELL targets unchanged. These are demonstrated historical outcomes, not guaranteed future-feasible actions.'}
        routes.append(result)
        (OUT/'effective_routes.json').write_text(json.dumps({'routes':routes,'episode_split':'original study only','preserve_order_slots':True},indent=2),encoding='utf-8')
        print(row['team'],row['episode_id'],'exact',actual,'hires',requested['HIRE'],'->',successful['HIRE'],flush=True)
finally:
    for name,fn in original.items():
        setattr(engine,name,fn)

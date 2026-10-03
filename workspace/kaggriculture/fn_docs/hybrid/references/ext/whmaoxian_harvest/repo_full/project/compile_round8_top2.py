"""Compile public demonstrations using actual successful official-engine actions.

Study episodes only. Each original match must reproduce both final rewards exactly.
Daily task records distinguish actual operations from failed/no-op requests.
"""
from collections import Counter
import contextlib
import copy
import gc
import gzip
import importlib
import io
import json
from pathlib import Path
from benchmark_replays import tape_policy
with contextlib.redirect_stdout(io.StringIO()):
    from kaggle_environments import make

ROOT=Path(__file__).parent
OUT=ROOT/'research/round8/top2'
engine=importlib.import_module('kaggle_environments.envs.kaggriculture.kaggriculture')
NAMES=['_process_market','_parse_order','_commit_unit','_do_hire','_do_buy_land','_apply_unit_action']
original={name:getattr(engine,name) for name in NAMES}
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
    return p


def commit(op,item,price,farm,private,market,shed_capacity=100):
    ok=original['_commit_unit'](op,item,price,farm,private,market,shed_capacity)
    if ok:
        p=record(farm)
        if op=='SELL':
            ctx['sold'][(p,item)]+=1
            ctx['revenue'][(p,item)]+=price
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


def unit(farm,private,idx,action,board_size,day,turns_per_day,shed_capacity=100):
    if idx==0:
        ctx['unit_seat']=(ctx['unit_seat']+1)%2
    seat=ctx['unit_seat']
    active=seat==ctx['seat'] and action and action[0] not in ('NORTH','SOUTH','EAST','WEST','PASS')
    pos=engine._farmer_position(farm,idx) if active else None
    if pos is not None:
        x,y=pos
        before=copy.deepcopy((farm['tiles'][y][x],private['inventories'][idx],private['shed'],private['seeds']))
    result=original['_apply_unit_action'](farm,private,idx,action,board_size,day,turns_per_day,shed_capacity)
    if pos is not None:
        after=(farm['tiles'][y][x],private['inventories'][idx],private['shed'],private['seeds'])
        t=ctx['turn']+1
        if before!=after:
            ctx['tasks'].append({'step':t,'unit':idx,'position':[x,y],'action':list(action)})
        else:
            ctx['noop'][action[0]]+=1
    return result


def main():
    for name,fn in zip(NAMES,[market,parse,commit,hire,land,unit]):
        setattr(engine,name,fn)
    results=[]
    try:
        for row in json.loads((OUT/'index.json').read_text()):
            if row['split']!='study':
                continue
            dest=OUT/f"compiled_{row['episode_id']}_{row['seat']}.json.gz"
            if dest.exists():
                compiled=json.loads(gzip.decompress(dest.read_bytes()))
                results.append({k:v for k,v in compiled.items() if k not in ('actions','dawn_states','tasks')})
                continue
            game=json.loads(gzip.decompress((OUT/f"{row['episode_id']}.json.gz").read_bytes()))
            seat=row['seat']
            ctx.clear()
            ctx.update(turn=-1,success=Counter(),unit_seat=-1,seat=seat,tasks=[],noop=Counter(),sold=Counter(),revenue=Counter())
            env=make('kaggriculture',configuration=dict(game['configuration'],seed=game['info']['seed']),debug=True)
            env.run([tape_policy([s[p]['action'] for s in game['steps'][1:]]) for p in range(2)])
            actual=[s.reward for s in env.steps[-1]]
            assert actual==game['rewards'],(row['episode_id'],actual,game['rewards'])
            assert [s.status for s in env.steps[-1]]==['DONE','DONE']
            assert not [v.get('stderr') for logs in env.logs for v in logs if v.get('stderr')]
            actions=[]
            requested,successful=Counter(),Counter()
            for t,s in enumerate(game['steps'][1:]):
                a=copy.deepcopy(s[seat]['action']); compiled_orders=[]
                for i,order in enumerate(a.get('market',[])[:10]):
                    qty=ctx['success'][(t,seat,i)]
                    if not order:
                        compiled_orders.append([])
                    elif order[0]=='SELL':
                        compiled_orders.append(order)
                    elif order[0] in ('HIRE','BUY_LAND'):
                        requested[order[0]]+=1; successful[order[0]]+=qty
                        compiled_orders.append([order[0]] if qty else [])
                    elif order[0] in ('BUY_SEED','BUY_PRODUCT','BUY_ANIMAL'):
                        key=f'{order[0]}:{order[1]}'
                        requested[key]+=int(order[2]); successful[key]+=qty
                        compiled_orders.append([order[0],order[1],qty] if qty else [])
                    else:
                        compiled_orders.append([])
                a['market']=compiled_orders; actions.append(a)
            dawn=[]
            for t in range(0,719,24):
                obs=game['steps'][t][seat]['observation']
                dawn.append({'step':t,'farm':obs['farms'][seat],'private':obs['private'],'shops':obs['town']['unlocked_shops']})
            compiled={**row,'seed':game['info']['seed'],'rewards':game['rewards'],'original_reproduced_exactly':True,'actions':actions,'dawn_states':dawn,'tasks':ctx['tasks'],'noop_requests':dict(ctx['noop']),'requested':dict(requested),'successful':dict(successful),'sold':{item:n for (p,item),n in ctx['sold'].items() if p==seat},'sales_income':{item:n for (p,item),n in ctx['revenue'].items() if p==seat}}
            dest.write_bytes(gzip.compress(json.dumps(compiled,separators=(',',':')).encode()))
            results.append({k:v for k,v in compiled.items() if k not in ('actions','dawn_states','tasks')})
            (OUT/'compiled_index.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
            print(row['team'],row['episode_id'],'exact',actual,'tasks',len(ctx['tasks']),flush=True)
            del game,env,compiled,actions,dawn
            gc.collect()
    finally:
        for name,fn in original.items():
            setattr(engine,name,fn)


if __name__=='__main__':
    main()

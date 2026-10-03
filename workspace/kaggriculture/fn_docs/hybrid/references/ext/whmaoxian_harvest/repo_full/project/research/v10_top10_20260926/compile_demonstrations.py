"""Extract successful public task/transaction demonstrations; observe engine calls unchanged."""
from pathlib import Path
from collections import Counter
import copy,gzip,hashlib,json,sys
N=Path(__file__).resolve().parent;R=N.parents[1]
sys.path.insert(0,str(R/'research/v10_rebuild_20260926'))
import fast_arena as arena
engine=arena.engine
original={name:getattr(engine,name) for name in ('_process_market','_parse_order','_commit_unit','_do_hire','_do_buy_land','_apply_unit_action')}
ctx={}
def market(state,env):
    ctx['farms']=[id(f) for f in state[0].observation.farms]
    ctx['slots']={id(order):i for s in state for i,order in enumerate(s.action.get('market',[])[:10])}
    return original['_process_market'](state,env)
def parse(order):
    if id(order) in ctx['slots']:ctx['slot']=ctx['slots'][id(order)]
    return original['_parse_order'](order)
def record(farm,count=1):
    p=ctx['farms'].index(id(farm));ctx['success'][(ctx['step'],p,ctx['slot'])]+=count

def commit(op,item,price,farm,private,market,shed_capacity=100):
    ok=original['_commit_unit'](op,item,price,farm,private,market,shed_capacity)
    if ok:record(farm)
    return ok

def hire(farm,private,board_size,mult=1):
    before=len(farm['hands']);result=original['_do_hire'](farm,private,board_size,mult)
    if len(farm['hands'])>before:record(farm)
    return result

def land(farm,board_size):
    before=len(farm['unlocked_quadrants']);result=original['_do_buy_land'](farm,board_size)
    if len(farm['unlocked_quadrants'])>before:record(farm)
    return result

def unit(farm,private,actor,command,board_size,day,turns_per_day,shed_capacity=100):
    positions=[farm['farmer']]+farm['hands']
    p=ctx['farms'].index(id(farm))
    if p not in ctx['plans'] or actor>=len(positions) or not command or command[0] in ('PASS','NORTH','SOUTH','EAST','WEST'):
        return original['_apply_unit_action'](farm,private,actor,command,board_size,day,turns_per_day,shed_capacity)
    x,y=positions[actor]
    before=copy.deepcopy((farm['tiles'][y][x],private['inventories'][actor],private['shed'],private['seeds']))
    result=original['_apply_unit_action'](farm,private,actor,command,board_size,day,turns_per_day,shed_capacity)
    after=(farm['tiles'][y][x],private['inventories'][actor],private['shed'],private['seeds'])
    if before!=after:
        cmd=list(command)
        if cmd[0]=='PICKUP':cmd=['PICKUP',cmd[1],after[1].get(cmd[1],0)-before[1].get(cmd[1],0)]
        ctx['plans'][p][day]['tasks'][actor].append(dict(xy=[x,y],op=cmd,hour=ctx['step']%24,quadrant=1+(x>=5)+2*(y>=5)))
    return result


def compile_episode(episode,views):
    raw=gzip.decompress((N/f'study_replays/{episode}.json.gz').read_bytes());game=json.loads(raw)
    state,env=arena.new_game(game['info']['seed'],game['configuration'])
    seats={v['seat'] for v in views}
    plans={p:[dict(hands=0,hire_hours=[],tasks=[[] for _ in range(40)]) for d in range(30)] for p in seats}
    ctx.update(step=0,success=Counter(),plans=plans,farms=[id(f) for f in state[0].observation.farms])
    equal_observations=0
    for step in range(719):
        ctx['step']=step
        for p in (0,1):
            state[p].observation.step=step
            state[p].action=copy.deepcopy(game['steps'][step+1][p]['action'])
        engine.interpreter(state,env)
        for p in (0,1):
            reference=game['steps'][step+1][p]['observation']
            assert all(state[p].observation[k]==reference[k] for k in ('farms','market','town','private','day','hour')), (episode,step,p)
            equal_observations+=1
        if (step+1)%24:
            for p in seats:
                count=len(state[p].observation.farms[p]['hands']);plan=plans[p][step//24]
                plan['hands']=max(plan['hands'],count)
                plan['hire_hours'].extend([step%24]*max(0,count-len(plan['hire_hours'])))
    assert [s.reward for s in state]==game['rewards']
    receipts=[]
    for view in views:
        p=view['seat'];actions=[]
        for step in range(719):
            action=copy.deepcopy(game['steps'][step+1][p]['action']);orders=[]
            for i,order in enumerate(action.get('market',[])[:10]):
                quantity=ctx['success'][(step,p,i)]
                if order and order[0]=='SELL':orders.append(order)
                elif order and order[0] in ('HIRE','BUY_LAND'):orders.append([order[0]] if quantity else [])
                elif order and order[0] in ('BUY_SEED','BUY_PRODUCT','BUY_ANIMAL'):orders.append([order[0],order[1],quantity] if quantity else [])
                else:orders.append([])
            action['market']=orders;actions.append(action)
        for plan in plans[p]:plan['tasks']=plan['tasks'][:plan['hands']+1]
        result=dict(view,actions=actions,plans=plans[p],historical_seed=game['info']['seed'],
            historical_rewards=game['rewards'],replay_sha256=hashlib.sha256(raw).hexdigest(),
            exact_observations=equal_observations,scope='Public historical demonstration, not hidden live state.')
        target=N/'demonstrations'/f'{episode}_{p}.json.gz'
        target.parent.mkdir(exist_ok=True)
        target.write_bytes(gzip.compress(json.dumps(result,separators=(',',':')).encode(),compresslevel=6))
        receipts.append(dict(view,path=target.relative_to(R).as_posix(),sha256=hashlib.sha256(target.read_bytes()).hexdigest(),tasks=sum(len(q) for d in plans[p] for q in d['tasks'])))
    print(json.dumps(dict(episode=episode,views=len(views),exact_observations=equal_observations,rewards=game['rewards'])),flush=True)
    return receipts

if __name__=='__main__':
    split=json.loads((N/'replay_split.json').read_text(encoding='utf-8'));receipts=[]
    replacements={'_process_market':market,'_parse_order':parse,'_commit_unit':commit,
        '_do_hire':hire,'_do_buy_land':land,'_apply_unit_action':unit}
    try:
        for name,fn in replacements.items():setattr(engine,name,fn)
        for episode in sorted({v['episode'] for v in split['study']}):
            receipts.extend(compile_episode(episode,[v for v in split['study'] if v['episode']==episode]))
            (N/'demonstrations_index.json').write_text(json.dumps(receipts,indent=2),encoding='utf-8')
    finally:
        for name,fn in original.items():setattr(engine,name,fn)
    print(json.dumps(dict(demonstrations=len(receipts))),flush=True)

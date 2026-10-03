"""Replay public actions through unchanged rules; audit cash by product and day."""
from pathlib import Path
from collections import Counter
import contextlib, copy, gzip, io, json, sys
D=Path(__file__).resolve().parent; R=D.parents[1]
SOURCE=R/'research/meta_rebuild_20260927/r2_feedback'
sys.path.insert(0,str(R/'research/v10_rebuild_20260926'))
with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
    import fast_arena as fa

def audit(row):
    game=json.loads(gzip.decompress((SOURCE/f"{row['episode']}.json.gz").read_bytes()))
    state,env=fa.new_game(game['info']['seed'],game['configuration'])
    stats=[dict(sales=Counter(),revenue=Counter(),purchases=Counter(),harvest=Counter(),wages=0,land=0,hires=0) for _ in range(2)]
    ids={};daily=[];differences=[]
    names=('_commit_unit','_do_hire','_do_buy_land','_apply_unit_action')
    original={n:getattr(fa.engine,n) for n in names}
    def commit(op,item,price,farm,private,market,shed_capacity=100):
        before=farm['money'];ok=original['_commit_unit'](op,item,price,farm,private,market,shed_capacity)
        if ok:
            s=stats[ids[id(farm)]];delta=farm['money']-before
            if op=='SELL':s['sales'][item]+=1;s['revenue'][item]+=delta
            else:s['purchases'][op+':'+item]-=delta
        return ok
    def hire(farm,private,board_size,mult=1):
        before=farm['money'];n=len(farm['hands'])
        out=original['_do_hire'](farm,private,board_size,mult)
        s=stats[ids[id(farm)]];s['wages']+=before-farm['money'];s['hires']+=len(farm['hands'])-n
        return out
    def land(farm,board_size):
        before=farm['money'];out=original['_do_buy_land'](farm,board_size)
        stats[ids[id(farm)]]['land']+=before-farm['money'];return out
    def unit(farm,private,idx,action,board_size,day,turns_per_day,shed_capacity=100):
        tracked=bool(action and action[0]=='HARVEST' and idx<len(private['inventories']))
        before=dict(private['inventories'][idx]) if tracked else {}
        out=original['_apply_unit_action'](farm,private,idx,action,board_size,day,turns_per_day,shed_capacity)
        if tracked:
            s=stats[ids[id(farm)]]
            for item,n in private['inventories'][idx].items():s['harvest'][item]+=max(0,n-before.get(item,0))
        return out
    try:
        for n,fn in zip(names,(commit,hire,land,unit)):setattr(fa.engine,n,fn)
        for t in range(719):
            ids={id(f):i for i,f in enumerate(state[0].observation.farms)}
            for i in (0,1):
                state[i].observation.step=t
                state[i].action=copy.deepcopy(game['steps'][t+1][i]['action'])
            fa.engine.interpreter(state,env)
            for s in state:s.observation.step=t+1
            recorded=game['steps'][t+1][0]['observation']
            if state[0].observation.farms!=recorded['farms'] and len(differences)<8:
                differences.append(t+1)
            if (t+1)%24==0 or t==718:
                farms=state[0].observation.farms;snapshot=[]
                for i,f in enumerate(farms):
                    mix=Counter(z.get('animal') or z.get('crop') or z.get('kind') for line in f['tiles'] for z in line if isinstance(z,dict))
                    snapshot.append(dict(money=f['money'],mix=dict(mix),land=f['unlocked_quadrants'],economics=copy.deepcopy(stats[i])))
                daily.append(dict(step=t+1,farms=snapshot,prices=dict(state[0].observation.market['prices']),shops=list(state[0].observation.town['unlocked_shops'])))
        money=[s.reward for s in state]
        for s,m in zip(stats,money):
            assert 3000+sum(s['revenue'].values())-sum(s['purchases'].values())-s['wages']-s['land']==m
        valid=not differences and money==game['rewards']
        return dict(row,valid=valid,simulated_money=money,recorded_money=game['rewards'],divergent_steps=differences,daily=daily,economics=stats)
    finally:
        for n,fn in original.items():setattr(fa.engine,n,fn)

if __name__=='__main__':
    report=[]
    for row in json.loads((SOURCE/'selection.json').read_text()):
        result=audit(row);report.append(result)
        (D/'replay_economics.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
        own=row['seat'];other=1-own
        delta={p:result['economics'][own]['revenue'].get(p,0)-result['economics'][other]['revenue'].get(p,0) for p in fa.engine.PRODUCTS}
        print(json.dumps(dict(episode=row['episode'],valid=result['valid'],margin=row['margin'],revenue_delta=delta,wages=[s['wages'] for s in result['economics']],land=[s['land'] for s in result['economics']])),flush=True)

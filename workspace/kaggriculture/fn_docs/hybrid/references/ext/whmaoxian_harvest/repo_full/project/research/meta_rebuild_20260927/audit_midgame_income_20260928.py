"""Read archived public games and attribute income with unchanged game transitions."""
from pathlib import Path
from collections import Counter
import contextlib,copy,gzip,io,json,sys
D=Path(__file__).resolve().parent;R=D.parents[1];F=D/'r2_feedback'
sys.path.insert(0,str(R/'research/v10_rebuild_20260926'))
with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
    import fast_arena as fa

def audit(row):
    game=json.loads(gzip.decompress((F/f"{row['episode']}.json.gz").read_bytes()))
    state,env=fa.new_game(game['info']['seed'],game['configuration'])
    stats=[dict(revenue=Counter(),sales=Counter(),purchases=Counter(),harvest=Counter(),wages=0,land=0) for _ in range(2)]
    ids={id(f):i for i,f in enumerate(state[0].observation.farms)}
    names=('_commit_unit','_do_hire','_do_buy_land','_apply_unit_action')
    original={name:getattr(fa.engine,name) for name in names}
    def commit(op,item,price,farm,private,market,shed_capacity=100):
        before=farm['money'];ok=original['_commit_unit'](op,item,price,farm,private,market,shed_capacity)
        if ok:
            s=stats[ids[id(farm)]];delta=farm['money']-before
            if op=='SELL':s['sales'][item]+=1;s['revenue'][item]+=delta
            else:s['purchases'][op+':'+item]-=delta
        return ok
    def hire(farm,private,board_size,mult=1):
        before=farm['money'];result=original['_do_hire'](farm,private,board_size,mult)
        stats[ids[id(farm)]]['wages']+=before-farm['money'];return result
    def land(farm,board_size):
        before=farm['money'];result=original['_do_buy_land'](farm,board_size)
        stats[ids[id(farm)]]['land']+=before-farm['money'];return result
    def unit(farm,private,idx,action,board_size,day,turns_per_day,shed_capacity=100):
        track=bool(action and action[0]=='HARVEST' and idx<len(private['inventories']))
        before=dict(private['inventories'][idx]) if track else {}
        result=original['_apply_unit_action'](farm,private,idx,action,board_size,day,turns_per_day,shed_capacity)
        if track:
            s=stats[ids[id(farm)]]
            for item,q in private['inventories'][idx].items():s['harvest'][item]+=max(0,q-before.get(item,0))
        return result
    daily=[];mismatches=[]
    try:
        for name,fn in zip(names,(commit,hire,land,unit)):setattr(fa.engine,name,fn)
        for t in range(719):
            for i in (0,1):
                state[i].observation.step=t
                state[i].action=copy.deepcopy(game['steps'][t+1][i]['action'])
            fa.engine.interpreter(state,env)
            recorded=game['steps'][t+1][0]['observation']
            for key in ('farms','market','town'):
                if state[0].observation[key]!=recorded[key]:mismatches.append((t+1,key))
            if (t+1)%24==0 or t==718:
                farms=state[0].observation.farms;mix=[]
                for f in farms:
                    mix.append(dict(Counter(tile.get('animal') or tile.get('crop') or tile.get('kind') for tiles in f['tiles'] for tile in tiles if isinstance(tile,dict))))
                daily.append(dict(step=t+1,cash=[f['money'] for f in farms],mix=mix,cumulative=copy.deepcopy(stats)))
        money=[s.reward for s in state]
        for i,s in enumerate(stats):
            assert 3000+sum(s['revenue'].values())-sum(s['purchases'].values())-s['wages']-s['land']==money[i]
        assert money==game['rewards'],(money,game['rewards'])
        assert not mismatches,mismatches[:5]
        return dict(row,valid=True,all_719_transitions_equal=True,daily=daily,final=stats,rewards=money)
    finally:
        for name,fn in original.items():setattr(fa.engine,name,fn)

if __name__=='__main__':
    results=[]
    for row in json.loads((F/'selection.json').read_text()):
        result=audit(row);results.append(result)
        seat=row['seat'];own,other=result['final'][seat],result['final'][1-seat]
        delta={i:own['revenue'].get(i,0)-other['revenue'].get(i,0) for i in set(own['revenue'])|set(other['revenue'])}
        print(json.dumps(dict(episode=row['episode'],reproduced=result['valid'],margin=row['margin'],revenue_difference=delta,wage_difference=own['wages']-other['wages'])),flush=True)
        (D/'midgame_income_audit_20260928.json').write_text(json.dumps(results,indent=2),encoding='utf-8')

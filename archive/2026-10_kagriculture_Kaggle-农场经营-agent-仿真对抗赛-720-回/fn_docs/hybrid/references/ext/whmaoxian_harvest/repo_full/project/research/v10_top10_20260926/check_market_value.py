"""Compare fast price-prefix calculations with explicit per-unit transactions."""
from pathlib import Path
import copy,json,sys
D=Path(__file__).resolve().parent;R=D.parents[1]
sys.path.insert(0,str(R/'research/v10_rebuild_20260926'))
import fast_arena as a
entry=a.load('research/v10_top10_20260926/market_value/v00.py');ns=entry.__globals__
assert entry.__name__=='market_value_agent'
state,env=a.new_game(0);obs=copy.deepcopy(state[0].observation);obs.update(step=300,day=12,hour=12)
obs['town']['unlocked_shops']=['SMOOTHIE_SHOP','ICE_CREAM_SHOP','YARN_STORE']
ns['_OR2_STATE'][0]={'stock':{'MILK':17,'WOOL':11,'STRAWBERRY':13}}
params=ns['_v44y_params'](obs);checks=0
for item in ('MILK','WOOL','STRAWBERRY'):
    for inv in (9850,10000,10100):
        obs['market']['inventory'][item]=inv
        horizon=ns['_MV_HORIZON'];shops=obs['town']['unlocked_shops']
        per=sum((2 if len(ns['_OR2_SHOPS'].get(s,()))==1 else 1) for s in shops if item in ns['_OR2_SHOPS'].get(s,()))
        demand=per*sum(t%4==0 for t in range(300,300+horizon))+sum(t%24==0 for t in range(300,300+horizon))
        rival=int(ns['_OR2_STATE'][0]['stock'][item]*ns['_MV_STOCK_WEIGHT']+.5)
        scenarios=((0,.25),(rival,.75*.7),(min(100,rival*2),.75*.3))
        def sell(level,n):
            revenue=0
            for _ in range(n):
                price=max(1,ns['_r37_market_price'](item,level,params))
                revenue+=price;level+=int(price>1)
            return revenue,level
        scores=[]
        for quantity in range(9):
            now,post=sell(inv,quantity);value=0.0
            for other,weight in scenarios:
                rival_first,end=sell(inv-demand//2,other)
                rival_late,_=sell(post-demand//2,other)
                our_late,_=sell(end-(demand-demand//2),quantity)
                value+=weight*(now-our_late+ns['_MV_RIVAL_WEIGHT']*(rival_first-rival_late))
            scores.append(value)
        expected=max(range(9),key=lambda q:(scores[q],-abs(q-3)))
        if scores[expected]<=scores[3]+ns['_MV_MIN_GAIN']:expected=3
        actual=ns['_mv_quantity'](obs,item,8,3,params)
        assert actual==expected,(item,inv,actual,expected,scores)
        checks+=1
report=dict(passed=True,explicit_transaction_comparisons=checks,scope='Synthetic model-equivalence checks only; no opponent win-rate claim.')
(D/'market_value_unit_checks.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report),flush=True)

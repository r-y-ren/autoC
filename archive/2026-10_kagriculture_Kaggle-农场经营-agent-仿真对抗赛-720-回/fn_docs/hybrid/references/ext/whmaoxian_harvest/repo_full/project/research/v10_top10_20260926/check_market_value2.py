"""Independent per-unit comparison of the full-inventory margin objective."""
from pathlib import Path
import copy,json,sys
D=Path(__file__).resolve().parent;R=D.parents[1]
sys.path.insert(0,str(R/'research/v10_rebuild_20260926'))
import fast_arena as a
fn=a.load('research/v10_top10_20260926/market_value2/v00.py');ns=fn.__globals__
s,env=a.new_game(0);obs=copy.deepcopy(s[0].observation);obs.update(step=300,day=12,hour=12)
obs['town']['unlocked_shops']=['SMOOTHIE_SHOP','ICE_CREAM_SHOP','YARN_STORE'];params=ns['_v44y_params'](obs)
ns['_OR2_STATE'][0]={'stock':{'MILK':17,'WOOL':11,'STRAWBERRY':13}};checks=0
for item in ('MILK','WOOL','STRAWBERRY'):
    for inventory in (9850,10000,10100):
        obs['market']['inventory'][item]=inventory
        demand=sum((2 if len(ns['_OR2_SHOPS'].get(shop,()))==1 else 1) for shop in obs['town']['unlocked_shops'] if item in ns['_OR2_SHOPS'].get(shop,()))
        rival=int(ns['_OR2_STATE'][0]['stock'][item]*.4+.5)
        def sell(level,quantity):
            total=0
            for _ in range(quantity):
                price=max(1,ns['_r37_market_price'](item,level,params))
                total+=price;level+=int(price>1)
            return total,level
        values=[]
        for early in range(9):
            first,level=sell(inventory,early);score=0
            for count,weight in ((0,.25),(rival,.525),(2*rival,.225)):
                other,nextlevel=sell(level-demand//2,count)
                rest,_=sell(nextlevel-(demand-demand//2),8-early)
                score+=weight*(first+rest-.5*other)
            values.append(score)
        expected=max(range(9),key=lambda q:(values[q],-abs(q-3)))
        if values[expected]<=values[3]+5:expected=3
        actual=ns['_mv_quantity'](obs,item,8,3,params)
        assert actual==expected,(item,inventory,actual,expected)
        checks+=1
report=dict(passed=True,full_inventory_transaction_checks=checks,scope='Model implementation check, not evidence of gameplay strength.')
(D/'market_value2_unit_checks.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report),flush=True)

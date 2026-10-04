"""Check probability conservation and trading against original official functions."""
from pathlib import Path
import copy,json,sys,time
D=Path(__file__).resolve().parent;R=D.parents[1]
sys.path.insert(0,str(R/'research/v10_rebuild_20260926'))
import fast_arena as a
fn=a.load('research/v10_top10_20260926/herd_expectation/risk0_stock0.py');ns=fn.__globals__
probability_checks=0;trade_checks=0
for item in ('EGG','MILK','WOOL'):
    for day,count in ((0,0),(7,2),(13,4),(24,8)):
        scenarios=ns['_he_scenarios'](item,day,['BAKERY']*count)
        assert abs(sum(p for x,p in scenarios)-1)<1e-10
        dates=[d for d in range(day+1,30) if d%3==0 and d<=24][:max(0,8-count)]
        expected=len(dates)*sum((2 if len(v)==1 else 1) for v in ns['_HD2_SHOP_TYPES'].values() if item in v)/len(ns['_HD2_SHOP_TYPES'])
        assert abs(sum(sum(x.values())*p for x,p in scenarios)-expected)<1e-10
        probability_checks+=1
    for inventory in (9850,10000,10400):
        for mine,theirs in ((3,7),(9,2)):
            state,env=a.new_game(0);market=state[0].observation.market
            market['inventory'][item]=inventory
            params=ns['_v44y_params'](state[0].observation)
            expected=ns['_he_trade'](inventory,mine,theirs,lambda i:ns['_r37_market_price'](item,i,params))
            for seat,quantity in enumerate((mine,theirs)):
                state[seat].observation.private['shed'][item]=quantity
                state[seat].action={'farmer':['PASS'],'hands':[],'market':[['SELL',item,quantity]]}
            a.engine._process_market(state,env)
            actual=(state[0].observation.farms[0]['money']-3000,state[0].observation.farms[1]['money']-3000,market['inventory'][item])
            assert actual==expected,(item,inventory,actual,expected)
            trade_checks+=1
report={'passed':True,'probability_checks':probability_checks,'official_market_comparisons':trade_checks,'scope':'Implementation checks only, not game-strength evidence.'}
(D/'herd_expectation_unit_checks.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report),flush=True)

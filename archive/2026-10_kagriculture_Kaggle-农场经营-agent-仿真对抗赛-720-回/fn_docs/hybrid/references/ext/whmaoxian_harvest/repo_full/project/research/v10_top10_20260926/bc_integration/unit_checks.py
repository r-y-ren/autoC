"""Synthetic integration contracts, separate from game-strength evidence."""
from pathlib import Path
import copy,hashlib,json,runpy
B=Path(__file__).resolve().parent
ns=runpy.run_path(str(B/'add_p55_q16.py'));ns=ns['market_bc_agent'].__globals__;cfg=ns['_MBC_CFG']
checks=[]
obs=dict(player=0,step=250,market={'prices':{i:100 for i in ns['_MBC_ITEMS']}})
action=dict(farmer=['PASS'],hands=[],market=[['HIRE'],['SELL','MILK',2]])
context=dict(projected={'MILK':10},own={'money':20000},total=10,non_sells=[['HIRE']])
ns['_mbc_features']=lambda context,item:[0.0]*45
ns['_mbc_predict']=lambda features:[.99,.8]
fn=ns['_mbc_advise'];out=fn(obs,copy.deepcopy(action),context)
assert out['farmer']==action['farmer'] and out['hands']==action['hands']
assert out['market'][0]==['HIRE'] and out['market'][1]==['SELL','MILK',8]
checks.append('bounded_sell_only_preserves_physical_and_non_sell_orders')
full=dict(action,market=[['HIRE']]*10)
assert fn(obs,full,context)==full
checks.append('max_ten_order_slots')
assert fn(obs,action,dict(context,own={'money':7999}))==action
assert fn(dict(obs,step=700),action,context)==action
checks.extend(['low_cash_fallback','endgame_unchanged'])
picked=dict(action,farmer=['PICKUP','MILK'])
assert fn(obs,picked,context)==picked
checks.append('protect_same_turn_pickup')
buy=dict(action,market=[['BUY_PRODUCT','WHEAT',5],['SELL','MILK',2]])
assert fn(obs,buy,context)==buy
checks.append('input_purchase_turn_unchanged')
cfg['mode']='shadow'
assert fn(obs,action,context) is action
checks.append('shadow_returns_original_object')
cfg['mode']='active'
state={'prev':{'step':250,'own':{'MILK':2}}}
ns['_OR2_STATE'][0]=state
ns['_RACE_STATE'][0]={'step':250,'prev_action':action}
ns['_mbc_sync_observers'](obs,out,{'MILK':8})
assert state['prev']['own']['MILK']==8
assert ns['_RACE_STATE'][0]['prev_action']==out
checks.append('observers_receive_final_emitted_sales')
result=dict(passed=True,checks=checks,scope='Synthetic contracts only, not match strength.')
(B/'unit_checks.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result),flush=True)

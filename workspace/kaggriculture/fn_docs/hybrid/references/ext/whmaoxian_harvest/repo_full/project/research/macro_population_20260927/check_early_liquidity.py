"""Synthetic action-contract checks, not win-rate evidence."""
from pathlib import Path
import contextlib,copy,io,json,sys
D=Path(__file__).resolve().parent;R=D.parents[1]
sys.path.insert(0,str(R/'research/v10_rebuild_20260926'))
with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):import fast_arena as fa
entry=fa.load('research/macro_population_20260927/early_liquidity/grain_h4.py');ns=entry.__globals__
ns['FarmView']=lambda obs:None
ns['projected_shed']=lambda action,view:{'WHEAT':10}
ns['_ca_tape']=lambda seat,t:{'farmer':['FEED'],'hands':[]}
obs={'step':90,'player':0,'farms':[{'money':100},{}],'market':{'prices':{'WHEAT':25}}}
action={'farmer':['PASS'],'hands':[],'market':[]};before=copy.deepcopy(action)
result=ns['_el_apply'](obs,action)
assert result['market']==[['SELL','WHEAT',3]] and action==before
assert result['farmer']==action['farmer'] and result['hands']==action['hands']
ns['_ca_tape']=lambda seat,t:{'farmer':['FEED'],'hands':[['FEED'],['FEED']]}
assert ns['_el_apply'](obs,action)==action
ns['_ca_tape']=lambda seat,t:{}
pick=dict(action,farmer=['PICKUP','WHEAT',1]);assert ns['_el_apply'](obs,pick)==pick
buy=dict(action,market=[['BUY_PRODUCT','WHEAT',1]]);assert ns['_el_apply'](obs,buy)==buy
full=dict(action,market=[[] for _ in range(10)]);assert ns['_el_apply'](obs,full)==full
rich=copy.deepcopy(obs);rich['farms'][0]['money']=5000;assert ns['_el_apply'](rich,action)==action
late=dict(obs,step=288);assert ns['_el_apply'](late,action)==action
result=dict(passed=True,checks=['future_feed_reserve','own_inventory_bound','physical_actions_unchanged','pickup_and_purchase_protection','ten_slots','cash_and_time_gate'],scope='Synthetic local contracts only. Future profit and solvency require actual games.')
(D/'early_liquidity_checks.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))

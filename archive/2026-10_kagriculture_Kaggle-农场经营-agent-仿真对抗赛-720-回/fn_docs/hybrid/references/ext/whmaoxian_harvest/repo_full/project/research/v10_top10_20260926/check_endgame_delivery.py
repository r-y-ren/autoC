"""Synthetic movement/deadline checks in an isolated agent namespace."""
from pathlib import Path
import copy,hashlib,json,sys
D=Path(__file__).resolve().parent;R=D.parents[1]
sys.path.insert(0,str(R/'research/v10_rebuild_20260926'))
import fast_arena as arena
path='research/v10_top10_20260926/endgame_delivery/collect90.py'
entry=arena.load(path);assert entry.__name__=='endgame_delivery_agent';ns=entry.__globals__
state,cfg=arena.new_game(0);initial=copy.deepcopy(state[0].observation)
initial.update(step=713,day=29,hour=17)
farm=initial['farms'][0];farm['farmer']=[4,4];farm['hands']=[[4,5]];farm['unlocked_quadrants']=['NW','NE','SW','SE'];farm['tiles']=[[None]*10 for _ in range(10)]
farm['tiles'][5][5]={'kind':'PLANT','crop':'WHEAT','yield_units':4,'max_lifespan_step':10000,'watered_today':True}
initial['private']['inventories']=[{},{}];initial['private']['shed']={item:0 for item in ns['PRODUCTS']}
action={'farmer':['PASS'],'hands':[['PASS']],'market':[]}
chassis=ns['_IMPL'].chassis;saved=chassis.routes[2]
route=[copy.deepcopy(action) for _ in range(719)];route[718]['hands']=[['DROP']]
chassis.routes[2]=route;checks=[]
try:
    obs=copy.deepcopy(initial);ns['_ED_STATE'].clear()
    a=ns['_ed_apply'](obs,action);assert a['hands']==[['EAST']] and a['market']==[]
    obs.update(step=714,hour=18);obs['farms'][0]['hands']=[[5,5]]
    a=ns['_ed_apply'](obs,action);assert a['hands']==[['HARVEST']] and a['market']==[]
    obs.update(step=715,hour=19);obs['farms'][0]['tiles'][5][5]=None;obs['private']['inventories'][1]={'WHEAT':4}
    a=ns['_ed_apply'](obs,action);assert a['hands']==[['DROP']] and a['market']==[]
    checks.append('move_collect_return_without_market_changes')
    ns['_ED_STATE'].clear();obs=copy.deepcopy(initial);obs.update(step=716,hour=20)
    assert ns['_ed_apply'](obs,action)==action;checks.append('late_collection_rejected')
    ns['_ED_STATE'].clear();obs=copy.deepcopy(initial);obs['private']['shed']['WHEAT']=90
    assert ns['_ed_apply'](obs,action)==action;checks.append('warehouse_budget_preserved')
    ns['_ED_STATE'].clear();obs=copy.deepcopy(initial);route[714]['hands']=[['HARVEST']]
    assert ns['_ed_apply'](obs,action)==action;checks.append('future_productive_worker_reserved')
    route[714]['hands']=[['PASS']]
    ns['_TERMINAL_PLANS'][0]={'accepted':True}
    assert ns['_ed_apply'](copy.deepcopy(initial),action)==action;checks.append('accepted_existing_plan_preserved')
    ns['_TERMINAL_PLANS'].clear();ns['_ED_STATE'].clear()
    obs=copy.deepcopy(initial);obs.update(step=718,hour=22)
    assert ns['_ed_apply'](obs,action)==action;checks.append('final_liquidation_left_to_parent')
finally:chassis.routes[2]=saved
report=dict(passed=True,checks=checks,entrypoint=entry.__name__,source_sha256=hashlib.sha256((R/path).read_bytes()).hexdigest(),scope='Isolated synthetic checks. Full-game behavior and realized profit remain unvalidated here.')
(D/'endgame_unit_checks.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report),flush=True)

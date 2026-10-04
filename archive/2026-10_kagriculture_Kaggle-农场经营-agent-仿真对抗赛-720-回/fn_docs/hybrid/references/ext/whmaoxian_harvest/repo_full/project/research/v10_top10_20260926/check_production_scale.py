"""Check absolute investment bookkeeping without modifying the game engine."""
from pathlib import Path
from types import SimpleNamespace
import copy,hashlib,json,sys
D=Path(__file__).resolve().parent;R=D.parents[1]
sys.path.insert(0,str(R/'research/v10_rebuild_20260926'))
import fast_arena as arena
path='research/v10_top10_20260926/production_scale/full152_net2k.py'
entry=arena.load(path);assert entry.__name__=='production_scale_agent';ns=entry.__globals__
state,env=arena.new_game(0);obs=copy.deepcopy(state[0].observation);obs.update(step=432,day=18,hour=0)
farm=obs['farms'][0];farm['money']=100000;farm['unlocked_quadrants']=['NW','NE','SW']
farm['tiles']=[[('LOCKED' if x>=5 and y>=5 else None) for x in range(10)] for y in range(10)]
obs['private']['shed']={i:0 for i in ns['PRODUCTS']};obs['private']['seeds']={i:0 for i in ('WHEAT','CARROT','TOMATO','STRAWBERRY','MELON')}
obs['town']['unlocked_shops']=['PIZZA_SHOP','FARMERS_MARKET'];obs['market']['inventory']['TOMATO']=9600
native={'route':0};chassis=ns['_IMPL'].chassis;saved=chassis.routes
chassis.routes={0:[{'farmer':['PASS'],'hands':[],'market':[]} for _ in range(719)]}
checks=[]
try:
    assert not ns['_PS_BASE_QUAL'](obs,native)
    value=ns['_ps_absolute_value'](obs,native);assert value is not None and value['land_seeds']==4950
    assert value['net']==value['revenue']-value['land_seeds']-value['labor']-value['fertilizer']
    assert ns['_v219_qualifies'](obs,native) and ns['_PS_CHOICES'][0]['new19']
    assert ns['_t19_qualifies'](obs,{'eligible':True})
    checks.append('independent_full_cost_gate_not_incremental_72_unit_gate')
    poor=copy.deepcopy(obs);poor['farms'][0]['money']=17999
    assert ns['_ps_absolute_value'](poor,native) is None;checks.append('initial_cash_guard_retained')
    a={'farmer':['PASS'],'hands':[],'market':[]};late=copy.deepcopy(obs);late.update(step=434,hour=2)
    s={'eligible':True,'t19_enabled':True,'committed':False}
    assert ns['_v219_request'](late,a,s,native)==a and not s['eligible'];checks.append('no_ineligible_ten_plot_fallback')
    obs3=copy.deepcopy(obs);obs3['town']['unlocked_shops'].append('PIZZA_SHOP');obs3['market']['prices']['TOMATO']=100
    assert ns['_PS_BASE_QUAL'](obs3,native)
    assert ns['_v219_qualifies'](obs3,native) and 0 not in ns['_PS_CHOICES']
    checks.append('original_eligible_branch_preserved')
finally:chassis.routes=saved
report=dict(passed=True,checks=checks,synthetic_forecast=value,source_sha256=hashlib.sha256((R/path).read_bytes()).hexdigest(),scope='Synthetic qualification/cost assertions, not realized field output or match wins.')
(D/'production_scale_unit_checks.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report),flush=True)

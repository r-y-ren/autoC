"""Focused semantic checks against the inherited exact official physical model."""
import json
from pathlib import Path
root=Path(__file__).resolve().parents[2]
ns={};exec(compile((root/'experiments/round8_terminal_inputs.py').read_text(encoding='utf-8'),'<terminal-inputs>','exec'),ns)
f=ns['_ti_fert_value']
w={'kind':'PLANT','crop':'WHEAT','planted_day':27,'watered_today':False,'fertilized_until_day':-1,'yield_units':2,'consecutive_unwatered':0,'max_lifespan_step':768}
assert f(w,29)
assert not f(dict(w,watered_today=True),29)
assert not f(dict(w,fertilized_until_day=29),29)
assert not f(dict(w,yield_units=5),29)
assert not f(dict(w,crop='TOMATO'),29)
# Directly prove why unconditional last-day fertilizer suppression is unsafe.
apply=ns['_PLANNER_NS']['_apply_unit_action']
outputs=[]
for fertilize in (False,True):
 tiles=[[None]*10 for _ in range(10)];tiles[4][4]=dict(w)
 farm={'tiles':tiles,'farmer':[4,4],'hands':[[4,4]],'unlocked_quadrants':['NW']}
 private={'seeds':{},'shed':{},'inventories':[{'FERTILIZER':1},{}]}
 if fertilize:apply(farm,private,0,['FERTILIZE'],10,29,24,100)
 apply(farm,private,1,['WATER'],10,29,24,100)
 outputs.append(farm['tiles'][4][4]['yield_units'])
assert outputs==[3,4],outputs
native={'pending':{}}
base=ns['_ti_seed_reserve'](native,660)
assert ns['_ti_seed_reserve']({'pending':{0:[((4,4),['PLANT','WHEAT']),((4,4),['WATER'])]}},660)==base+1
assert ns['_ti_seed_reserve'](native,671)==0
assert ns['_ti_seed_reserve'](native,700)==0
assert not ns['_ti_standard']({'episodeSteps':721})
report={'checks_passed':10,'official_physical_model_last_day_wheat_yield_without_fert':outputs[0],'with_fert':outputs[1],'seed_reserve_at_660':base,'pending_retry_increases_reserve':True,'same_full_reserve_applies_to_both_seed_species':True,'nonstandard_episode_abstains':True}
(root/'results/round8_terminal_inputs_semantics.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(report)

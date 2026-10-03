"""Synthetic risk-control assertions, separate from strength evaluation."""
from pathlib import Path
import json
C=Path(__file__).resolve().parent
ns={'phase_b_agent':lambda *args:{},'_OR2_STATE':{},'_ADV_ITEMS':('MILK','WOOL'),
    '_OR2_ANIMAL':{'COW':'MILK','SHEEP':'WOOL'}}
exec(compile((C/'risk_tail.py.txt').read_text(),str(C/'risk_tail.py.txt'),'exec'),ns)
farms=[dict(money=3000,tiles=[[None]]),dict(money=1000,tiles=[[None]])]
obs=dict(step=300,player=0,farms=farms,private=dict(shed={},inventories=[{}]),market=dict(prices={'MILK':100,'WOOL':100}))
allow=ns['_d_allow_advance'];checks=[]
assert not allow(obs)
checks.append('cash_lead_with_no_rival_stock_is_conservative')
ns['_OR2_STATE'][0]={'stock':{'MILK':20}}
assert allow(obs)
checks.append('rival_observed_premium_stock_prevents_false_lead')
ns['_D_WEALTH']=False
assert not allow(obs)
checks.append('cash_only_ablation_is_distinct')
obs['step']=10
assert allow(obs)
checks.append('early_production_not_changed_by_risk_gate')
result=dict(passed=True,checks=checks,scope='synthetic mechanism checks only')
(C/'risk_unit_checks.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result),flush=True)

"""Small deterministic checks of the public observer correction, not strength tests."""
from pathlib import Path
import copy,json
B=Path(__file__).resolve().parent; tail=(B/'repair_tail.py.txt').read_text()
def namespace():
 ns={'r2_opening_agent':lambda obs,config=None:{'farmer':['PASS'],'hands':[],'market':[]},
  '_V10_ADV_HORIZON':36,'_OR2_SN_K':4,'_OR2_STATE':{},'_ADV_ITEMS':('STRAWBERRY','MILK'),
  '_OR2_ONGOING':('STRAWBERRY','TOMATO'),'_r37_similarity':lambda obs:obs['test_similarity']}
 exec(compile(tail,'repair_tail.py.txt','exec'),ns); return ns
checks=[]
for label,step,current,expiry,expected in [('expired_partial',13,1,10,1),
 ('not_expired',13,1,20,2),('wrong_parity',12,1,10,2),('full_harvest',13,0,10,2),
 ('midnight_ambiguous',24,1,10,2)]:
 ns=namespace();ns['_B_DECAY']=True
 tile={'kind':'PLANT','crop':'STRAWBERRY','planted_day':0,'yield_units':current,'max_lifespan_step':expiry}
 obs={'step':step,'player':0,'farms':[{}, {'tiles':[[tile]]}],'test_similarity':1.0}
 ns['_OR2_STATE'][0]={'prev':{'step':step-1,'tiles':{(0,0):('P','STRAWBERRY',0,2)},'prices':{}},'stock':{}}
 before=copy.deepcopy(obs);ns['phase_b_agent'](obs)
 assert obs==before
 assert ns['_OR2_STATE'][0]['prev']['tiles'][(0,0)][3]==expected,label
 checks.append(label)
ns=namespace();ns['_B_FLOOR']=True;ns['_B_SIM_GATE']=.95
ns['_OR2_STATE'][0]={'prev':{'step':11,'prices':{'MILK':1}},'stock':{'MILK':7}}
obs={'step':12,'player':0,'farms':[{},{}],'test_similarity':.8}
ns['phase_b_agent'](obs);assert ns['_OR2_STATE'][0]['stock']['MILK']==0
assert (ns['_OR2_SN_K'],ns['_V10_ADV_HORIZON'])==(0,12)
obs['test_similarity']=1.0;ns['phase_b_agent'](obs)
assert (ns['_OR2_SN_K'],ns['_V10_ADV_HORIZON'])==(4,36)
checks.extend(['floor_uncertainty','dissimilar_conservative','similar_aggressive'])
(B/'unit_checks.json').write_text(json.dumps({'passed':True,'checks':checks,'scope':'local mechanism assertions only'},indent=2),encoding='utf-8')
print('PASSED',len(checks),'local mechanism assertions')

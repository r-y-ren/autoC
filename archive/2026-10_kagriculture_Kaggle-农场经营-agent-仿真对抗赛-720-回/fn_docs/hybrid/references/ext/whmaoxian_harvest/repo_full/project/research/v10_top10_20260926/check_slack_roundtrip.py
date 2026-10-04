"""Check restoration and deadline contracts in a synthetic idle interval."""
from pathlib import Path
import copy,json,sys
D=Path(__file__).resolve().parent;R=D.parents[1]
sys.path.insert(0,str(R/'research/v10_rebuild_20260926'))
import fast_arena as a
fn=a.load('research/v10_top10_20260926/slack_roundtrip/farmer_care1.py');ns=fn.__globals__
s,env=a.new_game(0);obs=copy.deepcopy(s[0].observation)
obs.update(step=300,day=12,hour=12);obs['farms'][0]['farmer']=[4,4];obs['farms'][0]['hands']=[]
obs['farms'][0]['tiles'][3][4]={'kind':'PASTURE','animal':'COW','placed_day':0,'fed_today':True,'cared_today':False,'yield_units':0,'pending_care_bonus':0}
tape=[{'farmer':['PASS'],'hands':[],'market':[]} for _ in range(719)];tape[303]={'farmer':['NORTH'],'hands':[],'market':[]}
ns['_IMPL'].chassis.routes={0:tape,1:tape,2:tape};ns['_IMPL'].chassis.players={0:{'route':0}}
ns['_V219_STATES'].clear()
def parent(view,config=None):
    assert view['farms'][0]['farmer']==[4,4],'Parent did not receive its reserved anchor position'
    return copy.deepcopy(tape[int(view['step'])])
ns['_SD_PARENT']=parent
expected=['NORTH','CARE','SOUTH','NORTH'];actual=[]
for step in range(300,304):
    obs.update(step=step,hour=step%24)
    act=fn(obs,env.configuration);command=act['farmer'][0];actual.append(command)
    if command in ns['_SD_MOVES']:
        dx,dy=ns['_SD_MOVES'][command];pos=obs['farms'][0]['farmer'];pos[0]+=dx;pos[1]+=dy
    elif command=='CARE':obs['farms'][0]['tiles'][3][4]['cared_today']=True
assert actual==expected,actual
assert ns['_SD_REPORT']['contract_errors']==0
ns['_SD_STATE'].clear();obs.update(step=300,hour=12);obs['farms'][0]['farmer']=[4,4]
obs['farms'][0]['tiles'][3][4]['cared_today']=False
tape[301]={'farmer':['NORTH'],'hands':[],'market':[]}
assert fn(obs,env.configuration)['farmer']==['PASS']
report=dict(passed=True,checks=['three_step_trip_restores_anchor_before_original_task','parent_reserved_position_preserved','insufficient_idle_window_declined'],scope='Synthetic unit contracts, not full-game performance.')
(D/'slack_roundtrip_unit_checks.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report),flush=True)

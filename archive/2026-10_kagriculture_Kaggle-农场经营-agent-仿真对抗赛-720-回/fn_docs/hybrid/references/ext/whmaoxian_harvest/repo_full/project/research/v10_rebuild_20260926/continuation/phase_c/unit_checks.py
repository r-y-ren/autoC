"""Mechanism-only assertions using synthetic PUBLIC observations."""
from pathlib import Path
import json
C=Path(__file__).resolve().parent
namespace={'phase_b_agent':lambda *args: {},'_OR2_ANIMAL':{'COW':'MILK','SHEEP':'WOOL','GOOSE':'EGG'},'_OR2_ONGOING':('TOMATO','STRAWBERRY')}
exec(compile((C/'readiness_tail.py.txt').read_text(),str(C/'readiness_tail.py.txt'),'exec'),namespace)
observe=namespace['_c_observe'];ready=namespace['_c_ready']
def observation(step,position,yield_units=None):
    tiles=[[None for _ in range(10)] for _ in range(10)]
    if yield_units is not None:
        tiles[0][0]=dict(kind='PLANT',crop='STRAWBERRY',planted_day=0,yield_units=yield_units)
    public=dict(farmer=position,hands=[],tiles=tiles)
    return dict(step=step,player=0,farms=[public,public])
checks=[]
observe(observation(240,[0,0],4))
obs=observation(241,[0,0],0);observe(obs)
assert ready(obs,'STRAWBERRY',4)==0
checks.append('remote_harvest_not_immediately_sellable')
obs=observation(242,[4,4],0);observe(obs)
assert ready(obs,'STRAWBERRY',4)==4
checks.append('shed_arrival_can_be_sold_same_turn')
observe(observation(243,[4,4],0))
assert not namespace['_C_STATE'][0]['cargo']
checks.append('possible_shed_drop_clears_cargo_constraint')
observe(observation(244,[0,0],3));observe(observation(245,[0,0],0))
assert ready(observation(245,[0,0]),'STRAWBERRY',3)==0
observe(observation(264,[0,0],0))
assert not namespace['_C_STATE'][0]['cargo']
checks.append('midnight_and_nonconsecutive_reset')
assert 'private' not in obs and 'configuration' not in obs
checks.append('no_private_opponent_or_future_state_required')
result=dict(passed=True,checks=checks,scope='synthetic local assertions, not win-rate evidence')
(C/'unit_checks.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result),flush=True)

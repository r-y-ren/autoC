import os, sys, json, itertools
from pathlib import Path
import numpy as np

ROOT = Path('/mnt/e/_work/kaggriculture3')
WT = ROOT / '.claude/worktrees/ship-pair'
os.chdir(WT)
sys.path[:0] = [str(WT/'src'), str(WT/'tests'), str(WT/'scripts')]
from kagg3 import spec
from kagg3.core import plan as P, ops as O, budget as B, projector as PJ
from test_budget_order import _macro
from test_land_value import _board, _wheat
from test_day_stats import _more_harvests_than_the_route_can_reach
from test_admit_route import _farm, _ripe

captures = []
def trace(frame, event, arg):
    if event == 'return' and frame.f_code.co_filename == P.__file__ and frame.f_code.co_name in ('_derive', '_plan_and_stats'):
        captures.append((frame.f_code.co_name, dict(frame.f_locals)))

def build(view, macro, table=None):
    captures.clear()
    sys.setprofile(trace)
    try: out = P.build_day(np, view, macro, table)
    finally: sys.setprofile(None)
    derives = [v for n,v in captures if n == '_derive']
    end = [v for n,v in captures if n == '_plan_and_stats'][-1]
    return out, derives, end

results = {}
# A full planner decision: land affordability is not subtraction from utility.
v = _board(day=27)
m = _macro(plant_target=_wheat(26))
out, ds, end = build(v,m)
d = ds[-1]
results['land'] = {k:int(d[k]) for k in ['land_cost','land_gap','land_value','buy_land','n_free','money']}
results['land']['bias'] = int(m.land_bias)
results['land']['seed_buy'] = d['seed_buy'].tolist()
results['land']['gain_net_land'] = int(d['land_value']-d['land_cost'])

# Positive gross value, negative net value: keeping cash is feasible.
values = np.zeros((B.N_LISTS,PJ.K),np.int32)
costs = np.ones_like(values)
wants = np.zeros(B.N_LISTS,np.int32)
values[B.L_SEED0+4,0] = 6
costs[B.L_SEED0+4,0] = 80
wants[B.L_SEED0+4] = 1
grant = B.grant(np,values,costs,wants,np.int32(80))
results['negative_net_purchase'] = {'grant':grant.tolist(),'value':6,'cost':80,'net':-74}
table = P.default_price_table()
floor_inv = np.full(9,spec.MARKET_I0,np.int32)
floor_inv[1] = np.flatnonzero(table[1] == 1)[0] + spec.PRICE_TABLE_LO
prices = table[np.arange(9),floor_inv-spec.PRICE_TABLE_LO]
v = _board(day=10,money=1000)._replace(nquad=np.int32(4),
    kind=np.full(100,spec.KIND_EMPTY,np.int32),price=prices,mkt_inv=floor_inv)
out,ds,e = build(v,_macro(plant_target=np.array([0,1,0,0,0],np.int32)))
results['negative_net_full_plan'] = {'carrot_seed_bought':int(ds[-1]['seed_buy'][1]),
    'candidate_value':int(ds[-1]['values'][B.L_SEED0+1,0]),
    'candidate_cost':int(ds[-1]['costs'][B.L_SEED0+1,0]),
    'plant_ops':int(np.sum(out[0]==O.OP_PLANT))}

# Adapt the existing test to respect the engine's four-unit strawberry cap.
# Expired fertilizer dates permit the corresponding accumulated yields.
v = _farm({4:_ripe(spec.I_STRAWBERRY,1),9:_ripe(spec.I_STRAWBERRY,3),
           91:_ripe(spec.I_STRAWBERRY,3),99:_ripe(spec.I_STRAWBERRY,4)})
fert_dates = v.t_fert.copy()
fert_dates[[9,91]],fert_dates[99] = 9,11
v = v._replace(t_fert=fert_dates)
out, ds, e = build(v,_macro())
work = ds[-1]
tiles = np.flatnonzero(work['n_ops'])
best=(-1,None,0)
for n in range(1,len(tiles)+1):
    for order in itertools.permutations(tiles,n):
        x,y=int(P.SPAWN_X[0]),int(P.SPAWN_Y[0]); turns=0; value=0
        for tile in order:
            nx,ny=int(P.SERP_X[tile]),int(P.SERP_Y[tile])
            turns += abs(nx-x)+abs(ny-y)+int(work['n_ops'][tile])
            value += int(work['tile_value'][tile]);x,y=nx,ny
        if turns <= 23 and value > best[0]:best=(value,list(map(int,order)),turns)
results['route'] = {'queued':int(work['tile_value'].sum()),'covered_tiles':np.flatnonzero(e['covered']).tolist(),
                    'covered_value':int(work['tile_value'][e['covered']].sum()),'brute_force_value':best[0],
                    'brute_force_order':best[1],'brute_force_route_turns':best[2], 'cash':int(v.money)}
round_results={}
original=P.ADMIT_ROUNDS
for rounds in [1,2,3,4,5]:
    P.ADMIT_ROUNDS=rounds
    _,ds,e=build(v,_macro())
    round_results[rounds]={'covered':np.flatnonzero(e['covered']).tolist(),'value':int(ds[-1]['tile_value'][e['covered']].sum())}
P.ADMIT_ROUNDS=original
results['route_rounds']=round_results
tiles = {4:_ripe(spec.I_STRAWBERRY,1),9:_ripe(spec.I_STRAWBERRY,4),
         91:_ripe(spec.I_STRAWBERRY,4),
         99:dict(kind=spec.KIND_PLANT,occ=spec.I_TOMATO,t_day=8,t_yield=0,t_cons=1)}
v=_farm(tiles)
fert_dates=v.t_fert.copy();fert_dates[[9,91]]=11
out,ds,e=build(v._replace(t_fert=fert_dates),_macro())
results['mandatory_missed']={'survival_tile':99,'tier':int(ds[-1]['tier'][99]),
    'admitted':bool(e['admitted'][99]),'covered':bool(e['covered'][99]),
    'covered_tiles':np.flatnonzero(e['covered']).tolist(),
    'turns_to_reach_and_water':int(abs(P.SPAWN_X[0]-P.SERP_X[99])+abs(P.SPAWN_Y[0]-P.SERP_Y[99])+1)}
v=_farm({i:dict(kind=spec.KIND_PLANT,occ=spec.I_MELON,t_day=0,t_yield=1)
         for i in range(100)},day=3)._replace(money=np.int32(10000))
results['future_hiring']={}
for horizon in [0,3,6]:
    out,ds,e=build(v,_macro(forward_days=np.int32(horizon)))
    h=int((out[3]==O.MO_HIRE).sum())
    results['future_hiring'][horizon]={'hires':h,'wages':int(spec.HIRE_COST[:h].sum()),
                                     'nonpass_unit_actions':int((out[0]!=O.OP_PASS).sum())}
Path('/tmp/kagg3-planner-review/probes.json').write_text(json.dumps(results,indent=2))
print(json.dumps(results,indent=2))

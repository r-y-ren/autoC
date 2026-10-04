"""Official-engine functional checks, explicitly not leaderboard evaluations.

The only environment change is the supported townCenterSellInterval=12 setting.
It supplies a reproducible sufficiently-demanding tomato market; the candidate's
investment gate, competing 19-plant supply assumption and worker costs are intact.
"""
import contextlib
import io
import json
import gzip
import argparse
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
with contextlib.redirect_stdout(io.StringIO()):
    from kaggle_environments import make
    from kaggle_environments.agent import get_last_callable
    from kaggle_environments.envs.kaggriculture import kaggriculture as engine
parser=argparse.ArgumentParser()
parser.add_argument('--source',default='experiments/round8_production_lean.py')
parser.add_argument('--seeds',type=int,nargs='+',default=[688041503])
args=parser.parse_args()
rows=[]
original_market=engine._process_market
original_commit=engine._commit_unit
original_drop=engine._drop_inventories_to_shed
trace={}
farm_seats={};private_seats={}
def market_audit(state,env):
    farm_seats.clear();private_seats.clear()
    for p,f in enumerate(state[0].observation.farms):farm_seats[id(f)]=p
    for p,s in enumerate(state):private_seats[id(s.observation.private)]=p
    return original_market(state,env)
def commit_audit(op,item,price,farm,private,market,shed_capacity=100):
    ok=original_commit(op,item,price,farm,private,market,shed_capacity)
    p=farm_seats.get(id(farm))
    if ok and p is not None and op=='SELL' and item=='TOMATO':
        trace[p]['sold']+=1;trace[p]['revenue']+=price
    return ok
def drop_audit(private,capacity):
    before=private['shed'].get('TOMATO',0)+sum(inv.get('TOMATO',0) for inv in private['inventories'])
    result=original_drop(private,capacity)
    p=private_seats.get(id(private))
    if p is not None:trace[p]['tomatoes_discarded']+=before-private['shed'].get('TOMATO',0)
    return result
engine._process_market=market_audit;engine._commit_unit=commit_audit;engine._drop_inventories_to_shed=drop_audit
for seed in args.seeds:
    trace.clear();trace.update({p:dict(sold=0,revenue=0,tomatoes_discarded=0) for p in (0,1)})
    source=ROOT/args.source
    agent=get_last_callable(source.read_text(encoding='utf-8'),path=str(source))
    env=make('kaggriculture',configuration={'seed':seed,'episodeSteps':720,'townCenterSellInterval':12},debug=True)
    env.run([agent,str(ROOT/'submissions/release_v7/main.py')])
    g=env.toJSON()
    path=ROOT/f'results/{source.stem}_function-seed{seed}.json.gz'
    path.write_bytes(gzip.compress(json.dumps(g).encode()))
    ns=agent.__globals__
    st=ns['_V219_STATES'][0]
    row={'kind':'modified_configuration_functional_check_not_rating_evidence',
         'configuration_override':{'townCenterSellInterval':12},'seed':seed,
         'rewards':[s.reward for s in env.steps[-1]],'telemetry':dict(agent.telemetry),
         'state':{k:v for k,v in st.items() if k in ('t19_enabled','t19_forecast_value','t19_forecast_extra_labor','committed')},
         'replay':str(path.relative_to(ROOT)), 'daily':[]}
    row['actual_tomato_market_and_storage']={p:dict(v) for p,v in trace.items()}
    for day in range(18,30):
        waters=set();fert=set();plants=set();harvest=0;hire_spend=0;hire_count=0
        for t in range(day*24,min(719,(day+1)*24)):
            obs=g['steps'][t][0]['observation'];farm=obs['farms'][0]
            action=g['steps'][t+1][0]['action'];positions=[farm['farmer'],*farm['hands']]
            h=farm['hires_today']
            for order in action['market']:
                if order==['HIRE']:
                    hire_spend+=ns['_v219_fib'](h);h+=1;hire_count+=1
            for actor,cmd in enumerate([action['farmer'],*action['hands']]):
                if actor>=len(positions):continue
                x,y=positions[actor];tile=farm['tiles'][y][x]
                if cmd==['PLANT','TOMATO'] and tile is None:plants.add((x,y))
                if not(isinstance(tile,dict) and tile.get('crop')=='TOMATO'):continue
                if cmd==['WATER'] and not tile['watered_today']:waters.add((x,y))
                if cmd==['FERTILIZE'] and obs['private']['inventories'][actor].get('FERTILIZER',0):fert.add((x,y))
                if cmd==['HARVEST']:harvest+=tile.get('yield_units',0)
        after=g['steps'][min(719,(day+1)*24)][0]['observation']
        live=[tile for r in after['farms'][0]['tiles'] for tile in r if isinstance(tile,dict) and tile.get('crop')=='TOMATO']
        row['daily'].append(dict(day=day,plants=len(plants),watered=len(waters),fertilized=len(fert),harvested=harvest,
                                 live_tomatoes=len(live),held_tomatoes=sum(t['yield_units'] for t in live),
                                 shed_tomatoes=after['private']['shed'].get('TOMATO',0),
                                 hire_count=hire_count,hire_spend=hire_spend))
    final=g['steps'][-1][0]['observation']['private']
    row['final_shed_tomatoes']=final['shed'].get('TOMATO',0)
    row['final_carried_tomatoes']=sum(i.get('TOMATO',0) for i in final['inventories'])
    row['harvested_tomatoes']=sum(d['harvested'] for d in row['daily'])
    rows.append(row)
    print(json.dumps(row),flush=True)
(ROOT/('results/'+Path(args.source).stem+'_function_summary.json')).write_text(json.dumps(rows,indent=2),encoding='utf-8')

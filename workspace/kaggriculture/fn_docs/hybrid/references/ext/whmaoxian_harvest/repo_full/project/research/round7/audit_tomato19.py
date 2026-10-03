"""Check the bounded tomato experiment's persistent entry and production."""
import contextlib
import argparse
import copy
import io
import json
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
parser=argparse.ArgumentParser()
parser.add_argument('--source',default='experiments/round7_tomato19.py')
parser.add_argument('--prefix',default='round7_tomato19')
parser.add_argument('--output',default='research/round7/tomato19_audit.json')
args=parser.parse_args()
with contextlib.redirect_stdout(io.StringIO()):
    from kaggle_environments.agent import get_last_callable

reports=[]
for replay_path in sorted((ROOT/'results').glob(args.prefix+'-seed*-seat*-replay.json')):
    seat=int(replay_path.stem.split('-seat')[1].split('-')[0])
    g=json.loads(replay_path.read_text())
    source=ROOT/args.source
    agent=get_last_callable(source.read_text(),path=str(source))
    differences=[]
    for t in range(719):
        obs=copy.deepcopy(g['steps'][t][seat]['observation'])
        obs['step']=t
        action=agent(obs,g['configuration'])
        if action!=g['steps'][t+1][seat]['action']:differences.append(t)
    ns=agent.__globals__
    error_counters={}
    for name,value in ns.items():
        if isinstance(value,dict) and name.endswith('REPORT'):
            errors={k:v for k,v in value.items() if isinstance(v,(int,float)) and v>0 and ('error' in k.lower() or 'shortfall' in k.lower())}
            if errors:error_counters[name]=errors
    diagnostics=dict(ns['_IMPL'].chassis.diagnostics)
    production=[]
    for p in (0,1):
        counts=[]
        for day in range(18,30):
            ts=range(day*24,min((day+1)*24,719))
            harvested=0
            watered=set();fertilized=set();planted=set()
            for t in ts:
                obs=g['steps'][t][p]['observation'];farm=obs['farms'][p]
                positions=[farm['farmer'],*farm['hands']]
                a=g['steps'][t+1][p]['action']
                for i,cmd in enumerate([a['farmer'],*a['hands']]):
                    if i>=len(positions):continue
                    x,y=positions[i];tile=farm['tiles'][y][x]
                    if cmd==['PLANT','TOMATO']:planted.add((x,y))
                    if isinstance(tile,dict) and tile.get('crop')=='TOMATO':
                        if cmd==['HARVEST']:harvested+=tile.get('yield_units',0)
                        if cmd==['WATER']:watered.add((x,y))
                        if cmd==['FERTILIZE']:fertilized.add((x,y))
            counts.append({'day':day,'planted':len(planted),'watered':len(watered),'fertilized':len(fertilized),'harvested_units':harvested})
        last=g['steps'][-1][p]['observation']
        remaining=sum(tile.get('yield_units',0) for row in last['farms'][p]['tiles'] for tile in row if isinstance(tile,dict) and tile.get('crop')=='TOMATO')
        production.append({'seat':p,'daily':counts,'final_unharvested_tomato':remaining,'final_seeds':last['private']['seeds']})
    assert not differences,differences
    reports.append({'candidate_seat':seat,'seed':g['info']['seed'],'matching_actions':719,'telemetry':dict(agent.telemetry),
                    'nonzero_error_or_shortfall_counters':error_counters,'base_diagnostics':diagnostics,
                    'tomato_state':{k:v for k,v in ns['_V219_STATES'][seat].items() if k in ('t19_enabled','t19_forecast_value','t19_forecast_extra_labor','requested_day','committed')},
                    'production':production})
(ROOT/args.output).write_text(json.dumps(reports,indent=2),encoding='utf-8')
for report in reports:
    print(report['candidate_seat'],report['telemetry'],report['nonzero_error_or_shortfall_counters'])
    for p in report['production']:
        print(p['seat'],'harvested',sum(x['harvested_units'] for x in p['daily']),'unharvested',p['final_unharvested_tomato'])

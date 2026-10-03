"""Five predeclared development matches; no independent-confirmation inputs."""
import contextlib,copy,gc,gzip,hashlib,io,json,runpy,time
from collections import Counter
from pathlib import Path
with contextlib.redirect_stdout(io.StringIO()):
    from kaggle_environments import make
    from kaggle_environments.agent import get_last_callable
    from kaggle_environments.envs.kaggriculture import kaggriculture as engine
ROOT=Path(__file__).parent
OUT=ROOT/'research/round8/top2'
manifest=json.loads((OUT/'contract_build.json').read_text())
candidate=ROOT/manifest['candidate']
assert hashlib.sha256(candidate.read_bytes()).hexdigest()==manifest['candidate_sha256']
old_stats=json.loads((ROOT/'research/round8/dsm_candidate_diagnostics/summary.json').read_text())
baselines={ (r['seed'],r['seat'],r['opponent']):r['delta'] for r in old_stats }
baselines[(82003,1,'submissions/release_v7/main.py')]=6597
baselines[(82005,0,'submissions/release_v7/main.py')]=9309
rows=[]
original_refresh=engine._daily_refresh_plants
context={}
def refresh(farm,*args):
    endangered={(x,y):t['crop'] for y,row in enumerate(farm['tiles']) for x,t in enumerate(row)
                if isinstance(t,dict) and t.get('kind')=='PLANT' and not t.get('watered_today') and t.get('consecutive_unwatered',0)>=1}
    result=original_refresh(farm,*args)
    if id(farm)==context.get('farm'):
        for (x,y),crop in endangered.items():
            if isinstance(farm['tiles'][y][x],dict) and farm['tiles'][y][x].get('kind')=='WEED':
                context['deaths'][crop]+=1
    return result
engine._daily_refresh_plants=refresh
for job in manifest['jobs']:
    started=time.perf_counter();seed,seat=job['seed'],job['seat']
    ns=runpy.run_path(str(candidate));entry=ns['agent'];events=[];understaffed=0
    guard=ns['_r8_contract']
    def audit_guard(obs,config,action):
        global understaffed
        before=copy.deepcopy(action)
        after=guard(obs,config,action)
        assert before.get('farmer')==after.get('farmer') and before.get('hands')==after.get('hands')
        assert Counter(map(lambda x:json.dumps(x,sort_keys=True),before['market']))==Counter(map(lambda x:json.dumps(x,sort_keys=True),after['market']))
        nonsell=lambda a:[x for x in a['market'] if not x or x[0]!='SELL']
        assert nonsell(before)==nonsell(after) and len(after['market'])<=10
        route=ns['_R8_IMPL'].players[seat]['route'];step=obs['step'];farm=obs['farms'][seat]
        missing=max(0,len(ns['_R8_ROUTES'][route][step].get('hands',[]))-len(farm['hands']))
        understaffed+=missing
        if before!=after:
            f=copy.deepcopy(farm);p=copy.deepcopy(obs['private'])
            units=[after.get('farmer') or ['PASS'],*(after.get('hands') or [])]
            demand=Counter(c[1] for c in units if len(c)>1 and c[0]=='PLANT')
            blocked={c for c,n in demand.items() if n>p['seeds'].get(c,0)}
            for actor,command in enumerate(units):
                if len(command)>1 and command[0]=='PLANT' and command[1] in blocked:command=['PASS']
                engine._apply_unit_action(f,p,actor,command,10,step//24,24,100)
            projected=ns['_R8_IMPL']._projected_shed(after,ns['_View'](obs,seat,ns['_R8_IMPL'].cfg))
            # Validate every product used by the changed sale prefix against
            # actual official unit execution, before either player's market.
            available=dict(p['shed'])
            for order in after['market']:
                if not order or order[0]!='SELL':break
                assert available.get(order[1],0)>=order[2],(step,order,available)
                available[order[1]]-=order[2]
            events.append({'step':step,'money_before':farm['money'],'hands_before':len(farm['hands']),
                           'hire_requests':sum(o==['HIRE'] for o in before['market']),
                           'before':before['market'],'after':after['market'],
                           'post_unit_shed':dict(p['shed']),'projection_exact':projected==p['shed']})
        return after
    entry.__globals__['_r8_contract']=audit_guard
    env=make('kaggriculture',configuration={'seed':seed,'episodeSteps':720},debug=True)
    initial_interpreter=env.interpreter;context.clear();context['deaths']=Counter()
    def interpreter(state,game):
        if getattr(state[0].observation,'farms',None):
            context['farm']=id(state[0].observation.farms[seat])
            before=len(state[0].observation.farms[seat]['hands'])
            step=state[0].observation['step']
        else:before=0;step=-1
        result=initial_interpreter(state,game)
        if events and events[-1]['step']==step:
            events[-1]['hands_after']=len(state[0].observation.farms[seat]['hands'])
            events[-1]['hire_successes']=events[-1]['hands_after']-before
        return result
    env.interpreter=interpreter
    opp=get_last_callable((ROOT/job['opponent']).read_text(encoding='utf-8'),path=str(ROOT/job['opponent']))
    entries=[entry,opp]
    if seat:entries.reverse()
    env.run(entries)
    rewards=[s.reward for s in env.steps[-1]];delta=rewards[seat]-rewards[1-seat]
    statuses=[s.status for s in env.steps[-1]]
    stderr=[v.get('stderr') for logs in env.logs for v in logs if v.get('stderr')]
    old=baselines[(seed,seat,job['opponent'])]
    telemetry={k:dict(getattr(entry,k,{})) for k in ('telemetry','routing_telemetry','contract_telemetry')}
    row={**job,'candidate_sha256':manifest['candidate_sha256'],'rewards':rewards,
         'baseline_delta':old,'delta':delta,'delta_improvement':delta-old,'statuses':statuses,
         'stderr':stderr,'telemetry':telemetry,'crop_deaths':dict(context['deaths']),
         'missing_worker_command_turns':understaffed,'cash_repair_events':events,
         'seconds':time.perf_counter()-started}
    rows.append(row);(OUT/'contract_screen.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
    print(json.dumps(row),flush=True)
    assert statuses==['DONE','DONE'] and len(env.steps)==720 and not stderr
    assert not any(entry.telemetry.values())
    del env,entry,ns,opp,entries
    gc.collect()

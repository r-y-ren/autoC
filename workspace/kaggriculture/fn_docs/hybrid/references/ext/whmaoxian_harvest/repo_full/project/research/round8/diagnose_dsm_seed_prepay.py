"""Small saved-action counterfactuals, not complete policy matches or a candidate.

Move the one already-planned strawberry purchase earlier within the same day.
The explicit step numbers are diagnostic interventions, never agent logic.
"""
import contextlib,copy,gzip,io,json,sys
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
with contextlib.redirect_stdout(io.StringIO()):
    from kaggle_environments import make
    from kaggle_environments.envs.kaggriculture import kaggriculture as engine
SOURCE=ROOT/'research/round8/dsm_candidate_diagnostics'
original_apply=engine._apply_unit_action;context={}
def apply(farm,private,actor,command,*args):
    watch=id(farm)==context.get('farm') and actor<len(private['inventories'])
    if watch:
        pos=farm['farmer'] if actor==0 else farm['hands'][actor-1];x,y=pos
        before=(copy.deepcopy(farm['tiles'][y][x]),dict(private['inventories'][actor]),dict(private['shed']),dict(private['seeds']))
    result=original_apply(farm,private,actor,command,*args)
    if watch and command and command[0] not in ('NORTH','SOUTH','EAST','WEST','PASS'):
        after=(farm['tiles'][y][x],private['inventories'][actor],private['shed'],private['seeds'])
        context['units'].append({'step':context['step'],'actor':actor,'pos':list(pos),'command':list(command),
                                 'effective':before!=after,
                                 'inventory_before':before[1],'inventory_after':dict(private['inventories'][actor])})
    return result
engine._apply_unit_action=apply
reports=[]
for filename,seed in [('seed733556107-seat0-fieldcraft.json.gz',733556107),
                      ('seed733556107-seat0-master2965.json.gz',733556107),
                      ('seed800459488-seat0-release_v6.json.gz',800459488)]:
    replay=json.loads(gzip.decompress((SOURCE/filename).read_bytes()))
    variants={}
    for label in ('baseline','prepay_at_175','earliest_existing_fertilizer_sales'):
        env=make('kaggriculture',configuration={'seed':seed,'episodeSteps':720},debug=True)
        units=[];brief=[];states={};blocked=[];advanced_by_day=Counter()
        original_interpreter=env.interpreter
        def interpreter(state,game):
            if getattr(state[0].observation,'farms',None):
                context.update(farm=id(state[0].observation.farms[0]),
                               step=state[0].observation['step'],units=units)
            return original_interpreter(state,game)
        env.interpreter=interpreter
        for step in range(216):
            actions=[copy.deepcopy(replay['steps'][step+1][p]['action']) for p in (0,1)]
            if label=='prepay_at_175':
                if step==175:actions[0]['market'].append(['BUY_SEED','STRAWBERRY',1])
                if step==182:
                    actions[0]['market']=[[] if o==['BUY_SEED','STRAWBERRY',1] else o for o in actions[0]['market']]
            obs=env.state[0].observation;before=json.loads(json.dumps(obs))
            if label=='earliest_existing_fertilizer_sales' and 144<=step<192:
                # Diagnostic comparison: sell each day's SAME planned
                # fertilizer total as soon as physical delivery permits.
                f=copy.deepcopy(obs.farms[0]);p=copy.deepcopy(obs.private)
                unit_commands=[actions[0]['farmer'],*actions[0]['hands']]
                demand=Counter(c[1] for c in unit_commands if len(c)>1 and c[0]=='PLANT')
                blocked_crops={c for c,n in demand.items() if n>p['seeds'].get(c,0)}
                for actor,command in enumerate(unit_commands):
                    if len(command)>1 and command[0]=='PLANT' and command[1] in blocked_crops:command=['PASS']
                    original_apply(f,p,actor,command,10,step//24,24,100)
                day=step//24
                total=sum(o[2] for t in range(day*24,(day+1)*24)
                          for o in replay['steps'][t+1][0]['action']['market']
                          if len(o)>2 and o[:2]==['SELL','FERTILIZER'])
                actions[0]['market']=[[] if o[:2]==['SELL','FERTILIZER'] else o for o in actions[0]['market']]
                qty=min(p['shed'].get('FERTILIZER',0),total-advanced_by_day[day])
                if qty>0:
                    if [] in actions[0]['market']:
                        actions[0]['market'][actions[0]['market'].index([])]=['SELL','FERTILIZER',qty]
                    elif len(actions[0]['market'])<10:
                        actions[0]['market'].append(['SELL','FERTILIZER',qty])
                    else:qty=0
                    advanced_by_day[day]+=qty
            demand=Counter(c[1] for c in [actions[0]['farmer'],*actions[0]['hands']] if len(c)>1 and c[0]=='PLANT')
            for crop,n in demand.items():
                if n>obs.private['seeds'].get(crop,0):blocked.append({'step':step,'crop':crop,'requested':n,'available':obs.private['seeds'].get(crop,0)})
            env.step(actions)
            after=env.state[0].observation
            if step>=174 and (actions[0]['market'] or step in (186,191,192,215)):
                brief.append({'step':step,'money_before':before['farms'][0]['money'],
                              'money_after':after.farms[0]['money'],'hands_after':len(after.farms[0]['hands']),
                              'shed_after':dict(after.private['shed']),'seeds_after':dict(after.private['seeds']),
                              'market':actions[0]['market']})
            if step in (186,191,215):states[str(step+1)]=json.loads(json.dumps(after))
        assert len(units)>100,'Official interpreter hook must actually observe unit execution'
        variants[label]={'trace':brief,'units':[u for u in units if u['step']>=144],
                         'states':states,'blocked_plants':blocked}
    baseline=variants['baseline'];regressions={}
    for label,variant in variants.items():
        if label=='baseline':continue
        actual={(u['step'],u['actor']):u for u in variant['units']}
        regressions[label]=[{'old':u,'new':actual.get((u['step'],u['actor']))} for u in baseline['units']
                     if u['effective'] and (not actual.get((u['step'],u['actor']),{}).get('effective')
                                           or actual[(u['step'],u['actor'])]['pos']!=u['pos'])]
    result={'source':filename,'seed':seed,'kind':'216-step saved-action counterfactual only; rival actions fixed',
            'intervention':'prepay_at_175 moves planned strawberry1 purchase182 to175; earliest_existing_fertilizer_sales advances only the already-planned fertilizer quantity; all physical commands unchanged',
            'variants':variants,'lost_previously_effective_unit_operations':regressions}
    reports.append(result)
    print(json.dumps({'source':filename,'regressions':regressions,'blocked_before':baseline['blocked_plants'],
                      'blocked_after':{k:v['blocked_plants'] for k,v in variants.items()},
                      'money_at_216':[v['states']['216']['farms'][0]['money'] for v in variants.values()],
                      'seeds_at_216':[v['states']['216']['private']['seeds'] for v in variants.values()]}),flush=True)
(ROOT/'research/round8/top2/seed_prepay_counterfactual.json').write_text(json.dumps(reports,indent=2),encoding='utf-8')

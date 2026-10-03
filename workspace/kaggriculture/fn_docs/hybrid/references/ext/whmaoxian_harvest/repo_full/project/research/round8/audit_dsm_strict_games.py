"""Audit one representative bad/tight outcome per opponent without source edits.

The engine hooks count successful state changes, crop deaths, animal escapes,
sales and storage. They delegate every action unchanged to official functions.
Game rewards must exactly match the frozen league row selected for inspection.
"""
import contextlib
import copy
from collections import Counter
import gzip
import io
import json
import os
import sys
import time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];os.chdir(ROOT);sys.path.insert(0,str(ROOT))
from league_round8 import digest,telemetry
with contextlib.redirect_stdout(io.StringIO()):
    from kaggle_environments import make
    from kaggle_environments.agent import get_last_callable
    from kaggle_environments.envs.kaggriculture import kaggriculture as engine
ledger=ROOT/'results/round8_dsm_candidate_development8.jsonl'
rows=[json.loads(x) for x in ledger.read_text().splitlines()]
assert len(rows)==48,'Finish the declared league before selecting diagnostics.'
jobs=[]
for opponent in sorted({r['opponent'] for r in rows}):
    candidates=[r for r in rows if r['opponent']==opponent and r['valid']]
    jobs.append(min(candidates,key=lambda r:(r['delta'],r['seed'],r['seat'])))
out=ROOT/'research/round8/dsm_candidate_diagnostics';out.mkdir(exist_ok=True)
(out/'selection.json').write_text(json.dumps({'rule':'minimum bank delta per opponent, then seed and seat; diagnostic selection only','jobs':[{k:j[k] for k in ('candidate','candidate_sha256','opponent','opponent_sha256','seed','seat','delta')} for j in jobs]},indent=2),encoding='utf-8')
original_apply=engine._apply_unit_action
original_daily_plants=engine._daily_refresh_plants
original_daily_animals=engine._daily_refresh_animals
original_drop=engine._drop_inventories_to_shed
original_commit=engine._commit_unit
context={};reports=[]
def unit_apply(farm,private,actor,command,*args):
    p=context.get('farms',{}).get(id(farm))
    if p is None:return original_apply(farm,private,actor,command,*args)
    st=context['stats'][p];name=command[0] if command else 'PASS'
    if name=='PASS':st['pass_requests']+=1;return original_apply(farm,private,actor,command,*args)
    if name in ('NORTH','SOUTH','EAST','WEST'):
        st['moves']+=1;return original_apply(farm,private,actor,command,*args)
    st['requests'][name]+=1
    if actor>=len(private['inventories']):
        st['no_state_change'][name]+=1;st['absent_worker_requests']+=1
        return original_apply(farm,private,actor,command,*args)
    pos=farm['farmer'] if actor==0 else farm['hands'][actor-1]
    x,y=pos
    before=(copy.deepcopy(farm['tiles'][y][x]),dict(private['inventories'][actor]),dict(private['shed']),dict(private['seeds']))
    result=original_apply(farm,private,actor,command,*args)
    after=(farm['tiles'][y][x],private['inventories'][actor],private['shed'],private['seeds'])
    if before==after:
        st['no_state_change'][name]+=1
        st['no_state_change_by_day'][str(context['step']//24)+':'+name]+=1
        if len(st['first_no_state_changes'])<20:
            st['first_no_state_changes'].append({'step':context['step'],'actor':actor,'position':list(pos),'command':command,'tile':before[0],'carried':before[1]})
    else:st['state_changing'][name]+=1
    if name=='HARVEST':
        for item,n in after[1].items():st['harvest_units'][item]+=max(0,n-before[1].get(item,0))
    return result
def daily_plants(farm,*args):
    p=context.get('farms',{}).get(id(farm))
    before={(x,y):t['crop'] for y,row in enumerate(farm['tiles']) for x,t in enumerate(row)
            if isinstance(t,dict) and t.get('kind')=='PLANT' and not t.get('watered_today') and t.get('consecutive_unwatered',0)>=1}
    result=original_daily_plants(farm,*args)
    if p is not None:
        for (x,y),crop in before.items():
            if farm['tiles'][y][x].get('kind')=='WEED':context['stats'][p]['crops_lost_unwatered'][crop]+=1
    return result
def daily_animals(farm,*args):
    p=context.get('farms',{}).get(id(farm))
    before={(x,y):t['animal'] for y,row in enumerate(farm['tiles']) for x,t in enumerate(row)
            if isinstance(t,dict) and t.get('animal') and not t.get('fed_today') and t.get('consecutive_unfed',0)>=1}
    result=original_daily_animals(farm,*args)
    if p is not None:
        for (x,y),animal in before.items():
            if not farm['tiles'][y][x].get('animal'):context['stats'][p]['animals_escaped_unfed'][animal]+=1
    return result
def drop_inventory(private,capacity):
    p=context.get('privates',{}).get(id(private))
    before=Counter(private['shed'])
    for inv in private['inventories']:before.update(inv)
    result=original_drop(private,capacity)
    if p is not None:
        for item,n in before.items():context['stats'][p]['midnight_discarded'][item]+=max(0,n-private['shed'].get(item,0))
    return result
def commit_unit(op,item,price,farm,private,*args):
    result=original_commit(op,item,price,farm,private,*args)
    p=context.get('farms',{}).get(id(farm))
    if result and p is not None and op=='SELL':
        context['stats'][p]['sold_units'][item]+=1;context['stats'][p]['sale_revenue'][item]+=price
    return result
engine._apply_unit_action=unit_apply
engine._daily_refresh_plants=daily_plants
engine._daily_refresh_animals=daily_animals
engine._drop_inventories_to_shed=drop_inventory
engine._commit_unit=commit_unit
for j in jobs:
    started=time.perf_counter();sys.modules.pop('mirror_plan',None)
    assert digest(j['candidate'])==j['candidate_sha256'] and digest(j['opponent'])==j['opponent_sha256']
    paths=[j['candidate'],j['opponent']]
    entries=[get_last_callable(Path(p).read_text(encoding='utf-8'),path=str(ROOT/p)) for p in paths]
    ordered=entries[::-1] if j['seat'] else entries
    env=make('kaggriculture',configuration={'seed':j['seed'],'episodeSteps':720},debug=True)
    original_interpreter=env.interpreter
    stats=[dict(requests=Counter(),no_state_change=Counter(),state_changing=Counter(),harvest_units=Counter(),
                crops_lost_unwatered=Counter(),animals_escaped_unfed=Counter(),midnight_discarded=Counter(),
                sold_units=Counter(),sale_revenue=Counter(),pass_requests=0,moves=0,absent_worker_requests=0,
                atomic_seed_blocked=Counter(),no_state_change_by_day=Counter(),first_no_state_changes=[]) for _ in (0,1)]
    def interpreter(state,game):
        if getattr(state[0].observation,'farms',None):
            context.update(step=state[0].observation.get('step',0),stats=stats,
                farms={id(f):p for p,f in enumerate(state[0].observation.farms)},
                privates={id(s.observation.private):p for p,s in enumerate(state)})
            for p,s in enumerate(state):
                act=s.action if isinstance(s.action,dict) else {}
                demand=Counter(c[1] for c in [act.get('farmer') or ['PASS'],*(act.get('hands') or [])] if len(c)>1 and c[0]=='PLANT')
                for crop,n in demand.items():
                    if n>s.observation.private['seeds'].get(crop,0):stats[p]['atomic_seed_blocked'][crop]+=n
        return original_interpreter(state,game)
    env.interpreter=interpreter
    env.run(ordered)
    final=env.steps[-1];s=j['seat'];actual=final[s].reward-final[1-s].reward
    assert actual==j['delta'],(j['seed'],j['delta'],actual)
    entry=entries[0];ns=entry.__globals__
    row={k:j[k] for k in ('candidate','candidate_sha256','opponent','opponent_sha256','seed','seat','delta')}
    row.update(kind='selected_diagnostic_rerun_not_additional_independent_sample',rewards_match=True,
               routing=dict(entry.routing_telemetry),candidate_statistics=stats[s],opponent_statistics=stats[1-s],
               pending_retries=sum(len(q) for q in ns['_R8_IMPL'].players[s]['pending'].values()),
               final_route=ns['_R8_IMPL'].players[s]['route'],runtime_telemetry=telemetry(entry),
               final_shed=dict(final[s].observation.private['shed']),final_carried=list(final[s].observation.private['inventories']),
               seconds=time.perf_counter()-started)
    fields=Counter();unharvested=Counter()
    for tiles in final[s].observation.farms[s]['tiles']:
        for tile in tiles:
            if not isinstance(tile,dict):continue
            name=tile.get('crop') or tile.get('animal') or tile.get('kind');fields[name]+=1
            if tile.get('crop'):unharvested[tile['crop']]+=tile.get('yield_units',0)
            elif tile.get('animal'):unharvested[engine.ANIMALS[tile['animal']]['product']]+=tile.get('yield_units',0)
    row.update(final_field_counts=fields,final_unharvested_units=unharvested)
    filename=f"seed{j['seed']}-seat{s}-"+Path(j['opponent']).parent.name
    (out/(filename+'.json.gz')).write_bytes(gzip.compress(json.dumps(env.toJSON()).encode()))
    reports.append(row)
    (out/'summary.json').write_text(json.dumps(reports,indent=2),encoding='utf-8')
    print(json.dumps({'seed':j['seed'],'opponent':j['opponent'],'delta':actual,'candidate_statistics':{k:v for k,v in stats[s].items() if k!='first_no_state_changes'},'routing':row['routing'],'pending_retries':row['pending_retries']}),flush=True)

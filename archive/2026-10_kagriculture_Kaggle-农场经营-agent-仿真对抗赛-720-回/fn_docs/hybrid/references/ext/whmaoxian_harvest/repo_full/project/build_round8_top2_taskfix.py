"""Repair partial PICKUP completion and live input commitments in DSM task proxy."""
import base64
from collections import Counter
import contextlib
import copy
import gzip
import importlib
import io
import json
from pathlib import Path
import runpy
import zlib

ROOT=Path(__file__).parent
DATA=ROOT/'research/round8/top2'
source=(ROOT/'experiments/round8_top2_dsm_tasks.py').read_text(encoding='utf-8')
ns=runpy.run_path(str(ROOT/'experiments/round8_top2_dsm_tasks.py'))
demos=ns['_R8_DEMOS']
with contextlib.redirect_stdout(io.StringIO()):
    engine=importlib.import_module('kaggle_environments.envs.kaggriculture.kaggriculture')
adjustments=[]
for row in json.loads((DATA/'compiled_index.json').read_text()):
    if row['team']!='DSM':
        continue
    demo=demos[str(row['episode_id'])]
    targets={(t['step'],t['unit']):t for t in demo['tasks'] if t['action'][0]=='PICKUP'}
    game=json.loads(gzip.decompress((DATA/f"{row['episode_id']}.json.gz").read_bytes()))
    seat=row['seat']
    corrected=Counter()
    for step in sorted({t for t,u in targets}):
        obs=game['steps'][step][seat]['observation']
        farm=copy.deepcopy(obs['farms'][seat]); private=copy.deepcopy(obs['private'])
        action=game['steps'][step+1][seat]['action']
        actions=[action['farmer']]+action.get('hands',[])
        demand=Counter(a[1] for a in actions if a and a[0]=='PLANT')
        blocked={crop for crop,n in demand.items() if n>private['seeds'].get(crop,0)}
        for i,op in enumerate(actions):
            if i>=len(private['inventories']):
                continue
            task=targets.get((step,i))
            before=private['inventories'][i].get(op[1],0) if task else None
            actual=['PASS'] if op and op[0]=='PLANT' and op[1] in blocked else op
            engine._apply_unit_action(farm,private,i,actual,10,step//24,24,100)
            if task:
                qty=private['inventories'][i].get(op[1],0)-before
                assert qty>0,(row['episode_id'],step,i,qty)
                old=task['action'][2] if len(task['action'])>2 else 1
                if qty!=old:
                    corrected[op[1]]+=old-qty
                task['action']=['PICKUP',op[1],qty]
    adjustments.append({'episode_id':row['episode_id'],'removed_unexecuted_pickup_quantity':dict(corrected)})
    del game
    print(row['episode_id'],dict(corrected),flush=True)

# Transform the runtime in a new independent source; previous agents stay frozen.
source=source.replace("'seed_deferrals':0}","'seed_deferrals':0,'waits_by_operation':{},'waits_by_day':{},'unfinished_by_operation':{},'unfinished_by_day':{},'partial_pickups':0,'missing_target_skips':0,'input_reserves':0,'input_topups':0}")
source=source.replace("'indices':{},'step':-1}","'indices':{},'pickup_remaining':{},'step':-1}")
source=source.replace("st.update(day=day,route=route,indices={})","st.update(day=day,route=route,indices={},pickup_remaining={})")
needle="self.diagnostics['unfinished_daily_tasks']+=sum(max(0,len(tasks)-st['indices'].get(i,0)) for i,tasks in old.items())"
source=source.replace(needle,needle+"\n                for i,seq in old.items():\n                    for task in seq[st['indices'].get(i,0):]:\n                        name=task['action'][0]; key=str(st['day'])\n                        self.diagnostics['unfinished_by_operation'][name]=self.diagnostics['unfinished_by_operation'].get(name,0)+1\n                        self.diagnostics['unfinished_by_day'][key]=self.diagnostics['unfinished_by_day'].get(key,0)+1")
needle="if already:\n                    idx+=1; self.diagnostics['skipped_tasks']+=1; continue"
source=source.replace(needle,needle+"\n                absent=(name in ('FEED','CARE','COLLECT_FERTILIZER') and not (isinstance(tile,dict) and tile.get('animal'))) or (name in ('WATER','FERTILIZE') and not (isinstance(tile,dict) and tile.get('kind')=='PLANT')) or (name=='HARVEST' and (tile is None or tile=='LOCKED' or (isinstance(tile,dict) and tile.get('kind')=='WEED')))\n                if absent:\n                    idx+=1; self.diagnostics['missing_target_skips']+=1; continue")
needle="qty=min(int(op[2]) if len(op)>2 else 1,shed_budget.get(op[1],0))"
source=source.replace(needle,"goal=st['pickup_remaining'].setdefault((i,idx),int(op[2]) if len(op)>2 else 1)\n                    qty=min(goal,shed_budget.get(op[1],0))")
needle="op=['PICKUP',op[1],qty]; shed_budget[op[1]]-=qty"
source=source.replace(needle,needle+"\n                    st['pickup_remaining'][(i,idx)]-=qty\n                    if st['pickup_remaining'][(i,idx)]>0:\n                        self.diagnostics['partial_pickups']+=1; break")
source=source.replace("st['indices'][i]=idx; actions.append(op)","st['indices'][i]=idx; actions.append(op)\n            if op[0]=='PASS' and idx<len(sequence):\n                name=sequence[idx]['action'][0]; key=str(day)\n                self.diagnostics['waits_by_operation'][name]=self.diagnostics['waits_by_operation'].get(name,0)+1\n                self.diagnostics['waits_by_day'][key]=self.diagnostics['waits_by_day'].get(key,0)+1")
blob=base64.b85encode(zlib.compress(json.dumps(demos,separators=(',',':')).encode(),9)).decode()
source='\n'.join(f"_R8_DEMOS=json.loads(zlib.decompress(base64.b85decode({blob!r})))" if line.startswith('_R8_DEMOS=json.loads(') else line for line in source.splitlines())+'\n'
source+='''
# Modified 2026-09-22: preserve partially fulfilled pickup goals and feed inputs.
# Replay pickup quantities are compiled from actual source-state unit execution.
'''+'''
_R8_TASKS=_R8TaskExecutor(_R8_DEMOS)
_R8_FIX_PARENT=agent

def _r8_guard_inputs(obs,action):
    step=_step_of(obs); p=obs['player']; day=step//24
    state=_R8_TASKS.state[p]
    tasks=_R8_TASKS.by_day[state['route']].get(day,{})
    needs={'WHEAT':0,'FERTILIZER':0}
    for i,seq in tasks.items():
        for task in seq[state['indices'].get(i,0):]:
            name=task['action'][0]
            if name=='FEED': needs['WHEAT']+=1
            if name=='FERTILIZE': needs['FERTILIZER']+=1
    farm=obs['farms'][p]; priv=obs['private']
    view=_View(obs,p,_R8_IMPL.cfg)
    shed=_R8_IMPL._projected_shed(action,view)
    units=[action['farmer']]+action['hands']
    carried={k:sum(inv.get(k,0) for inv in priv['inventories']) for k in needs}
    for i,op in enumerate(units):
        if not op: continue
        if op[0]=='FEED': carried['WHEAT']-=1
        if op[0]=='FERTILIZE': carried['FERTILIZER']-=1
        if op[0]=='PICKUP' and op[1] in carried: carried[op[1]]+=op[2]
        if op[0]=='DROP' and i<len(priv['inventories']):
            for item in carried: carried[item]-=priv['inventories'][i].get(item,0)
    reserve={k:max(0,needs[k]-carried[k]) for k in needs}
    sells={k:max(0,shed.get(k,0)-reserve[k]) for k in needs}
    planned={k:0 for k in needs}
    orders=[]
    for order in action.get('market',[]):
        if order and order[0]=='SELL' and order[1] in sells:
            item=order[1]; qty=min(order[2],sells[item]); sells[item]-=qty
            if qty<order[2]: _R8_TASKS.diagnostics['input_reserves']+=1
            orders.append(['SELL',item,qty] if qty else [])
        else:
            orders.append(order)
        if order and order[0]=='BUY_PRODUCT' and order[1] in planned:
            planned[order[1]]+=order[2]
    # Repair a visible input shortage only after the cash-sensitive opening.
    # Existing purchases are counted; no target is derived from hidden state.
    if 72<=step<696:
        money=farm['money']
        for item in needs:
            qty=min(20,max(0,reserve[item]-shed.get(item,0)-planned[item]))
            cost=max(1,obs['market']['prices'].get(item,1))*3
            qty=min(qty,max(0,int((money-600)//cost)))
            if qty and len(orders)<10:
                orders.append(['BUY_PRODUCT',item,qty]); money-=qty*cost
                _R8_TASKS.diagnostics['input_topups']+=qty
    action['market']=orders
    return action

def round8_top2_dsm_tasks_fixed_agent(obs,config=None):
    return _r8_guard_inputs(obs,_R8_FIX_PARENT(obs,config))

agent=round8_top2_dsm_tasks_fixed_agent
agent.telemetry=_R8_IMPL.diagnostics
agent.routing_telemetry=_R8_ROUTER.diagnostics
agent.task_telemetry=_R8_TASKS.diagnostics
'''
dest=ROOT/'experiments/round8_top2_dsm_tasks_fixed.py'
dest.write_text(source,encoding='utf-8')
(DATA/'pickup_compilation.json').write_text(json.dumps(adjustments,indent=2),encoding='utf-8')
print(dest.name,dest.stat().st_size,flush=True)
# Preserve failed v1 for audit; v2 corrects two diagnosed scheduling mistakes.
start=source.index('                absent=(name in ')
end=source.index('                if pos[0]!=x or pos[1]!=y:',start)
fixed=source[:start]+source[end:]
needle="    step=_step_of(obs); p=obs['player']; day=step//24\n    state=_R8_TASKS.state[p]"
assert needle in fixed
fixed=fixed.replace(needle,"    step=_step_of(obs); p=obs['player']; day=step//24\n    if step<72:\n        return action\n    state=_R8_TASKS.state[p]")
fixed=fixed.replace('round8_top2_dsm_tasks_fixed_agent','round8_top2_dsm_tasks_fixed_v2_agent')
dest2=ROOT/'experiments/round8_top2_dsm_tasks_fixed_v2.py'
dest2.write_text(fixed,encoding='utf-8')
print(dest2.name,dest2.stat().st_size,flush=True)

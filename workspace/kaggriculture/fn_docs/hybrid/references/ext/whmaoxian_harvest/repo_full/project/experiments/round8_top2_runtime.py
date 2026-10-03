"""Observable-state routing and a daily-task interpreter for public demonstrations.

These are local proxies learned from public actions, never the authors' code.
This file is appended to the attributed chassis by build_round8_top2.py.
No exception is converted to PASS here; the evaluator must reject raised errors
and any upstream chassis fallback counter. Intentional waits are counted.
"""


def _r8_field_key(farm):
    # Weather-generated weeds on empty tiles are handled by chassis weed repair;
    # all crop/animal states, including yield, age and fertilizer, must agree.
    tiles=[]
    for row in farm['tiles']:
        tiles.append([None if isinstance(t,dict) and t.get('kind')=='WEED' else t for t in row])
    return json.dumps([tiles, farm['farmer'], farm['hands'], farm['unlocked_quadrants']],sort_keys=True,separators=(',',':'))


def _r8_shop_score(observed,donor):
    a=list(observed); b=list(donor[:len(a)])
    if a==b:
        return 100+len(a)
    # Partial agreement uses only shops already revealed to both observations.
    return sum(x==y for x,y in zip(a,b))


class _R8Router:
    def __init__(self,demos):
        self.demos=demos
        self.keys={rid:{d['step']:_r8_field_key(d['farm']) for d in v['dawn_states']} for rid,v in demos.items()}
        self.diagnostics={'route_switches':0,'compatible_options':0,'incompatible_rejected':0,'state_contract_rejected':0}

    def __call__(self,obs,step,state):
        current=state.setdefault('route',next(iter(self.demos)))
        if step==0:
            state['route']=next(iter(self.demos)); return state['route']
        if step%24 or step<72:
            return current
        player=obs['player']; farm=obs['farms'][player]; private=obs['private']
        key=_r8_field_key(farm)
        visible=obs['town']['unlocked_shops']
        best=current
        bestscore=_r8_shop_score(visible,self.demos[current]['dawn_states'][step//24]['shops'])
        for rid, demo in self.demos.items():
            if self.keys[rid].get(step)!=key:
                self.diagnostics['incompatible_rejected']+=1; continue
            expected=demo['dawn_states'][step//24]['private']
            if private['inventories']!=expected['inventories']:
                self.diagnostics['state_contract_rejected']+=1; continue
            if any(private['seeds'].get(k,0)<v for k,v in expected['seeds'].items()):
                self.diagnostics['state_contract_rejected']+=1; continue
            if any(private['shed'].get(k,0)<expected['shed'].get(k,0) for k in ('WHEAT','FERTILIZER','COW','SHEEP','GOOSE')):
                self.diagnostics['state_contract_rejected']+=1; continue
            self.diagnostics['compatible_options']+=1
            score=_r8_shop_score(visible,demo['dawn_states'][step//24]['shops'])
            if score>bestscore:
                best,bestscore=rid,score
        if best!=current:
            self.diagnostics['route_switches']+=1
        state['route']=best
        return best


class _R8TaskExecutor:
    """Preserve daily per-worker task order, recomputing movement and preconditions.

    Task targets were operations that actually succeeded in an official replay.
    Movement is planned from live positions; completed/idempotent tasks are skipped.
    Purchase/sale control remains with the reactive, source-attributed chassis.
    """
    def __init__(self,demos):
        self.by_day={}
        for rid,demo in demos.items():
            days={}
            for task in demo['tasks']:
                days.setdefault(task['step']//24,{}).setdefault(task['unit'],[]).append(task)
            self.by_day[rid]=days
        self.state={}
        self.diagnostics={'issued_tasks':0,'skipped_tasks':0,'waits':0,'weed_repairs':0,'moves':0,'unfinished_daily_tasks':0,'seed_deferrals':0}

    def act(self,obs,route,action):
        p=obs['player']; step=_step_of(obs); day=step//24
        st=self.state.get(p)
        if st is None or step==0 or step<=st['step']:
            st={'day':day,'route':route,'indices':{},'step':-1}; self.state[p]=st
        if day!=st['day'] or route!=st['route']:
            if day!=st['day']:
                old=self.by_day[st['route']].get(st['day'],{})
                self.diagnostics['unfinished_daily_tasks']+=sum(max(0,len(tasks)-st['indices'].get(i,0)) for i,tasks in old.items())
            st.update(day=day,route=route,indices={})
        st['step']=step
        farm=obs['farms'][p]; priv=obs['private']
        positions=[farm['farmer']]+farm['hands']
        tasks=self.by_day[route].get(day,{})
        seed_budget=dict(priv['seeds']); shed_budget=dict(priv['shed'])
        actions=[]
        for i,pos in enumerate(positions):
            sequence=tasks.get(i,[]); idx=st['indices'].get(i,0)
            inv=priv['inventories'][i]
            while idx<len(sequence):
                task=sequence[idx]; op=list(task['action']); name=op[0]
                x,y=task['position']; tile=farm['tiles'][y][x]
                # Only discard operations whose goal is visibly already satisfied.
                already=(name=='WATER' and isinstance(tile,dict) and tile.get('watered_today')) or (name=='FEED' and isinstance(tile,dict) and tile.get('fed_today')) or (name=='CARE' and isinstance(tile,dict) and tile.get('cared_today')) or (name=='COLLECT_FERTILIZER' and isinstance(tile,dict) and not tile.get('fertilizer_available')) or (name=='HARVEST' and isinstance(tile,dict) and tile.get('yield_units',0)<=0) or (name=='DIG' and tile is None) or (name=='FERTILIZE' and isinstance(tile,dict) and tile.get('fertilized_until_day',-1)>=day+2)
                if already:
                    idx+=1; self.diagnostics['skipped_tasks']+=1; continue
                if pos[0]!=x or pos[1]!=y:
                    op=['EAST' if pos[0]<x else 'WEST'] if pos[0]!=x else ['SOUTH' if pos[1]<y else 'NORTH']
                    self.diagnostics['moves']+=1; break
                if name in ('PLANT','BUILD_COOP','BUILD_PASTURE') and isinstance(tile,dict) and tile.get('kind')=='WEED':
                    op=['DIG']; self.diagnostics['weed_repairs']+=1; break
                if name=='PLANT' and seed_budget.get(op[1],0)<=0:
                    op=['PASS']; self.diagnostics['waits']+=1; self.diagnostics['seed_deferrals']+=1; break
                if _is_noop(op,tile,inv,seed_budget,pos,len(farm['tiles'])):
                    op=['PASS']; self.diagnostics['waits']+=1; break
                if name=='PICKUP':
                    qty=min(int(op[2]) if len(op)>2 else 1,shed_budget.get(op[1],0))
                    if qty<=0:
                        op=['PASS']; self.diagnostics['waits']+=1; break
                    op=['PICKUP',op[1],qty]; shed_budget[op[1]]-=qty
                if name=='PLANT':
                    seed_budget[op[1]]-=1
                idx+=1; self.diagnostics['issued_tasks']+=1; break
            else:
                # Idle delivery helps responsive sales without inventing farm jobs.
                if inv and _shed_adjacent(pos,len(farm['tiles'])):
                    op=['DROP']
                elif inv:
                    tx=min(max(pos[0],4),5); ty=min(max(pos[1],4),5)
                    op=['EAST' if pos[0]<tx else 'WEST'] if pos[0]!=tx else ['SOUTH' if pos[1]<ty else 'NORTH']
                else:
                    op=['PASS']
            st['indices'][i]=idx; actions.append(op)
        action['farmer']=actions[0]; action['hands']=actions[1:]
        return action

"""Two bounded diagnostic variants: event timing preservation and crop recovery."""
from pathlib import Path
ROOT=Path(__file__).parent
base=(ROOT/'experiments/round8_top2_dsm_tasks_fixed_v2.py').read_text(encoding='utf-8')
needle="                x,y=task['position']; tile=farm['tiles'][y][x]"
assert needle in base
release=base.replace("'partial_pickups':0,", "'release_waits':0,'partial_pickups':0,")
release=release.replace(needle,needle+'''
                if step<task['step']:
                    if pos[0]!=x or pos[1]!=y:
                        op=['EAST' if pos[0]<x else 'WEST'] if pos[0]!=x else ['SOUTH' if pos[1]<y else 'NORTH']
                        self.diagnostics['moves']+=1
                    else:
                        op=['PASS']; self.diagnostics['release_waits']+=1
                    break
''')
release=release.replace('def _r8_guard_inputs(obs,action):','def _r8_guard_inputs(obs,action):\n    return action  # Fixed timing preserves the original input procurement contract.')
release=release.replace('round8_top2_dsm_tasks_fixed_v2_agent','round8_top2_dsm_tasks_release_agent')
(ROOT/'experiments/round8_top2_dsm_tasks_release.py').write_text(release,encoding='utf-8')

recovery=base.replace("'partial_pickups':0,", "'restoration_digs':0,'restoration_plants':0,'restoration_seed_waits':0,'partial_pickups':0,")
recovery=recovery.replace("st['step']=step\n        farm=", "st['step']=step\n        st['restoration_seed_requests']={}\n        farm=")
needle="                if name=='PLANT' and seed_budget.get(op[1],0)<=0:"
assert needle in recovery
recovery=recovery.replace(needle,'''                if name in ('WATER','FERTILIZE') and (tile is None or (isinstance(tile,dict) and tile.get('kind')=='WEED')):
                    expected=_R8_DEMOS[route]['dawn_states'][day]['farm']['tiles'][y][x]
                    crop=expected.get('crop') if isinstance(expected,dict) else None
                    first_yield={'TOMATO':8,'STRAWBERRY':10}.get(crop,99)
                    if day>=3 and day+first_yield<=27:
                        if tile is not None:
                            op=['DIG']; self.diagnostics['restoration_digs']+=1; break
                        if seed_budget.get(crop,0)>0:
                            op=['PLANT',crop]; seed_budget[crop]-=1
                            self.diagnostics['restoration_plants']+=1; break
                        st['restoration_seed_requests'][crop]=st['restoration_seed_requests'].get(crop,0)+1
                        op=['PASS']; self.diagnostics['restoration_seed_waits']+=1; break
'''+needle)
needle="    action['market']=orders\n    return action"
assert needle in recovery
recovery=recovery.replace(needle,'''    for crop,n in state.get('restoration_seed_requests',{}).items():
        existing=sum(o[2] for o in orders if o and o[0]=='BUY_SEED' and o[1]==crop)
        qty=max(0,n-existing)
        if qty and len(orders)<10 and farm['money']>600+SEED_PRICE[crop]*qty:
            orders.append(['BUY_SEED',crop,qty])
    action['market']=orders
    return action''')
recovery=recovery.replace('round8_top2_dsm_tasks_fixed_v2_agent','round8_top2_dsm_tasks_recovery_agent')
(ROOT/'experiments/round8_top2_dsm_tasks_recovery.py').write_text(recovery,encoding='utf-8')
for variant in ('release','recovery'):
    probe=(ROOT/'research_round8_top2_taskfix_probe.py').read_text(encoding='utf-8').replace('tasks_fixed.py',f'tasks_{variant}.py').replace("'dsm_tasks_fixed'",f"'dsm_tasks_{variant}'").replace('taskfix_screen.json',f'task_{variant}_screen.json').replace('taskfix_{seed}',f'task_{variant}_{{seed}}')
    (ROOT/f'research_round8_top2_{variant}_probe.py').write_text(probe,encoding='utf-8')

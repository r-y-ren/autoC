"""Keep demonstrated cross-worker cell dependencies while recomputing movement."""
from pathlib import Path
ROOT=Path(__file__).parent
source=(ROOT/'experiments/round8_top2_dsm_tasks_fixed_v2.py').read_text(encoding='utf-8')
source=source.replace("'partial_pickups':0,", "'dependency_waits':0,'partial_pickups':0,")
source=source.replace("'pickup_remaining':{},'step':-1}","'pickup_remaining':{},'done_tasks':set(),'step':-1}")
source=source.replace("indices={},pickup_remaining={})","indices={},pickup_remaining={},done_tasks=set())")
needle="                x,y=task['position']; tile=farm['tiles'][y][x]"
assert needle in source
source=source.replace(needle,needle+'''
                task_id=(task['step'],task['unit'])
                predecessor=self.dependencies.get(route,{}).get(task_id)
                if predecessor is not None and predecessor not in st['done_tasks']:
                    if pos[0]!=x or pos[1]!=y:
                        op=['EAST' if pos[0]<x else 'WEST'] if pos[0]!=x else ['SOUTH' if pos[1]<y else 'NORTH']
                        self.diagnostics['moves']+=1
                    else:
                        op=['PASS']; self.diagnostics['waits']+=1; self.diagnostics['dependency_waits']+=1
                    break
''')
source=source.replace("idx+=1; self.diagnostics['skipped_tasks']+=1; continue", "st['done_tasks'].add(task_id); idx+=1; self.diagnostics['skipped_tasks']+=1; continue")
source=source.replace("idx+=1; self.diagnostics['issued_tasks']+=1; break", "st['done_tasks'].add(task_id); idx+=1; self.diagnostics['issued_tasks']+=1; break")
source+='''
# Modified 2026-09-22: DAG edges preserve same-day cell operation order.
# An action may move earlier, but HARVEST cannot overtake a demonstrated WATER
# or FERTILIZE by another worker on the same cell.
_R8_TASKS.dependencies={}
for _r8_rid,_r8_demo in _R8_DEMOS.items():
    _r8_previous={}; _r8_edges={}
    for _r8_task in sorted(_r8_demo['tasks'],key=lambda x:(x['step'],x['unit'])):
        _r8_key=(_r8_task['step']//24,tuple(_r8_task['position']))
        _r8_id=(_r8_task['step'],_r8_task['unit'])
        if _r8_key in _r8_previous:
            _r8_edges[_r8_id]=_r8_previous[_r8_key]
        _r8_previous[_r8_key]=_r8_id
    _R8_TASKS.dependencies[_r8_rid]=_r8_edges
_R8_DEP_PARENT=agent

def round8_top2_dsm_tasks_dependencies_agent(obs,config=None):
    return _R8_DEP_PARENT(obs,config)

agent=round8_top2_dsm_tasks_dependencies_agent
agent.telemetry=_R8_IMPL.diagnostics
agent.routing_telemetry=_R8_ROUTER.diagnostics
agent.task_telemetry=_R8_TASKS.diagnostics
'''
dest=ROOT/'experiments/round8_top2_dsm_tasks_dependencies.py'
dest.write_text(source,encoding='utf-8')
print(dest.name,dest.stat().st_size)
probe=(ROOT/'research_round8_top2_taskfix_probe.py').read_text(encoding='utf-8').replace('tasks_fixed.py','tasks_dependencies.py').replace("'dsm_tasks_fixed'","'dsm_tasks_dependencies'").replace('taskfix_screen.json','task_dependencies_screen.json').replace('taskfix_{seed}','task_dependencies_{seed}')
(ROOT/'research_round8_top2_dependencies_probe.py').write_text(probe,encoding='utf-8')

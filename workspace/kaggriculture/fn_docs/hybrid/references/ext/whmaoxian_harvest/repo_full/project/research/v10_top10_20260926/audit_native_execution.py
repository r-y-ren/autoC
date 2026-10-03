"""Observe failed physical operations in one existing development simulation."""
from pathlib import Path
from collections import Counter
import copy,json,sys
D=Path(__file__).resolve().parent;R=D.parents[1]
sys.path.insert(0,str(R/'research/v10_rebuild_20260926'))
import fast_arena as arena
jobs=json.loads((D/'native_v6_jobs.json').read_text())
job=next(j for j in jobs if 'teacher04_rescue1.py' in j['candidate'] and j['seat']==0)
original=arena.engine._apply_unit_action
counts=Counter();examples=[]
def observed(farm,private,actor,command,board_size,day,turns_per_day,shed_capacity=100):
    positions=[farm['farmer']]+farm['hands']
    if actor>=len(positions):return original(farm,private,actor,command,board_size,day,turns_per_day,shed_capacity)
    x,y=positions[actor];before=copy.deepcopy((farm['tiles'][y][x],private['inventories'][actor],private['shed'],private['seeds']))
    result=original(farm,private,actor,command,board_size,day,turns_per_day,shed_capacity)
    after=(farm['tiles'][y][x],private['inventories'][actor],private['shed'],private['seeds'])
    if command and command[0] in ('PLANT','FEED','FERTILIZE','HARVEST','PLACE','PICKUP','CARE') and before==after:
        counts[command[0]]+=1
        if len(examples)<60:examples.append(dict(day=day,actor=actor,position=[x,y],command=command,cash=farm['money'],tile=before[0],own_bag=before[1],own_shed=before[2],own_seeds=before[3]))
    return result
try:
    arena.engine._apply_unit_action=observed
    result=arena.run_job(job)
finally:arena.engine._apply_unit_action=original
report=dict(job=job,result=result,unchanged_operations=dict(counts),first_examples=examples,scope='Unchanged official physical operations observed in a development game; examples include BOTH players and harmless redundant operations.')
(D/'native_execution_audit.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(dict(valid=result.get('valid'),margin=result.get('margin'),checkpoints=result.get('checkpoints'),unchanged=dict(counts),examples=examples[:8])),flush=True)

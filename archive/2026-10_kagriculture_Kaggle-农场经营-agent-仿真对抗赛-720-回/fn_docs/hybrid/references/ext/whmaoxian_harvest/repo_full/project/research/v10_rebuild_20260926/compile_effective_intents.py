"""Instrument unchanged official unit execution to remove historical no-op requests."""
from pathlib import Path
import copy,gzip,json
import fast_arena as arena
OUT=Path(__file__).resolve().parent
records=json.loads((OUT/'intent_agents.json').read_text(encoding='utf-8'))
results=[]
original=arena.engine._apply_unit_action
for record in records[:3]:
    game=json.loads(gzip.decompress((OUT/f"public_replays/{record['episode']}.json.gz").read_bytes()))
    state,env=arena.new_game(game['info']['seed'],game['configuration'])
    plans=[{'hands':0,'tasks':[[] for _ in range(25)]} for _ in range(30)]
    context={'step':0}
    def observed(farm,private,actor,command,board_size,day,turns_per_day,shed_capacity=100):
        selected=farm is state[0].observation.farms[record['seat']]
        if not selected or not command or command[0] in ('PASS','NORTH','SOUTH','EAST','WEST'):
            return original(farm,private,actor,command,board_size,day,turns_per_day,shed_capacity)
        positions=[farm['farmer']]+farm['hands']
        if actor>=len(positions):return original(farm,private,actor,command,board_size,day,turns_per_day,shed_capacity)
        x,y=positions[actor];before=copy.deepcopy((farm['tiles'][y][x],private['inventories'][actor],private['shed'],private['seeds']))
        result=original(farm,private,actor,command,board_size,day,turns_per_day,shed_capacity)
        after=(farm['tiles'][y][x],private['inventories'][actor],private['shed'],private['seeds'])
        if before!=after:
            cmd=list(command)
            if cmd[0]=='PICKUP':cmd=['PICKUP',cmd[1],after[1].get(cmd[1],0)-before[1].get(cmd[1],0)]
            plans[day]['tasks'][actor].append(dict(xy=[x,y],op=cmd,hour=context['step']%24,quadrant=1+(x>=5)+2*(y>=5)))
        return result
    arena.engine._apply_unit_action=observed
    try:
        for step in range(719):
            context['step']=step
            for seat in (0,1):
                state[seat].observation.step=step
                state[seat].action=copy.deepcopy(game['steps'][step+1][seat]['action'])
            plans[step//24]['hands']=max(plans[step//24]['hands'],len(state[record['seat']].observation.farms[record['seat']]['hands']))
            arena.engine.interpreter(state,env)
        rewards=[s.reward for s in state]
        assert rewards==game['rewards'],(record['episode'],rewards,game['rewards'])
    finally:
        arena.engine._apply_unit_action=original
    for day in plans:day['tasks']=day['tasks'][:day['hands']+1]
    result=dict(record,plans=plans,official_rewards=rewards,exact_reconstruction=True)
    results.append(result)
    (OUT/'effective_intents.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
    print('Executed intent reconstruction',record['episode'],rewards,'tasks',sum(len(q) for d in plans for q in d['tasks']),flush=True)

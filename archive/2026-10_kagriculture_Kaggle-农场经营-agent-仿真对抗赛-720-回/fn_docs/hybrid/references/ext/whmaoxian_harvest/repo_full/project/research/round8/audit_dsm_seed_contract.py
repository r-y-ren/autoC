"""Replay frozen observed actions only; inspect pre-plant seed and care contracts."""
import contextlib,io,gzip,json,sys,runpy
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
with contextlib.redirect_stdout(io.StringIO()):
    from kaggle_environments import make
path=ROOT/'research/round8/dsm_candidate_diagnostics/seed733556107-seat0-fieldcraft.json.gz'
replay=json.loads(gzip.decompress(path.read_bytes()))
env=make('kaggriculture',configuration={'seed':733556107,'episodeSteps':720},debug=True)
events=[]
targets={(2,0),(5,0),(2,1),(5,1),(2,2),(1,2)}
tape=runpy.run_path(str(ROOT/'experiments/round8_top2_dsm_compact.py'))['_R8_ROUTES']['111940707']
for step in range(264):
    obs=env.state[0].observation; farm=obs.farms[0]; private=obs.private
    action=replay['steps'][step+1][0]['action']
    commands=[action.get('farmer') or ['PASS'],*(action.get('hands') or [])]
    positions=[farm['farmer'],*farm['hands']]
    demand=Counter(c[1] for c in commands if len(c)>1 and c[0]=='PLANT')
    blocked={c:n for c,n in demand.items() if n>private['seeds'].get(c,0)}
    if step in (180,181,182,183,184,185,239,240,241):
        events.append({'type':'funding','step':step,'money':farm['money'],'hands':len(farm['hands']),'shed':dict(private['shed']),'inventories':[dict(x) for x in private['inventories']],'market':action['market']})
    if 216<=step and len(tape[step].get('hands',[]))>len(farm['hands']):
        events.append({'type':'understaffed','step':step,'hands':len(farm['hands']),'tape_hands':len(tape[step].get('hands',[])),'money':farm['money'],'shed':dict(private['shed']),'market':action['market'],'missing_commands':tape[step]['hands'][len(farm['hands']):]})
    if blocked or any(o and o[0]=='BUY_SEED' for o in action['market']):
        events.append({'type':'seeds','step':step,'day':step//24,'blocked':blocked,'seeds':dict(private['seeds']),'money':farm['money'],'market':action['market'],'plants':[(i,positions[i],c) for i,c in enumerate(commands) if i<len(positions) and c[0]=='PLANT']})
    if 192<=step<264:
        for i,(pos,command) in enumerate(zip(positions,commands)):
            if tuple(pos) in targets and command[0] not in ('NORTH','SOUTH','EAST','WEST'):
                x,y=pos;events.append({'type':'care','step':step,'actor':i,'pos':list(pos),'action':command,'tile':dict(farm['tiles'][y][x]) if isinstance(farm['tiles'][y][x],dict) else farm['tiles'][y][x]})
    env.step([replay['steps'][step+1][p]['action'] for p in (0,1)])
out=ROOT/'research/round8/top2/seed_contract_audit.json'
out.write_text(json.dumps(events,indent=2),encoding='utf-8')
print(json.dumps(events),flush=True)

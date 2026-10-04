"""Inspect actual candidate cargo and livestock service in one complete game."""
from pathlib import Path
from collections import Counter
import contextlib,io,json,sys
D=Path(__file__).resolve().parent;R=D.parents[1]
sys.path.insert(0,str(R/'research/v10_rebuild_20260926'))
with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
    import fast_arena as fa
candidate='research/herd_search_20260929/candidates/repeat_early.py'
result=fa.play(candidate,'submissions/release_v10_r2/main.py',1799657451,0,capture=True)
trace=result.pop('_trace');counts=Counter();examples=[];daily=[]
for step in range(719):
    obs=trace[step][0].observation;farm=obs['farms'][0];private=obs['private']
    action=trace[step+1][0].action
    positions=[farm['farmer']]+farm['hands'];units=[action.get('farmer') or ['PASS']]+list(action.get('hands',[]))
    for actor,(pos,cmd) in enumerate(zip(positions,units)):
        inv=private['inventories'][actor];tile=farm['tiles'][pos[1]][pos[0]]
        if len(cmd)>=2 and cmd[:2]==['PLACE','MILK'] and not inv.get('MILK',0) and inv.get('WOOL',0)>0:
            counts['milk_place_with_only_wool']+=1;counts['wool_waiting_units']+=inv['WOOL']
            if len(examples)<16:examples.append(dict(step=step,actor=actor,position=pos,command=cmd,inventory=inv))
        if isinstance(tile,dict) and tile.get('animal')=='SHEEP' and tile.get('yield_units',0)>0:
            counts['sheep_ready:'+str(cmd[0])]+=1
    if step%24==23 or step==718:
        post=trace[step+1][0].observation;daily.append(dict(step=step+1,cash=[f['money'] for f in post['farms']],carried_wool=sum(i.get('WOOL',0) for i in post['private']['inventories']),shed_wool=post['private']['shed'].get('WOOL',0)))
report=dict(result=result,counts=dict(counts),examples=examples,daily=daily,scope='One diagnostic execution on a known development world, not independent validation.')
(D/'cargo_flow_audit.json').write_text(json.dumps(report,indent=2))
print(json.dumps(dict(valid=result['valid'],margin=result['margin'],counts=dict(counts),examples=examples)),flush=True)

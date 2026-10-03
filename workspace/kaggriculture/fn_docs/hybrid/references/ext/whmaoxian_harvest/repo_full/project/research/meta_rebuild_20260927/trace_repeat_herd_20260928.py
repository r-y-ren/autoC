"""Inspect physical execution of the new repeated-herd prototype."""
from pathlib import Path
import contextlib,io,json,sys
D=Path(__file__).resolve().parent;R=D.parents[1]
sys.path.insert(0,str(R/'research/v10_rebuild_20260926'))
with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
    import fast_arena as fa
result=fa.play('research/meta_rebuild_20260927/candidates/repeat_two.py','submissions/release_v10_r2/main.py',1799657451,0,capture=True)
trace=result.pop('_trace');events=[]
for step in range(72,241):
    before=trace[step][0].observation;action=trace[step+1][0].action
    farm=before['farms'][0];private=before['private'];positions=[farm['farmer']]+farm['hands']
    units=[action.get('farmer',['PASS'])]+action.get('hands',[])
    selected=[]
    for actor,command in enumerate(units[:len(positions)]):
        if len(command)>1 and command[0] in ('PICKUP','PLACE') and command[1] in ('COW','SHEEP'):
            x,y=positions[actor];selected.append(dict(actor=actor,position=[x,y],command=command,tile=farm['tiles'][y][x],inventory=private['inventories'][actor]))
    buys=[o for o in action.get('market',[]) if o and o[0]=='BUY_ANIMAL']
    if selected or buys:events.append(dict(step=step,buy=buys,workers=selected,shed_animals={i:private['shed'].get(i,0) for i in ('COW','SHEEP')}))
print(json.dumps(dict(valid=result['valid'],margin=result['margin'],events=events)),flush=True)
(D/'repeat_herd_trace_20260928.json').write_text(json.dumps(dict(result=result,events=events),indent=2))

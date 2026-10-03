"""Offline audit. Hidden inventories are measured only after agent decisions."""
from pathlib import Path
import contextlib,copy,io,json,sys
B=Path(__file__).resolve().parent; D=B.parent; W=D.parent; R=W.parents[1]
sys.path.insert(0,str(W))
with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
 import fast_arena as fa
candidate='research/v10_rebuild_20260926/continuation/generation5/advance36.py'
opponent='research/v10_rebuild_20260926/notebooks/extracted/fieldcraft/single_file.py'
seed=349766850
entries=[fa.load(candidate),fa.load(opponent)]; ns=entries[0].__globals__
state,env=fa.new_game(seed); records=[]
for step in range(719):
 before={k:copy.deepcopy(ns.get(k,{})) for k in ('_OR2_REPORT','_ADV_REPORT')}
 for i,entry in enumerate(entries):
  state[i].observation.step=step
  state[i].action=entry(copy.deepcopy(state[i].observation),env.configuration)
 obs=state[0].observation
 changes={key:ns.get(report,{}).get(key,0)-before[report].get(key,0)
          for report,key in (('_OR2_REPORT','or2_sellnow'),('_ADV_REPORT','adv_units'))}
 if any(changes.values()):
  actual=dict(state[1].observation.private['shed'])
  for inv in state[1].observation.private['inventories']:
   for item,n in inv.items():actual[item]=actual.get(item,0)+n
  records.append(dict(step=step,changes=changes,similarity=ns['_r37_similarity'](obs),
   estimated=copy.deepcopy(ns.get('_OR2_STATE',{}).get(0,{}).get('stock',{})),
   actual_total=actual,actual_shed=dict(state[1].observation.private['shed']),
   our_orders=copy.deepcopy(state[0].action['market']),rival_orders=copy.deepcopy(state[1].action['market']),
   prices=dict(obs.market['prices']),shops=list(obs.town['unlocked_shops'])))
 fa.engine.interpreter(state,env)
 for value in state:value.observation.step=step+1
result=dict(seed=seed,candidate=candidate,opponent=opponent,money=[s.reward for s in state],events=records,
 warning='Opponent hidden inventory is audit output only. The deployed candidate receives only its ordinary legal observation.')
(B/'pressure_audit.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(dict(money=result['money'],events=len(records),
 min_similarity=min(r['similarity'] for r in records),max_similarity=max(r['similarity'] for r in records))),flush=True)

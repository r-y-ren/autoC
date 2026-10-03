"""Sequential 12-game paired round8 market screening, with silent errors exposed."""
import contextlib,io,json,time,hashlib
from pathlib import Path
root=Path(__file__).resolve().parents[1]
with contextlib.redirect_stdout(io.StringIO()):
 from kaggle_environments import make
sources=['submissions/release_v7/main.py','experiments/round8_market_recurrence.py']
opp='experiments/round7_routes/effective_111918050.py'
output=root/'results/round8_market_screen.json'
rows=[]
def load(name):
 ns={}
 with contextlib.redirect_stdout(io.StringIO()):exec(compile((root/name).read_text(encoding='utf-8-sig'),name,'exec'),ns)
 entry=[v for v in ns.values() if callable(v)][-1]
 return ns,entry

def errors(ns,entry):
 bad={}
 for name,value in ns.items():
  if isinstance(value,dict) and ('REPORT' in name.upper() or 'STATS' in name.upper()):
   for key,v in value.items():
    if isinstance(v,(int,float)) and v and ('error' in str(key).lower() or 'fallback' in str(key).lower()):bad[name+'.'+str(key)]=v
 impl=ns.get('_IMPL');chassis=getattr(impl,'chassis',None)
 for key,v in getattr(chassis,'diagnostics',{}).items():
  if v and ('error' in str(key).lower() or 'fallback' in str(key).lower()):bad['chassis.'+str(key)]=v
 for key,v in getattr(entry,'telemetry',{}).items():
  if isinstance(v,(int,float)) and v and ('error' in str(key).lower() or 'fallback' in str(key).lower()):bad['entry.'+str(key)]=v
 return bad
for seed in range(81000,81003):
 for seat in (0,1):
  for path in sources:
   ns,entry=load(path)
   oppns,oppentry=load(opp)
   players=[entry,oppentry]
   if seat:players.reverse()
   env=make('kaggriculture',configuration={'seed':seed,'episodeSteps':720},debug=True)
   start=time.perf_counter();env.run(players)
   end=env.steps[-1]
   allerrors=[v.get('stderr') for ls in env.logs for v in ls if isinstance(v,dict) and v.get('stderr','').strip()]
   statuses=[v.status for v in end]
   money=[s.observation.farms[i]['money'] for i,s in enumerate(end)]
   mine=money[seat];other=money[1-seat]
   report=dict(getattr(entry,'telemetry',{}))
   row={'source':path,'sha256':hashlib.sha256((root/path).read_bytes()).hexdigest(),'seed':seed,'seat':seat,'money':mine,'opponent_money':other,'delta':mine-other,'statuses':statuses,'seconds':round(time.perf_counter()-start,2),'stderr':allerrors,'silent_errors':errors(ns,entry),'opponent_silent_errors':errors(oppns,oppentry),'max_action_seconds':max(v[seat].get('duration',0) for v in env.logs if len(v)>seat),'market_report':dict(ns.get('_R8M_REPORT',{})),'orderbook_report':dict(ns.get('_CXD_REPORT',{}))}
   rows.append(row)
   output.write_text(json.dumps({'kind':'reactive public DSM episode imitation; not DSM private agent','opponent':opp,'rows':rows},indent=2),encoding='utf-8')
   print(json.dumps(row),flush=True)
   assert statuses==['DONE','DONE'] and not allerrors and not row['silent_errors'],row

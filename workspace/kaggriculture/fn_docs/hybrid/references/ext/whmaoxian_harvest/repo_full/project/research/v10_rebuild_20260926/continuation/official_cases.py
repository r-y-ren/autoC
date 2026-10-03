"""Collect 12 real file-path games independently of screening results."""
from pathlib import Path
import contextlib,gc,hashlib,io,json,time
D=Path(__file__).resolve().parent; R=D.parents[2]
with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
 import kaggle_environments
 from kaggle_environments import make
selection=json.loads((D/'selection.json').read_text()); design=json.loads((D/'confirmation_design.json').read_text())
assert hashlib.sha256((R/selection['candidate']).read_bytes()).hexdigest()==selection['sha256']
repair=json.loads((D/'confirmation_entry_repair_jobs.json').read_text())
for opponent in design['roster']:
 if opponent['name']=='marketshock':opponent['path']=repair[0]['opponent']
seed=design['seeds'][0]; results=[]
for opponent in design['roster']:
 for seat in (0,1):
  paths=[str(R/selection['candidate']),str(R/opponent['path'])]
  if seat:paths.reverse()
  out=io.StringIO(); began=time.perf_counter()
  with contextlib.redirect_stdout(out),contextlib.redirect_stderr(out):
   env=make('kaggriculture',configuration={'seed':seed,'episodeSteps':720},debug=True)
   env.run(paths)
  hashes=[hashlib.sha256(),hashlib.sha256()]
  for pair in env.steps[1:]:
   for i,state in enumerate(pair):hashes[i].update(json.dumps(state.action,sort_keys=True).encode())
  money=[env.steps[-1][seat].reward,env.steps[-1][1-seat].reward]
  logs=[(i,log) for step in env.logs for i,log in enumerate(step) if isinstance(log,dict)]
  errors=[log.get('stderr','') for _,log in logs if log.get('stderr','').strip()]
  durations=[log.get('duration',0) for i,log in logs if i==seat]
  item=dict(candidate=selection['candidate'],candidate_sha256=selection['sha256'],
   opponent=opponent['path'],opponent_sha256=hashlib.sha256((R/opponent['path']).read_bytes()).hexdigest(),
   family=opponent['name'],seed=seed,seat=seat,money=money,states=len(env.steps),
   statuses=[s.status for s in env.steps[-1]],action_hash=[h.hexdigest() for h in hashes],
   max_candidate_seconds=max(durations),stderr=errors,captured_output=out.getvalue()[:1200],
   seconds=time.perf_counter()-began)
  item['valid']=item['states']==720 and item['statuses']==['DONE','DONE'] and not errors
  results.append(item)
  (D/'official_cases.json').write_text(json.dumps(dict(games=results,complete=len(results)==12,engine=kaggle_environments.__version__),indent=2),encoding='utf-8')
  print(json.dumps({k:item[k] for k in ('family','seed','seat','money','valid','max_candidate_seconds')}),flush=True)
  del env; gc.collect()
assert len(results)==12 and all(r['valid'] for r in results)

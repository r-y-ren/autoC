"""Six sequential official games using the parent league's hash-bound runner."""
import hashlib,json,os,sys
from pathlib import Path
root=Path(__file__).resolve().parents[2];sys.path.insert(0,str(root))
from league_round8 import run_job,digest
os.chdir(root)
oldlib=os.environ.pop('V92_SELL_LIB',None)
rows=[]
try:
 for name in ('fieldcraft','master2965','icefire'):
  candidate=f'external/round8/{name}/main.py';opponent='submissions/release_v7/main.py'
  for seat in (0,1):
   sys.modules.pop('mirror_plan',None)
   job={'candidate':candidate,'candidate_sha256':digest(candidate),'opponent':opponent,'opponent_sha256':digest(opponent),'seed':84000,'seat':seat,'split':'public_source_smoke'}
   job['id']=hashlib.sha256(json.dumps(job,sort_keys=True).encode()).hexdigest()[:24]
   result=run_job(job);rows.append(result)
   (root/'results/round8_public_sources_screen.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
   print(json.dumps({k:result.get(k) for k in ('candidate','seat','delta','valid','max_action_seconds','entry_names','exception')}),flush=True)
finally:
 if oldlib is not None:os.environ['V92_SELL_LIB']=oldlib

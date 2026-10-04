"""Eight development screens per frozen public fusion, one sequential process."""
import hashlib,json,os,sys
from pathlib import Path
root=Path(__file__).resolve().parents[2];sys.path.insert(0,str(root));os.chdir(root)
from league_round8 import run_job,digest,freeze_seeds
seeds=freeze_seeds()['development'][:4]
assert 'V92_SELL_LIB' not in os.environ, 'Clear V92_SELL_LIB before deterministic local evaluation.'
rows=[]
for candidate in ['experiments/round8_advance.py','experiments/round8_fullfusion.py']:
 for seed in seeds:
  for opponent in ['submissions/release_v7/main.py','submissions/release_v6/main.py']:
   job={'candidate':candidate,'candidate_sha256':digest(candidate),'opponent':opponent,'opponent_sha256':digest(opponent),'seed':seed,'seat':0,'split':'development'}
   job['id']=hashlib.sha256(json.dumps(job,sort_keys=True).encode()).hexdigest()[:24]
   result=run_job(job);rows.append(result)
   (root/'results/round8_public_fusions_screen.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
   print(json.dumps({k:result.get(k) for k in ('candidate','opponent','seed','delta','valid','max_action_seconds','entry_names','exception')}),flush=True)

"""Initial eight games of conservative terminal input fusion, frozen dev worlds."""
import hashlib,json,os,sys
from pathlib import Path
root=Path(__file__).resolve().parents[2];sys.path.insert(0,str(root));os.chdir(root)
from league_round8 import run_job,digest,freeze_seeds
assert 'V92_SELL_LIB' not in os.environ
candidate='experiments/round8_terminal_inputs.py';rows=[]
for seed in freeze_seeds()['development'][:4]:
 for opponent in ['submissions/release_v7/main.py','external/round8/master2965/main.py']:
  job={'candidate':candidate,'candidate_sha256':digest(candidate),'opponent':opponent,'opponent_sha256':digest(opponent),'seed':seed,'seat':0,'split':'development'}
  job['id']=hashlib.sha256(json.dumps(job,sort_keys=True).encode()).hexdigest()[:24]
  r=run_job(job);rows.append(r)
  (root/'results/round8_terminal_inputs_screen.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
  print(json.dumps({k:r.get(k) for k in ['candidate','opponent','seed','delta','valid','max_action_seconds','exception']}),flush=True)
  print(r.get('telemetry',[{}])[0].get('details',{}).get('_TI_REPORT',{}),flush=True)

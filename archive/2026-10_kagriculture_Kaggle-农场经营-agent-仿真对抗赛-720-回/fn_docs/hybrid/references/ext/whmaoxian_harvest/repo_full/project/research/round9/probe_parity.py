import argparse,contextlib,copy,gzip,hashlib,io,json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--episode',type=int,required=True);p.add_argument('--output',required=True);a=p.parse_args()
root=Path(__file__).resolve().parents[2]
with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
 from kaggle_environments.agent import get_last_callable
g=json.loads(gzip.decompress((root/f'research/round9/user-{a.episode}.json.gz').read_bytes()))
row=next(r for r in json.loads((root/'research/round9/audit_selection.json').read_text(encoding='utf-8')) if r['eid']==a.episode)
source=root/f"submissions/release_{row['version']}/main.py"
fn=get_last_callable(source.read_text(encoding='utf-8'),path=str(source));actions=[];differences=[]
for step in range(719):
 obs=copy.deepcopy(g['steps'][step][row['seat']]['observation']);obs['step']=step
 act=fn(obs,g['configuration']);actions.append(act)
 if act!=g['steps'][step+1][row['seat']]['action']:differences.append({'step':step,'market':act.get('market')})
result={'eid':a.episode,'actions_sha256':hashlib.sha256(json.dumps(actions,sort_keys=True).encode()).hexdigest(),'differences':differences}
(root/a.output).write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps(result))

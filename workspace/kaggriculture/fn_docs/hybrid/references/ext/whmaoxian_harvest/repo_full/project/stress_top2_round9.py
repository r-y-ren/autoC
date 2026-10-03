"""Locked public-replay counterfactual stress; NOT the private top-player policies."""
import argparse,contextlib,io,json,gzip,hashlib,requests,copy,time
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor,as_completed
ROOT=Path(__file__).resolve().parent

def one(job):
 meta,source,sha=job
 with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
  from kaggle_environments import make
  from kaggle_environments.agent import get_last_callable
 g=json.loads(gzip.decompress((ROOT/f"research/round9/top2-holdout-{meta['eid']}.json.gz").read_bytes()))
 s=meta['seat'];cfg=dict(g['configuration'],seed=g['info']['seed']);diff=[];shop_diff=[]
 def tape(seat):
  def act(obs,configuration=None):return g['steps'][int(obs['step'])+1][seat]['action']
  return act
 if source=='original-replay':
  entries=[tape(0),tape(1)];candidate=None
 else:
  data=(ROOT/source).read_bytes();assert hashlib.sha256(data).hexdigest()==sha
  candidate=get_last_callable(data.decode('utf-8'),path=str(ROOT/source))
  def opponent(obs,configuration=None):
   t=int(obs['step']);a=obs['farms'][s];b=g['steps'][t][s]['observation']['farms'][s]
   if any(a[k]!=b[k] for k in ('tiles','farmer','hands','unlocked_quadrants','hires_today')):diff.append(t)
   if obs['town']['unlocked_shops']!=g['steps'][t][s]['observation']['town']['unlocked_shops']:shop_diff.append(t)
   return g['steps'][t+1][s]['action']
  entries=[None,None];entries[s]=opponent;entries[1-s]=candidate
 env=make('kaggriculture',configuration=cfg,debug=True);env.run(entries)
 rewards=[x.reward for x in env.steps[-1]]
 stderr=[l.get('stderr') for step in env.logs for l in step if isinstance(l,dict) and l.get('stderr','').strip()]
 from league_round8 import telemetry
 tele=telemetry(candidate) if candidate else None
 result={**meta,'source':source,'sha256':sha,'seed':g['info']['seed'],'rewards':rewards,'delta':rewards[1-s]-rewards[s],
 'original_rewards':g['rewards'],'opponent_physical_divergence_steps':len(diff),'first_opponent_physical_divergence':diff[0] if diff else None,
 'market_path_divergence_steps':len(shop_diff),'first_market_path_divergence':shop_diff[0] if shop_diff else None,
 'states':len(env.steps),'statuses':[x.status for x in env.steps[-1]],'stderr':stderr,'telemetry':tele,
 'counterfactual_only':True,'private_adaptive_opponent_evaluated':False}
 result['valid']=len(env.steps)==720 and result['statuses']==['DONE','DONE'] and not stderr and not (tele and tele['nonzero'])
 if source=='original-replay':
  assert result['valid'] and rewards==g['rewards']
  matched=0
  for t in range(720):
   for seat in range(2):
    actual=dict(env.steps[t][seat].observation);expected=dict(g['steps'][t][seat]['observation'])
    for observation in (actual,expected):observation.pop('remainingOverageTime',None);observation['step']=t
    assert actual==expected,(meta['eid'],t,seat)
    matched+=1
  result['original_observations_matched']=matched
 return result

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--candidate',required=True);p.add_argument('--expected-sha256',required=True);p.add_argument('--workers',type=int,default=4);a=p.parse_args()
 assert hashlib.sha256((ROOT/a.candidate).read_bytes()).hexdigest()==a.expected_sha256
 selection=json.loads((ROOT/'research/round9/top2_locked_holdout_selection.json').read_text())
 for meta in selection:
  out=ROOT/f"research/round9/top2-holdout-{meta['eid']}.json.gz"
  if not out.exists():
   r=requests.get(f"https://www.kaggle.com/competitions/episodes/{meta['eid']}/replay.json",timeout=120);r.raise_for_status()
   g=json.loads(r.content);assert len(g['steps'])==720;out.write_bytes(gzip.compress(r.content));print('downloaded',meta['eid'],flush=True)
 sources=[('original-replay',None),('submissions/release_v8/main.py',hashlib.sha256((ROOT/'submissions/release_v8/main.py').read_bytes()).hexdigest()),(a.candidate,a.expected_sha256)]
 ledger=ROOT/'results/round9_top2_locked_stress.jsonl'
 rows=[json.loads(l) for l in ledger.read_text().splitlines()] if ledger.exists() else []
 done={(r['eid'],r['source'],r['sha256']) for r in rows}
 jobs=[(m,s,h) for m in selection for s,h in sources if (m['eid'],s,h) not in done]
 with ProcessPoolExecutor(a.workers) as pool,ledger.open('a',encoding='utf-8') as f:
  for future in as_completed([pool.submit(one,j) for j in jobs]):
   r=future.result();rows.append(r);f.write(json.dumps(r)+'\n');f.flush()
   print({k:r[k] for k in ['author','eid','source','delta','valid','opponent_physical_divergence_steps']},flush=True)
 summary={}
 for source,sha in sources:
  matches=[r for r in rows if r['source']==source and r['sha256']==sha]
  summary[source]={'matches':len(matches),'valid':sum(r['valid'] for r in matches),'wins':sum(r['delta']>0 for r in matches),'losses':sum(r['delta']<0 for r in matches),'ties':sum(r['delta']==0 for r in matches),'opponent_physical_trace_preserved':sum(r['opponent_physical_divergence_steps']==0 for r in matches)}
 (ROOT/'results/round9_top2_locked_stress.json').write_text(json.dumps({'summary':summary,'counterfactual_only':True,'warning':'Recorded rival actions do not adapt to our changes. This is not a head-to-head win rate against DSM or Vadim.'},indent=2),encoding='utf-8')
 print(json.dumps(summary),flush=True)

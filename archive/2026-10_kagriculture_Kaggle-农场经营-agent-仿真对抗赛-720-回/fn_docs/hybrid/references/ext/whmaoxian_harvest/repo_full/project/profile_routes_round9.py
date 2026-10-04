"""Build economic flow profiles from actual engine transactions; never fit to scores."""
import contextlib,io,json,hashlib,importlib,collections,time
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor,as_completed
ROOT=Path(__file__).resolve().parent

def job(route):
 with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
  from kaggle_environments import make
  from kaggle_environments.agent import get_last_callable
  engine=importlib.import_module('kaggle_environments.envs.kaggriculture.kaggriculture')
  src=(ROOT/'submissions/release_v8/main.py').read_text(encoding='utf-8')
  entry=get_last_callable(src);other=get_last_callable(src)
 g=entry.__globals__;parent=g['_IMPL'].chassis.router
 def router(obs,step,state):
  r=parent(obs,step,state)
  if 144<=step<648:state['route']=route;return route
  return r
 g['_IMPL'].chassis.router=router
 g['_v219_qualifies']=lambda obs,native:False
 flow=[{'sell':{},'buy':{},'fixed':0} for _ in range(720)];ctx={};snaps={}
 def actor(obs,cfg=None):
  ctx['step']=int(obs['step'])
  if ctx['step'] in (144,216,264,288,360,432,648):
   snaps[str(ctx['step'])]=json.loads(json.dumps({'farm':obs['farms'][0],'private':obs['private']}))
  return entry(obs,cfg)
 original={name:getattr(engine,name) for name in ('_process_market','_commit_unit','_do_hire','_do_buy_land')}
 def market(state,env):
  ctx['farm']=id(state[0].observation.farms[0]);return original['_process_market'](state,env)
 def commit(op,item,price,farm,private,market,shed_capacity=100):
  result=original['_commit_unit'](op,item,price,farm,private,market,shed_capacity)
  if result and id(farm)==ctx.get('farm'):
   row=flow[ctx['step']]
   if op in ('SELL','BUY_PRODUCT'):
    key='sell' if op=='SELL' else 'buy';row[key][item]=row[key].get(item,0)+1
   else:row['fixed']+=price
  return result
 def hire(farm,private,board_size,mult=1):
  before=farm['money'];res=original['_do_hire'](farm,private,board_size,mult)
  if id(farm)==ctx.get('farm'):flow[ctx['step']]['fixed']+=before-farm['money']
  return res
 def land(farm,board_size):
  before=farm['money'];res=original['_do_buy_land'](farm,board_size)
  if id(farm)==ctx.get('farm'):flow[ctx['step']]['fixed']+=before-farm['money']
  return res
 for name,fn in [('_process_market',market),('_commit_unit',commit),('_do_hire',hire),('_do_buy_land',land)]:setattr(engine,name,fn)
 try:
  env=make('kaggriculture',configuration={'seed':0,'episodeSteps':720},debug=True);env.run([actor,other])
 finally:
  for name,fn in original.items():setattr(engine,name,fn)
 result={'route':route,'profile_seed':0,'purpose':'physical flow calibration, not performance validation','flow':flow,'snapshots':snaps,'states':len(env.steps),'statuses':[s.status for s in env.steps[-1]],'money':env.steps[-1][0].reward}
 assert result['states']==720 and result['statuses']==['DONE','DONE']
 from league_round8 import telemetry
 result['telemetry']=telemetry(entry)
 out=ROOT/f'research/round9/profiles/route_{route}.json';out.write_text(json.dumps(result,separators=(',',':')),encoding='utf-8')
 return route,result['money'],result['telemetry']['nonzero']

if __name__=='__main__':
 with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
  from kaggle_environments.agent import get_last_callable
  f=get_last_callable((ROOT/'main.py').read_text(encoding='utf-8'))
 routes=[r for r in f.__globals__['_IMPL'].chassis.routes if r!=1]
 (ROOT/'research/round9/profiles').mkdir(parents=True,exist_ok=True)
 with ProcessPoolExecutor(6) as pool:
  fut=[pool.submit(job,r) for r in routes if not (ROOT/f'research/round9/profiles/route_{r}.json').exists()]
  for f in as_completed(fut):print(f.result(),flush=True)

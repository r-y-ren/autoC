"""Offline oracle ceiling: quantify order-model error on six public study trajectories.
Opponent private stock and same-turn action are ORACLE ONLY, never exported to agents.
This evaluates immediate money margins with physical production held fixed.
"""
import gzip,json,itertools,time
from pathlib import Path
root=Path(__file__).resolve().parents[1]
ns={};exec(compile((root/'experiments/round8_market_recurrence.py').read_text(),'<agent>','exec'),ns)
rows=[r for r in json.loads((root/'research/round7/top2/index.json').read_text()) if r['split']=='study']
output=[]
for row in rows:
 g=json.loads(gzip.decompress((root/f"research/round7/top2/{row['episode_id']}.json.gz").read_bytes()))
 p=row['seat'];details=[]
 for t in range(240,696):
  obs=dict(g['steps'][t][p]['observation']);obs['step']=t
  other=dict(g['steps'][t][1-p]['observation']);other['step']=t
  a=g['steps'][t+1][p]['action'];opp=g['steps'][t+1][1-p]['action']
  orders=a.get('market',[])[:10];theirs=opp.get('market',[])[:10]
  slots=[i for i,o in enumerate(orders) if o and o[0]=='SELL']
  if not 2<=len(slots)<=6:continue
  # Do not reorder a sale that is chained to a buy of the same product.
  if {o[1] for o in orders if o and len(o)>1 and o[0]=='BUY_PRODUCT'} & {orders[i][1] for i in slots}:continue
  stock=ns['projected_shed'](a,ns['FarmView'](obs))
  oppstock=ns['projected_shed'](opp,ns['FarmView'](other))
  inv=dict(obs['market']['inventory']);params=ns['_v44y_params'](obs)
  oracle=ns['_r8m_factor'](theirs,inv,stock,oppstock,params)
  mirror=ns['_v44y_factor_margin'](orders,inv,stock,params)
  real0=realbest=oracle(orders);mir0=mirbest=mirror(orders)
  mircand=orders;realcand=orders
  for perm in itertools.permutations([orders[i] for i in slots]):
   cand=list(orders)
   for i,o in zip(slots,perm):cand[i]=o
   r=oracle(cand);m=mirror(cand)
   if r>realbest+.5:realbest=r;realcand=cand
   if m>mirbest+.5:mirbest=m;mircand=cand
  if realbest>real0 or mirbest>mir0:
   details.append({'step':t,'oracle_gain':realbest-real0,'mirror_predicted_gain':mirbest-mir0,'mirror_real_gain':oracle(mircand)-real0,'own_market':orders,'rival_market':theirs,'oracle_orders':realcand,'mirror_orders':mircand})
 result={'episode_id':row['episode_id'],'team':row['team'],'kind':'same-turn omniscient diagnostic; not a deployable policy or win rate','turns':len(details),'oracle_margin_gain':sum(d['oracle_gain'] for d in details),'mirror_predicted_margin_gain':sum(d['mirror_predicted_gain'] for d in details),'mirror_actual_margin_gain':sum(d['mirror_real_gain'] for d in details),'details':details}
 output.append(result)
 (root/'results/round8_market_oracle_audit.json').write_text(json.dumps(output,indent=2))
 print({k:v for k,v in result.items() if k!='details'},flush=True)

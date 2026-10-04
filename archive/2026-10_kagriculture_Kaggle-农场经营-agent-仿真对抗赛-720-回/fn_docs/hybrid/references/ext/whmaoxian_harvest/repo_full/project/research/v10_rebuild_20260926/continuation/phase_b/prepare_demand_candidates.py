"""Test a demand-aware sale-reservation gate on existing development cases."""
from pathlib import Path
import hashlib,json
B=Path(__file__).resolve().parent; D=B.parent; W=D.parent; R=W.parents[1]
base=(D/'generation5/advance36.py').read_text(encoding='utf-8')
needle='                        q = min(planned, avail - take)'
assert base.count(needle)==1
replacement='''                        demand = _b_known_demand(observation, item, step, t)
                        if st['stock'].get(item, 0) < max(_OR2_SN_K, _B_TOWN_FACTOR * demand):
                            _B_TOWN_REPORT['declines'] += 1
                            continue
                        q = min(planned, avail - take)'''
base=base.replace(needle,replacement)
tail='''
# Only present town shops and our own planned sale times are used.
_B_TOWN_REPORT={'declines':0}
def _b_known_demand(obs,item,start,end):
    per_tick=0
    for shop in obs['town']['unlocked_shops']:
        products=_OR2_SHOPS.get(shop,())
        if item in products:per_tick+=2 if len(products)==1 else 1
    return per_tick*((end-1)//4-(start-1)//4)+(end-1)//24-(start-1)//24
_B_DEMAND_PARENT=r2_opening_agent
def demand_agent(observation,configuration=None):
    if int(observation['step'])==0:_B_TOWN_REPORT['declines']=0
    return _B_DEMAND_PARENT(observation,configuration)
demand_agent.telemetry=_B_TOWN_REPORT
agent=demand_agent
kaggle_submission_agent=demand_agent
'''
C=B/'demand'; C.mkdir(exist_ok=True)
reference_jobs=json.loads((D/'generation6_jobs.json').read_text())
reference_name='submissions/release_v10/main.py'
reference_jobs=[j for j in reference_jobs if j['candidate']==reference_name]
jobs=[]
for name,factor in [('demand05',.5),('demand1',1.0),('demand2',2.0)]:
 text=base+tail+f'\n_B_TOWN_FACTOR={factor!r}\n'
 path=C/(name+'.py');assert not path.exists();compile(text,str(path),'exec');path.write_text(text,encoding='utf-8')
 digest=hashlib.sha256(path.read_bytes()).hexdigest()
 for old in reference_jobs:
  job={**old,'candidate':path.relative_to(R).as_posix(),'candidate_sha256':digest};job.pop('id')
  job['id']=hashlib.sha256(json.dumps(job,sort_keys=True).encode()).hexdigest()[:24];jobs.append(job)
(D/'demand_dev_jobs.json').write_text(json.dumps(jobs,indent=2),encoding='utf-8')
print(json.dumps({'candidates':3,'full_games':len(jobs),'only_development_worlds':True}),flush=True)

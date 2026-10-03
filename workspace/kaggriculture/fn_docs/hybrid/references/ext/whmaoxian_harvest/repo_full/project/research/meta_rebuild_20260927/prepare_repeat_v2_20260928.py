"""Second repeated-herd generation: recognize existing successful species corrections."""
from pathlib import Path
import hashlib,json,random
D=Path(__file__).resolve().parent;R=D.parents[1];BASE='submissions/release_v10_r2/main.py'
sha=lambda b:hashlib.sha256(b).hexdigest()
raw=(R/BASE).read_bytes();assert sha(raw)=='b35b5b09fbec059ab7cbd2ba67a9fbb6d3e467ef5262f3e2ddba592b3e50c1c4'
tail=(D/'repeat_herd_policy_20260928.txt').read_text()
for old,new in [("commands[actor][:2]==['PICKUP','COW']","commands[actor][:2] in (['PICKUP','COW'],['PICKUP','SHEEP'])"),("commands[actor][:2]==['PLACE','COW']","commands[actor][:2] in (['PLACE','COW'],['PLACE','SHEEP'])")]:
    assert tail.count(old)==1;tail=tail.replace(old,new)
old="if farm['money']<budget:_K28S_REPORT['budget_veto']+=1"
new="if not (_k28s_affordable(observation,action,_K28S_RESERVE) if _K28S_FUND_SALES else farm['money']>=budget):_K28S_REPORT['budget_veto']+=1"
assert tail.count(old)==1;tail=tail.replace(old,new)
helper=(D/'herd_cash_guard_20260928.txt').read_text()
assert helper.count('net={};hires=')==1;helper=helper.replace('net={};hires=','net={};lower={};hires=')
(D/'herd_cash_guard_v2_20260928.txt').write_text(helper)
(D/'repeat_herd_v2_policy_20260928.txt').write_text(tail)
variants=[]
settings=[('repeat_v2_one',1,150,False,False,False,False),('repeat_v2_two',2,150,False,False,False,False),('repeat_v2_nomilk',3,150,True,False,False,False),('repeat_v2_funded',3,25,False,False,True,False),('repeat_v2_repair',3,150,False,True,False,False),('repeat_v2_care',3,150,False,False,False,True)]
for name,limit,reserve,nomilk,repair,funding,care in settings:
    cfg=dict(FROM=72,TO=264,COW_FLOOR=2,LIMIT=limit,RESERVE=reserve,MIN_GAIN=600,NO_MILK=nomilk,REPAIR=repair,FUND_SALES=funding)
    data=raw+('\n'+''.join('_K28S_'+k+'='+repr(v)+'\n' for k,v in cfg.items())).encode()+helper.encode()+tail.encode()
    if care:data+=b'\n_TF_FEED=False\n_TF_CARE=True\n'+(D/'terminal_feed_tail.txt').read_bytes().replace(b'_TF_PARENT=phase_b_agent',b'_TF_PARENT=repeat_herd_agent')
    path=D/'candidates'/(name+'.py');compile(data,str(path),'exec')
    if path.exists():assert path.read_bytes()==data
    else:path.write_bytes(data)
    variants.append(dict(name=name,path=path.relative_to(R).as_posix(),sha256=sha(data),parameters=cfg,terminal_care=care))
jobs=[]
for v in variants+[dict(name='r2',path=BASE,sha256=sha(raw))]:
    for seat in (0,1):
        j=dict(candidate=v['path'],opponent=BASE,family='r2',panel='mechanism_diagnostic',seed=1799657451,seat=seat,candidate_sha256=v['sha256'],opponent_sha256=sha(raw))
        j['id']=sha(json.dumps(j,sort_keys=True).encode())[:24];jobs.append(j)
for name,data in [('repeat_v2_design_20260928.json',dict(variants=variants,scope='Second mechanism generation, development only.')),('repeat_v2_smoke_jobs_20260928.json',jobs)]:
    p=D/name;text=json.dumps(data,indent=2)
    if p.exists():assert p.read_text()==text
    else:p.write_text(text)
print(json.dumps(dict(variants=len(variants),cases=len(jobs))),flush=True)

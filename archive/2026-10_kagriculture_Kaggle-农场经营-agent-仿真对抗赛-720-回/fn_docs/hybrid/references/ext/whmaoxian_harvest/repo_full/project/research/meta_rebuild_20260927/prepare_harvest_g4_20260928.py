"""Integrate harvest/calendar synchronization into the selected development architecture."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1];BASE='submissions/release_v10_r2/main.py'
sha=lambda b:hashlib.sha256(b).hexdigest()
parent_path='research/meta_rebuild_20260927/candidates/g3_robust.py'
parent=(R/parent_path).read_text(encoding='utf-8');helper=(D/'herd_harvest_sync_20260928.txt').read_text(encoding='utf-8')
helper=helper.replace('actor>=len(commands) or quota<=0','actor>=len(commands) or actor>=len(positions) or quota<=0')
variants=[]
settings=[('h4_all',1,False,True,True,1),('h4_ripe',3,False,True,True,1),('h4_overflow',1,True,True,True,1),('h4_field',1,False,False,True,1),('h4_native_sales',3,False,True,False,1),('h4_two',3,False,True,True,2)]
for name,minimum,overflow,shipping,sales,limit in settings:
    source=parent
    marker='def repeat_herd_agent(observation,configuration=None):';assert source.count(marker)==1
    constants=f'\n_K28H_MIN_YIELD={minimum!r}\n_K28H_OVERFLOW_ONLY={overflow!r}\n_K28H_SHIP={shipping!r}\n'
    source=source.replace(marker,constants+helper+'\n'+marker)
    marker='    action=_K28S_PARENT(observation,configuration)';assert source.count(marker)==1
    source=source.replace(marker,"    if st.get('ship_day')!=day:st['ship_day']=day;st['expedited']={}\n"+marker)
    marker="        if (x,y,int(tile['placed_day'])) not in st['sites']:continue";assert source.count(marker)==1
    source=source.replace(marker,marker+"\n        commands[actor]=_k28h_harvest(observation,st,actor,tile,commands[actor])")
    marker='    result=dict(action,farmer=commands[0],hands=commands[1:],market=market)';assert source.count(marker)==1
    source=source.replace(marker,'    if _K28H_SHIP:commands=_k28h_ship(observation,st,action,commands)\n'+marker)
    source=source.replace('_K28S_LIMIT=1','_K28S_LIMIT='+str(limit),1)
    marker='_MP_REPORT=_K28S_REPORT';assert source.count(marker)==1
    source=source.replace(marker,"_K28S_REPORT.update(early_harvests=0,early_shipped_units=0)\n"+marker)
    if not sales:
        marker="extra=min(st['credit'],max(0,int(stock.get('WOOL',0))-planned))";assert source.count(marker)==1
        source=source.replace(marker,'extra=0  # Retain native sales only.')
    data=source.encode();path=D/'candidates'/(name+'.py');compile(source,str(path),'exec')
    if path.exists():assert path.read_bytes()==data
    else:path.write_bytes(data)
    variants.append(dict(name=name,path=path.relative_to(R).as_posix(),sha256=sha(data),minimum_yield=minimum,overflow_only=overflow,shipping=shipping,extra_sales=sales,limit=limit))
variants.extend(dict(name=name,path=p,sha256=sha((R/p).read_bytes())) for name,p in [('g3_robust',parent_path),('r2',BASE)])
jobs=[]
for seed in (1799657451,1401688540):
    for v in variants:
        for seat in (0,1):
            j=dict(candidate=v['path'],opponent=BASE,family='r2',panel='mechanism_diagnostic',seed=seed,seat=seat,candidate_sha256=v['sha256'],opponent_sha256=sha((R/BASE).read_bytes()))
            j['id']=sha(json.dumps(j,sort_keys=True).encode())[:24];jobs.append(j)
for name,data in [('harvest_g4_20260928_design.json',dict(variants=variants,scope='Two declared development worlds, mechanism activation screening only.')),('harvest_g4_20260928_jobs.json',jobs)]:
    p=D/name;text=json.dumps(data,indent=2)
    if p.exists():assert p.read_text()==text
    else:p.write_text(text)
print(json.dumps(dict(variants=len(variants),cases=len(jobs))),flush=True)

"""Mechanism probe only: shared procurement, canonical R2 continuation, gated expert."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1];sha=lambda b:hashlib.sha256(b).hexdigest()
r2=(R/'submissions/release_v10_r2/main.py').read_bytes()
assert sha(r2)=='b35b5b09fbec059ab7cbd2ba67a9fbb6d3e467ef5262f3e2ddba592b3e50c1c4'
new=(D/'route_raw_fixed10.py').read_bytes()
for name,data in [('bridge_r2_core.py',r2),('bridge_new_core.py',new)]:
    p=D/name
    if p.exists():assert p.read_bytes()==data
    else:p.write_bytes(data)
tail=(D/'bridge_policy_tail.txt').read_text()
tail=tail.replace("    virtual['farms'][seat]['farmer']=[4,3]\n",'')
tail=tail.replace("{'mode':None}","{'mode':None,'prebought_seed':1}")
tail=tail.replace("original.get('farmer')!=['NORTH']","original.get('farmer')!=['PASS']")
tail=tail.replace("'market':[['BUY_PRODUCT','WHEAT',5],['BUY_ANIMAL','COW',1]","'market':[['BUY_PRODUCT','WHEAT',5],['BUY_SEED','WHEAT',1],['BUY_ANIMAL','COW',1]")
tail=tail.replace("        action=_BR28_R2(_br28_virtual_r2(observation),configuration)","        state['prebought_seed']=0\n        action=_BR28_R2(_br28_virtual_r2(observation),configuration)")
tail=tail.replace("action.get('farmer')!=['PASS']","action.get('farmer')!=['NORTH']")
tail=tail.replace("    return action\ncompatible_opening_agent.telemetry", "    if state['mode']=='new' and state['prebought_seed']:\n        orders=[list(o) for o in action.get('market',[])]\n        for o in orders:\n            if len(o)>2 and o[:2]==['BUY_SEED','WHEAT']:\n                q=min(int(o[2]),state['prebought_seed']);o[2]-=q;state['prebought_seed']-=q\n        action=dict(action,market=orders)\n    return action\ncompatible_opening_agent.telemetry")
(D/'bridge_policy_v2_tail.txt').write_text(tail)
variants=[]
for mode,gate in (('r2',2000),('new',2000),('gated',2000)):
    header=f'_BR28_R2_SHA={sha(r2)!r}\n_BR28_NEW_SHA={sha(new)!r}\n_BR28_MODE={mode!r}\n_BR28_GATE={gate}\n'
    data=(header+tail).encode();p=D/('bridge_'+mode+'.py');compile(data,str(p),'exec')
    if p.exists():assert p.read_bytes()==data
    else:p.write_bytes(data)
    variants.append(dict(name='bridge_'+mode,path=p.relative_to(R).as_posix(),sha256=sha(data)))
variants.insert(0,dict(name='r2',path='submissions/release_v10_r2/main.py',sha256=sha(r2)))
spec=json.loads((D/'route_execution_design.json').read_text())
roster=[r for r in spec['roster'] if r['family'] in ('r2','aurax','dmitrii')]
roster.append(dict(path='research/herd_validation_20260928/route_raw_fixed10.py',family='current_route_proxy',panel='responsive_route_probe'))
seeds=spec['seeds'][:2];jobs=[]
for v in variants:
    for op in roster:
        for seed in seeds:
            for seat in (0,1):
                j=dict(candidate=v['path'],opponent=op['path'],family=op['family'],panel=op['panel'],seed=seed,seat=seat,candidate_sha256=v['sha256'],opponent_sha256=sha((R/op['path']).read_bytes()))
                j['id']=sha(json.dumps(j,sort_keys=True).encode())[:24];jobs.append(j)
(D/'bridge_jobs.json').write_text(json.dumps(jobs,indent=2))
(D/'bridge_design.json').write_text(json.dumps(dict(variants=variants,roster=roster,seeds=seeds,scope='Engineering probe only. Alternate production expert has not passed strength tests. Virtual R2 step1 adjusts only our known prepaid inventory/money; original environment is untouched.',core_hashes=dict(r2=sha(r2),new=sha(new))),indent=2))
print(json.dumps(dict(candidates=len(variants),cases=len(jobs))),flush=True)

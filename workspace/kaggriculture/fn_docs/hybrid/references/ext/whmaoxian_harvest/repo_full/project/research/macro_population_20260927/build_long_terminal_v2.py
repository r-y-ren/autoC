"""Extend the local, Apache-credited terminal simulator to legal empty SELL slots.
No evaluation gates are removed: physical deposits and overflow remain constrained.
"""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1];out=D/'long_terminal_v2';out.mkdir(exist_ok=True)
base=(R/'submissions/release_v10_r2/main.py').read_bytes()
assert hashlib.sha256(base).hexdigest()=='b35b5b09fbec059ab7cbd2ba67a9fbb6d3e467ef5262f3e2ddba592b3e50c1c4'
model=(R/'external/ahmed_nested1.py').read_text(encoding='utf-8')
old="        for order in market:\n            if not isinstance(order, list)"
assert model.count(old)==1
model=model.replace(old,"        for order in market:\n            if order==[]:continue\n            if not isinstance(order, list)")
assert model.count('(order[2] <= 0)')==1
model=model.replace('(order[2] <= 0)','(order[2] < 0)')
old="        for _, item, requested in action.get('market', []):"
assert model.count(old)==1
model=model.replace(old,"        for _, item, requested in (o for o in action.get('market', []) if o):")
tail=(D/'long_terminal_tail.py.txt').read_text(encoding='utf-8').replace('_PLANNER_NS','_LT_NS')
old="        if step<718 and (len(orders)!=9 or {o[1] for o in orders if len(o)>1}!=set(PRODUCTS) or any(len(o)!=3 or o[0]!='SELL' or type(o[2]) is not int or o[2]<100 for o in orders)):return None"
assert tail.count(old)==1
new="        if any(o and (len(o)!=3 or o[0]!='SELL' or o[1] not in PRODUCTS or type(o[2]) is not int or o[2]<0) for o in orders):return None"
tail=tail.replace(old,new)
namespace="\n_LT_NS=dict(_UNIT_NS)\nexec("+repr(model)+",_LT_NS)\n_LT_NS['shop_liquidation']=_parent_liquidate\n"
variants=[]
for name,start in [('control',712),('start712',712),('start708',708),('start704',704),('start700',700)]:
    constants=f'\n_LT_MODE={name!r}\n_LT_START={start}\n_LT_BUDGET=192\n_LT_PROPOSALS=12\n'
    data=base+namespace.encode()+constants.encode()+tail.encode();path=out/(name+'.py')
    compile(data,str(path),'exec')
    if path.exists():assert path.read_bytes()==data
    else:path.write_bytes(data)
    variants.append(dict(path=path.relative_to(R).as_posix(),name=name,sha256=hashlib.sha256(data).hexdigest()))
old_jobs=json.loads((D/'long_terminal_jobs.json').read_text());jobs=[]
lookup={v['name']:v for v in variants}
for old in old_jobs:
    item=lookup[Path(old['candidate']).stem]
    job=dict(old,candidate=item['path'],candidate_sha256=item['sha256']);job.pop('id')
    job['id']=hashlib.sha256(json.dumps(job,sort_keys=True).encode()).hexdigest()[:24];jobs.append(job)
(D/'long_terminal_v2_manifest.json').write_text(json.dumps(variants,indent=2))
(D/'long_terminal_v2_jobs.json').write_text(json.dumps(jobs,indent=2))
(D/'long_terminal_v2_model.py').write_text(model,encoding='utf-8')
(D/'long_terminal_v2_changes.json').write_text(json.dumps(dict(source='external/ahmed_nested1.py',source_sha256=hashlib.sha256((R/'external/ahmed_nested1.py').read_bytes()).hexdigest(),changes=['Permit legal empty market slots','Permit zero-quantity SELL instructions','Skip empty slots when simulating stock transitions'],source_notice='Retain the Apache-2.0 attribution and license notices from release_v10_r2.',strength_claim=False),indent=2))
print(json.dumps(dict(variants=len(variants),games=len(jobs),physical_dominance_kept=True)),flush=True)

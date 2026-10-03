"""Retain husbandry coverage while restoring short-cycle crop investment."""
from pathlib import Path
import hashlib,json,ast,random
D=Path(__file__).resolve().parent;R=D.parents[1]
base=(R/'submissions/release_v10_r2/main.py').read_bytes()
assert hashlib.sha256(base).hexdigest()=='b35b5b09fbec059ab7cbd2ba67a9fbb6d3e467ef5262f3e2ddba592b3e50c1c4'
helpers=(D/'dispatch.py.txt').read_text();original=(D/'route_dispatch.py.txt').read_text()
tail=original
old="cost=_vr_cost(candidate,jobs,starts[actor])"
assert tail.count(old)==1;tail=tail.replace(old,"cost=_vr_insert_cost(route,jobs,starts[actor],index,offset,costs[actor])")
old="ops,value,need=_dp_bundle(tile,day,hour,prices,crop)\n            if not ops:continue"
new="ops,value,need=_dp_bundle(tile,day,hour,prices,crop)\n            if prices['FERTILIZER']<_VR_MIN_FERT and ['COLLECT_FERTILIZER'] in ops:\n                ops.remove(['COLLECT_FERTILIZER']);value-=prices['FERTILIZER']\n            if not ops:continue"
assert tail.count(old)==1;tail=tail.replace(old,new)
cost_source=(D/'route_cost.py.txt').read_text()
ns={'_DP_HOME':((4,4),(5,4),(4,5),(5,5))}
for source,names in [(helpers,('_dp_dist','_dp_home')),(original,('_vr_cost',)),(cost_source,('_vr_insert_cost',))]:
    tree=ast.parse(source)
    for node in tree.body:
        if isinstance(node,ast.FunctionDef) and node.name in names:exec(ast.get_source_segment(source,node),ns)
rng=random.Random(927);checks=0
for _ in range(100):
    jobs=[dict(xy=(rng.randrange(10),rng.randrange(10)),ops=[['PASS']]*rng.randint(1,4),need={i:rng.randrange(2) for i in ('WHEAT','FERTILIZER')}) for _ in range(9)]
    route=list(range(rng.randrange(8)));start=(4,4);current=ns['_vr_cost'](route,jobs,start)
    for offset in range(len(route)+1):
        assert ns['_vr_insert_cost'](route,jobs,start,8,offset,current)==ns['_vr_cost'](route[:offset]+[8]+route[offset:],jobs,start);checks+=1
(D/'route_cost_checks.json').write_text(json.dumps(dict(checks=checks,passed=True)))
old="            if not ops:continue\n            essential=0"
new="""            if not ops:continue
            if crop is not None and isinstance(tile,dict) and tile.get('crop') and ['HARVEST'] in ops:
                exhausted=tile['crop'] not in ('TOMATO','STRAWBERRY') or tile.get('max_lifespan_step',-1)>=0
                if exhausted:
                    if tile['crop'] in ('TOMATO','STRAWBERRY'):ops.append(['DIG'])
                    ops.append(['PLANT',crop]);need['seed:'+crop]=1
                    value+=_DP_PLANT_WEIGHT*max(0,_DP_CROPS[crop][2]*prices[crop]-_DP_CROPS[crop][3])
            essential=0"""
assert tail.count(old)==1;tail=tail.replace(old,new)
manifest=[]
for workers in (12,13):
    for weight in (1.0,2.0):
        for minimum in (20,40):
            name=f'routed2_w{workers}_p{int(weight)}_fert{minimum}'
            constants=f'\n_DP_START=16\n_DP_WORKERS={workers}\n_DP_DELIVERY=16\n_DP_PLANT_WEIGHT={weight}\n_DP_FEED_WEIGHT=1\n_DP_DISTANCE_POWER=1.0\n_VR_START=16\n_VR_WORKERS={workers}\n_VR_FEED=200\n_VR_CARE=0\n_VR_MIN_FERT={minimum}\n'
            code=base+constants.encode()+helpers.encode()+cost_source.encode()+tail.encode()
            path=D/(name+'.py');assert not path.exists();compile(code,str(path),'exec');path.write_bytes(code)
            manifest.append(dict(name=name,path=path.relative_to(R).as_posix(),sha256=hashlib.sha256(code).hexdigest()))
base_path='submissions/release_v10_r2/main.py'
cases=[j for j in json.loads((D/'smoke_jobs.json').read_text()) if j['candidate']==base_path];jobs=[]
for item in manifest:
    for case in cases:
        job=dict(case,candidate=item['path'],candidate_sha256=item['sha256']);job.pop('id')
        job['id']=hashlib.sha256(json.dumps(job,sort_keys=True).encode()).hexdigest()[:24];jobs.append(job)
(D/'routed_v2_manifest.json').write_text(json.dumps(manifest,indent=2))
(D/'routed_v2_jobs.json').write_text(json.dumps(jobs,indent=2))
print(json.dumps(dict(variants=len(manifest),games=len(jobs),cost_checks=checks)),flush=True)

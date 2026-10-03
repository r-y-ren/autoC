"""Immutable full-game candidates for compatible whole production routes."""
from pathlib import Path
import contextlib,hashlib,io,json,sys
D=Path(__file__).resolve().parent;R=D.parents[1]
sys.path.insert(0,str(R/'research/v10_rebuild_20260926'))
with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
    import fast_arena as fa
sha=lambda b:hashlib.sha256(b).hexdigest();base='submissions/release_v10_r2/main.py'
raw=(R/base).read_bytes();assert sha(raw)=='b35b5b09fbec059ab7cbd2ba67a9fbb6d3e467ef5262f3e2ddba592b3e50c1c4'
entry=fa.load(base);routes=entry.__globals__['_IMPL'].chassis.routes
physical=lambda a:(a.get('farmer'),a.get('hands',[]))
choices=[key for key,tape in routes.items() if key!=2 and all(physical(tape[t])==physical(routes[0][t]) for t in range(144))]
features=(D/'route_features.py').read_text(encoding='utf-8')
for a,b in [('PRODUCTS','_K29_RF_PRODUCTS'),('TYPES','_K29_RF_TYPES'),('SHOPS','_K29_RF_SHOPS'),('route_features','_k29_route_features')]:features=features.replace(a,b)
tail=(D/'route_choice_tail.txt').read_text(encoding='utf-8')
tail=tail.replace('    if 144<=step<648:',"    if step==144:\n        _K29_ROUTE_REPORT['features']=_k29_route_features(observation)\n        _K29_ROUTE_REPORT['native_route']=selected\n    if 144<=step<648:")
folder=D/'route_candidates';folder.mkdir(exist_ok=True);variants=[]
for route in choices:
    data=raw+('\n_K29_FORCED_ROUTE='+repr(route)+'\n'+features+'\n'+tail).encode()
    path=folder/f'route_{route}.py';compile(data,str(path),'exec')
    if path.exists():assert path.read_bytes()==data
    else:path.write_bytes(data)
    variants.append(dict(name=f'route_{route}',route=route,path=path.relative_to(R).as_posix(),sha256=sha(data)))
wide=json.loads((D/'herd_extended_design.json').read_text());archives=json.loads((D/'archived_opponents.json').read_text())
roster=[p for p in wide['roster'] if p['family'] in ('fieldcraft','pipe16','r2')]+[p for p in archives if p['family']=='archived_05']
seeds=[1799657451]+wide['seeds'][:2];jobs=[]
all_variants=[dict(name='r2',route=None,path=base,sha256=sha(raw))]+variants
for v in all_variants:
    for rival in roster:
        for seed in seeds:
            for seat in (0,1):
                j=dict(candidate=v['path'],opponent=rival['path'],family=rival['family'],panel=rival['panel'],seed=seed,seat=seat,candidate_sha256=v['sha256'],opponent_sha256=sha((R/rival['path']).read_bytes()),forced_route=v['route'])
                j['id']=sha(json.dumps(j,sort_keys=True).encode())[:24];jobs.append(j)
for name,data in [('route_choice_jobs.json',jobs),('route_choice_design.json',dict(variants=all_variants,roster=roster,seeds=seeds,compatible_routes=choices,scope='Full-game development route search; all candidates preserve step0..143 and native terminal routing.'))]:
    p=D/name;s=json.dumps(data,indent=2)
    if p.exists():assert p.read_text()==s
    else:p.write_text(s)
print(json.dumps(dict(routes=len(choices),jobs=len(jobs))),flush=True)

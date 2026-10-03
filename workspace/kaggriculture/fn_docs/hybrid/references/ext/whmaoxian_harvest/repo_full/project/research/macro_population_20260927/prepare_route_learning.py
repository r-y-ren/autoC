"""Compare complete farm routes across new worlds for a small shop-conditioned policy.
This prepares local simulated-game experiments only; it does not submit to Kaggle.
"""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1]
variants=json.loads((D/'route_population.json').read_text())
keep={None,0,9,12,100,101,110,123,128}
variants=[v for v in variants if v['route'] in keep]
roster=json.loads((D/'roster.json').read_text())
known=set(sum(json.loads((D/'worlds.json').read_text()).values(),[]))
known.update(json.loads((D/'route_design.json').read_text())['seeds'])
seeds=[];counter=0
while len(seeds)<48:
    seed=int.from_bytes(hashlib.sha256(f'route-context-study-20260927-{counter}'.encode()).digest()[:4],'big')%2000000000;counter+=1
    if seed not in known and seed not in seeds:seeds.append(seed)
jobs=[]
for variant in variants:
    for opponent in roster:
        for seed in seeds:
            for seat in (0,1):
                j=dict(candidate=variant['path'],opponent=opponent['path'],family=opponent['family'],panel=opponent['panel'],seed=seed,seat=seat)
                for key in ('candidate','opponent'):j[key+'_sha256']=hashlib.sha256((R/j[key]).read_bytes()).hexdigest()
                j['id']=hashlib.sha256(json.dumps(j,sort_keys=True).encode()).hexdigest()[:24];jobs.append(j)
manifest=D/'route_learning_jobs.json';assert not manifest.exists()
manifest.write_text(json.dumps(jobs,indent=2))
(D/'route_learning_design.json').write_text(json.dumps(dict(seeds=seeds,variants=variants,roster=roster,total_games=len(jobs),feature_scope='First two already-opened shops only.',scope='Development for route selection, not final validation.'),indent=2))
print(json.dumps(dict(worlds=len(seeds),routes=len(variants),games=len(jobs))),flush=True)

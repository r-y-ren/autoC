"""Offline spatial routing only; no game outcome or held-out seed is used."""
import math
import random
import json
import argparse
from pathlib import Path
parser=argparse.ArgumentParser()
parser.add_argument('--fert3',action='store_true')
parser.add_argument('--harvest5',action='store_true')
args=parser.parse_args()
targets=[(x,y) for y in (5,6,7) for x in range(5,10)]+[(x,8) for x in range(6,10)]
starts=[(4,4),(5,4),(4,5),(5,5)]
if args.fert3:starts=[(5,5),(4,5),(5,5)]
if args.harvest5:starts=[(5,5),(4,5),(5,5),(4,5),(5,5)]
n=len(starts)
def dist(a,b):return abs(a[0]-b[0])+abs(a[1]-b[1])
def costs(routes):
    return [dist(st,p[0])+sum(dist(a,b) for a,b in zip(p,p[1:]))+2*len(p)+(0 if args.fert3 else min(dist(p[-1],h) for h in starts))+1 for st,p in zip(starts,routes)]
def score(routes):
    v=costs(routes)
    return 100*max(v)+sum(v)
rng=random.Random(772903)
best=None
for restart in range(12):
    initial=list(targets);rng.shuffle(initial)
    paths=[initial[i::n] for i in range(n)]
    v=score(paths)
    for k in range(16000):
        p=[list(a) for a in paths]
        a,b=rng.sample(range(n),2)
        i=rng.randrange(len(p[a]));j=rng.randrange(len(p[b]))
        if rng.random()<0.3 and len(p[a])>1:p[b].insert(j,p[a].pop(i))
        elif rng.random()<0.8:p[a][i],p[b][j]=p[b][j],p[a][i]
        else:
            a=rng.randrange(n);i,j=sorted(rng.sample(range(len(p[a])+1),2));p[a][i:j]=reversed(p[a][i:j])
        w=score(p);temp=max(0.15,50*(1-k/16000))
        if w<v or rng.random()<math.exp(min(0,(v-w)/temp)):paths,v=p,w
        if best is None or v<best[0]:best=v,paths,costs(paths)
report={'objective':('all 19 WATER+FERTILIZE including pickup' if args.fert3 else 'all 19 WATER+HARVEST and mandatory return+PLACE'),'starts':starts,'paths':best[1],'durations':best[2],'score':best[0]}
Path('research/round8').mkdir(parents=True,exist_ok=True)
Path('research/round8/production_spatial_routes'+('_fert3' if args.fert3 else ('_harvest5' if args.harvest5 else ''))+'.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report))

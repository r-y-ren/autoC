"""Paired, world-clustered reports; no rating extrapolation from fixed programs."""
from pathlib import Path
import collections, json, random, statistics, sys
D=Path(__file__).resolve().parent

def load(path):
 return [json.loads(line) for line in Path(path).read_text(encoding='utf-8').splitlines()]
def point(r):
 return 1.0 if r['margin']>0 else 0.0 if r['margin']<0 else 0.5
def desc(rows):
 good=[r for r in rows if r.get('valid')]
 values=sorted(r['margin'] for r in good)
 return dict(games=len(rows),invalid=len(rows)-len(good),
  wins=sum(r['margin']>0 for r in good),ties=sum(r['margin']==0 for r in good),
  losses=sum(r['margin']<0 for r in good),points=statistics.mean(map(point,good)) if good else None,
  mean_margin=statistics.mean(values) if values else None,
  p10=values[int(.1*(len(values)-1))] if values else None,worst=values[0] if values else None)
def paired(candidate,baseline):
 key=lambda r:(r['opponent_sha256'],r['seed'],r['seat'])
 index={key(r):r for r in baseline}; pairs=[(r,index[key(r)]) for r in candidate if key(r) in index]
 if len(pairs)!=len(candidate) or any(not a.get('valid') or not b.get('valid') for a,b in pairs):
  return dict(complete=False,matched=len(pairs),expected=len(candidate))
 worlds=collections.defaultdict(list)
 for a,b in pairs:worlds[a['seed']].append(point(a)-point(b))
 samples=[statistics.mean(group) for group in worlds.values()]
 rng=random.Random(20260926)
 boot=sorted(statistics.mean(rng.choices(samples,k=len(samples))) for _ in range(4000))
 return dict(complete=True,worlds=len(worlds),games=len(pairs),point_gain=statistics.mean(samples),
  world_bootstrap_95=[boot[100],boot[3899]],mean_margin_gain=statistics.mean(a['margin']-b['margin'] for a,b in pairs),
  shop_sequences_changed=sum(a['shops']!=b['shops'] for a,b in pairs))
def report(path):
 rows=load(path); result={}; names=sorted({r['candidate'] for r in rows})
 assert len({r['id'] for r in rows})==len(rows),'Duplicate completed jobs'
 for name in names:
  candidate=[r for r in rows if r['candidate']==name]; panels={}
  for panel in sorted({r['panel'] for r in candidate}):
   subset=[r for r in candidate if r['panel']==panel]
   item={'overall':desc(subset),'families':{f:desc([r for r in subset if r['family']==f]) for f in sorted({r['family'] for r in subset})}}
   for version in ('v9','v10'):
    baseline=[r for r in rows if r['candidate']==f'submissions/release_{version}/main.py' and r['panel']==panel]
    if baseline:item['versus_'+version]=paired(subset,baseline)
   panels[panel]=item
  result[name]=panels
 out=Path(path).with_suffix('.paired.json'); out.write_text(json.dumps(result,indent=2),encoding='utf-8')
 for name,panels in result.items():
  label=name.split('/continuation/')[-1] if '/continuation/' in name else name
  print(label,{p:{'games':v['overall']['games'],'wins':v['overall']['wins'],'ties':v['overall']['ties'],
   'margin':round(v['overall']['mean_margin'] or 0,1),'v10_gain':v.get('versus_v10',{}).get('point_gain')} for p,v in panels.items()},flush=True)
 return result
if __name__=='__main__':report(sys.argv[1])

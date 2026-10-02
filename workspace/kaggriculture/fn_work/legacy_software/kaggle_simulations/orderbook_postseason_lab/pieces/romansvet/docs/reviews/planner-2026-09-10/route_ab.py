import os,sys,inspect,json,csv
from pathlib import Path
import numpy as np
ROOT=Path('/mnt/e/_work/kaggriculture3');WT=ROOT/'.claude/worktrees/ship-pair'
os.chdir(WT);sys.path[:0]=[str(WT/'src'),str(WT/'scripts')]
os.environ['JAX_PLATFORMS']='cpu'
os.environ['KAGG3_TOWN_SCHEDULE']=str(ROOT/'S/band2100p/town_schedules.json')
from kagg3.core import plan as P
import eval_vs_baselines as EV
source=inspect.getsource(P._plan_and_stats)
source=source.replace('    for _ in range(ADMIT_ROUNDS):','    best_route = None\n    best_key = None\n    for _ in range(ADMIT_ROUNDS):',1)
needle='        n_admit = (n_admit - xp.sum((admitted & ~covered).astype(i32), dtype=i32)).astype(i32)'
assert source.count(needle)==1
source=source.replace(needle,'''        key = (xp.sum((covered & (d.tier >= 2)).astype(i32)),
               xp.sum((covered & (d.tier == 1)).astype(i32)),
               xp.sum(xp.where(covered, d.tile_value, 0), dtype=i32))
        candidate = (route_op, route_a, route_q, blk, covered, n_pick, lead,
                     early, bank_mask, admitted)
        if best_route is None:
            best_route, best_key = candidate, key
        else:
            better = ((key[0] > best_key[0])
                      | ((key[0] == best_key[0]) & (key[1] > best_key[1]))
                      | ((key[0] == best_key[0]) & (key[1] == best_key[1])
                         & (key[2] > best_key[2])))
            best_route = tuple(xp.where(better, a, b) for a, b in zip(candidate, best_route))
            best_key = tuple(xp.where(better, a, b) for a, b in zip(key, best_key))
'''+needle+'''
    (route_op, route_a, route_q, blk, covered, n_pick, lead,
     early, bank_mask, admitted) = best_route
''',1)
exec(compile(source,P.__file__,'exec'),P.__dict__)
rows=list(csv.DictReader((ROOT/'S/lossflip/g940pair_topb.csv').open()))
results=[]
for ep in ['107233845','107244033']:
 for seat in [0,1]:
  r=next(r for r in rows if ep in r['opponent'] and int(r['seat'])==seat)
  res=EV._play((int(r['seed']),str(ROOT/r['opponent']),seat,str(ROOT/'artifacts/kagg2_games/thetas/flow172_g940.npy'),False,None,None))
  row={'episode':ep,'seat':seat,'base_mine':float(r['mine']),'base_theirs':float(r['theirs']),'mine':res[1],'theirs':res[2],
       'margin_delta':(res[1]-res[2])-(float(r['mine'])-float(r['theirs']))}
  results.append(row);print(json.dumps(row),flush=True)
  Path('/tmp/kagg3-planner-review/route_ab.json').write_text(json.dumps(results,indent=2))

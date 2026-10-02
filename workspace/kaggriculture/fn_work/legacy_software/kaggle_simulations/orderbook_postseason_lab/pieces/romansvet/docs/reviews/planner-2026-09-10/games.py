import os,sys,json,csv,time
from pathlib import Path
import numpy as np
ROOT=Path('/mnt/e/_work/kaggriculture3')
WT=ROOT/'.claude/worktrees/ship-pair'
os.chdir(WT)
sys.path[:0]=[str(WT/'src'),str(WT/'scripts')]
os.environ['JAX_PLATFORMS']='cpu'
os.environ['KAGG3_TOWN_SCHEDULE']=str(ROOT/'S/band2100p/town_schedules.json')
from kagg3.core import plan as P,ops as O
import eval_vs_baselines as EV

records=[];cap=[]
def profile(frame,event,arg):
    if event=='return' and frame.f_code.co_filename==P.__file__:
        if frame.f_code.co_name in ('_derive','_plan_and_stats'):
            cap.append((frame.f_code.co_name,dict(frame.f_locals)))
        elif frame.f_code.co_name=='_routes':
            d=frame.f_back.f_locals['d']
            covered=arg[4]
            cap.append(('round',{'covered_value':int(np.sum(d.tile_value[covered])),
                                 'covered_count':int(covered.sum()),
                                 'tier2':int(np.sum(covered & (d.tier==2))),
                                 'tier1':int(np.sum(covered & (d.tier==1)))}))

original=P.build_day
def instrument(xp,view,macro,price_table=None):
    cap.clear();start=time.perf_counter();sys.setprofile(profile)
    try:out=original(xp,view,macro,price_table)
    finally:sys.setprofile(None)
    e=[v for n,v in cap if n=='_plan_and_stats'][-1]
    ds=[v for n,v in cap if n=='_derive'];d=ds[-1]
    rounds=[v for n,v in cap if n=='round']
    seedops=[]
    for c in range(5):seedops.append(int(np.sum((out[0]==O.OP_PLANT)&(out[1]==c))))
    purchases=np.array(d['seed_buy']);cons=np.array(seedops)
    records.append({'episode':episode,'seat':seat,'day':int(view.day),'money':int(view.money),
      'land_cost':int(d['land_cost']),'land_value':int(d['land_value']),'land_bias':int(macro.land_bias),
      'buy_land':int(d['buy_land']),'hires':int(e['n_hire']),'forward_days':int(macro.forward_days),
      'd0_tasks':int(e['d0'].task.sum()),'d_tasks':int(e['d'].task.sum()),
      'seed_buy':purchases.tolist(),'seed_ops':seedops,'seed_stock':view.seeds.tolist(),
      'excess_seed_buy':np.maximum(purchases-np.maximum(cons-view.seeds,0),0).tolist(),
      'wheat_reserved':int(e['wheat_reserved']),'routed_feeds':int(e['blk'][0].sum()),
      'fert_reserved':int(e['fert_reserved']),'routed_fert':int(e['blk'][1].sum()),
      'rounds':rounds,'seconds':round(time.perf_counter()-start,4)})
    return out
P.build_day=instrument
rows=list(csv.DictReader((ROOT/'S/lossflip/g940pair_topb.csv').open()))
results=[]
for episode in ['107233845','107244033']:
    for seat in [0,1]:
        r=next(r for r in rows if episode in r['opponent'] and int(r['seat'])==seat)
        opponent=str(ROOT/r['opponent'])
        res=EV._play((int(r['seed']),opponent,seat,str(ROOT/'artifacts/kagg2_games/thetas/flow172_g940.npy'),False,None,None))
        results.append({'episode':episode,'seat':seat,'result':res,'saved_mine':r['mine'],'saved_theirs':r['theirs']})
        print('GAME',episode,seat,res,flush=True)
        Path('/tmp/kagg3-planner-review/games.json').write_text(json.dumps({'results':results,'days':records},indent=2))
print('DONE',len(records),flush=True)

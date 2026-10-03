"""Run a game between two agent files with transaction logging. usage: glog.py a.py b.py seed [items]"""
import sys,io,contextlib,collections,os
with contextlib.redirect_stdout(io.StringIO()):
    from kaggle_environments import make
    from kaggle_environments.agent import get_last_callable
    import kaggle_environments.envs.kaggriculture.kaggriculture as K
LOG=[];CUR={}
_opm=K._process_market
def pm(state,env):
    CUR['f']=state[0].observation.farms;CUR['t']=state[0].observation['step'];return _opm(state,env)
K._process_market=pm
_oc=K._commit_unit
def cu(op,item,price,farm,private,market,cap=100):
    ok=_oc(op,item,price,farm,private,market,cap)
    if ok:
        p=[i for i,f in enumerate(CUR['f']) if f is farm][0]
        LOG.append((CUR['t'],p,op,item,price))
    return ok
K._commit_unit=cu
_od=K._drop_inventories_to_shed
LOST=collections.Counter()
def dropx(private,cap):
    before=sum(sum(v.values()) for v in private['inventories'])+sum(private['shed'].values())
    _od(private,cap)
    after=sum(private['shed'].values())
    LOST[id(private)]+=before-after
K._drop_inventories_to_shed=dropx
def run(a,b,seed):
    LOG.clear()
    with contextlib.redirect_stdout(io.StringIO()):
        ents=[get_last_callable(open(p,encoding='utf-8').read(),path=os.path.abspath(p)) for p in (a,b)]
    env=make('kaggriculture',configuration={'seed':seed,'episodeSteps':720});env.run(ents)
    fin=[env.steps[-1][i].observation.farms[i]['money'] for i in (0,1)]
    return env,fin
if __name__=='__main__':
    a,b,seed=sys.argv[1],sys.argv[2],int(sys.argv[3])
    env,fin=run(a,b,seed)
    print('final',fin,'lost at night',[LOST[id(env.state[i].observation.private)] for i in (0,1)], 'lostcounter',dict(LOST))
    agg=[collections.defaultdict(lambda:[0,0]) for _ in range(2)]
    for t,p,op,it,pr in LOG:
        agg[p][op+':'+it][0]+=1;agg[p][op+':'+it][1]+=pr
    for k in sorted(set(agg[0])|set(agg[1])):
        x,y=agg[0][k],agg[1][k]
        print(f'{k:22s} {x[0]:5d} {x[1]:8d} ({x[1]/max(1,x[0]):6.1f})   {y[0]:5d} {y[1]:8d} ({y[1]/max(1,y[0]):6.1f})')
    fs=env.steps[-1]
    print('final shed',[dict(fs[i].observation.private['shed']) for i in (0,1)])

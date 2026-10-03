import sys,collections
import kaggle_environments.envs.kaggriculture.kaggriculture as K
from concurrent.futures import ProcessPoolExecutor
def one(seed):
    LOST=collections.Counter();CALLS=[0]
    _od=K._drop_inventories_to_shed
    def dropx(private,cap):
        before=collections.Counter(private['shed'])
        for inv in private['inventories']:
            for k,v in inv.items(): before[k]+=v
        _od(private,cap)
        after=collections.Counter(private['shed'])
        if CALLS[0]%2==0:
            for k in before:
                if before[k]>after[k]: LOST[k]+=before[k]-after[k]
        CALLS[0]+=1
    K._drop_inventories_to_shed=dropx
    from dbg import run
    env=run(sys.argv[1],'cand/r2.py',seed)
    prices=env.steps[-1][0].observation.market['prices']
    val=sum(v*prices.get(k,0) for k,v in LOST.items())
    return seed,dict(LOST),val
if __name__=='__main__':
    with ProcessPoolExecutor(16) as p:
        res=list(p.map(one,range(1000,1016)))
    for r in res: print(r)
    print('mean lost value',sum(r[2] for r in res)/len(res))

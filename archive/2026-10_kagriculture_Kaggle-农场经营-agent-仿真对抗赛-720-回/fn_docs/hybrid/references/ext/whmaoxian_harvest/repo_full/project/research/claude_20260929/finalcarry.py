import sys,collections
from concurrent.futures import ProcessPoolExecutor
def one(seed):
    from dbg import run
    env=run(sys.argv[1],'cand/r2.py',seed)
    o=env.steps[-1][0].observation
    c=collections.Counter()
    for i in o.private['inventories']:
        for k,v in i.items(): c[k]+=v
    sh={k:v for k,v in o.private['shed'].items() if v}
    pr=o.market['prices']
    return seed,dict(c),sh,sum(v*pr.get(k,0) for k,v in c.items())+sum(v*pr.get(k,0) for k,v in sh.items() if k in pr)
if __name__=='__main__':
    with ProcessPoolExecutor(16) as p:
        res=list(p.map(one,range(1000,1016)))
    for r in res: print(r)
    print('mean unsold value',sum(r[3] for r in res)/len(res))

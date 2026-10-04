import sys,collections
from concurrent.futures import ProcessPoolExecutor
def one(seed):
    from dbg import run
    from health import report
    env=run(sys.argv[1],'cand/r2.py',seed)
    fin,esc,dead,ops=report(env,verbose=False)
    o=env.steps[718][0].observation
    carried=sum(sum(i.values()) for i in o.private['inventories'])
    field=sum(t.get('yield_units',0) for row in o.farms[0]['tiles'] for t in row if isinstance(t,dict))
    seeds=dict(o.private['seeds'])
    return seed,dict(esc),dict(dead),carried,field,{k:v for k,v in seeds.items() if v},ops.get('PASS',0)
if __name__=='__main__':
    with ProcessPoolExecutor(16) as p:
        for r in p.map(one,range(1000,1016)): print(r)

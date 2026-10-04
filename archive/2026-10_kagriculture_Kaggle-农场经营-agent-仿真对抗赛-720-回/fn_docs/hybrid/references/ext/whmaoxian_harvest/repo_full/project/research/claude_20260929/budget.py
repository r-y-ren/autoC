import sys,collections
import glog
seeds=[int(x) for x in sys.argv[3].split(',')]
T0=int(sys.argv[4]) if len(sys.argv)>4 else 288
tot={}
for a,b in ((sys.argv[1],sys.argv[2]),(sys.argv[2],sys.argv[2])):
    c=collections.Counter()
    for sd in seeds:
        env,fin=glog.run(a,b,sd)
        for t,p,op,it,pr in glog.LOG:
            if p!=0 or t<T0: continue
            if op=='SELL': c['rev:'+('PREMIUM' if it in ('STRAWBERRY','MILK','WOOL','MELON') else it)]+=pr
            else: c['cost:'+op+(':'+it if op=='BUY_PRODUCT' else '')]+=pr
        c['final']+=fin[0]
        # hires cost
        for t in range(T0,720):
            o=env.steps[t][0].observation
            if o.hour==23:
                n=o.farms[0]['hires_today']; c['cost:HIRES']+=sum(glog_fib(k) for k in range(n)) if False else 0
    tot['A' if a!=b else 'R2']={k:v/len(seeds) for k,v in c.items()}
def fmt(d): return {k:int(v) for k,v in sorted(d.items())}
for k,v in tot.items(): print(k,fmt(v))

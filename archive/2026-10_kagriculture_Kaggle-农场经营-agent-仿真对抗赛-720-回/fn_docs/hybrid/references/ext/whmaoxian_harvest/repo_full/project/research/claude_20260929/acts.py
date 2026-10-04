import sys,io,contextlib,os
from dbg import run
a,b,seed,t0,t1=sys.argv[1],sys.argv[2],int(sys.argv[3]),int(sys.argv[4]),int(sys.argv[5])
env=run(a,b,seed)
for t in range(t0,t1):
    o=env.steps[t][0].observation;act=env.steps[t+1][0].action
    f=o.farms[0]
    print(f"t{t} d{o.day}h{o.hour} ${f['money']:.0f} units={[tuple(f['farmer'])]+[tuple(h) for h in f['hands']]} inv={o.private['inventories']} shed={ {k:v for k,v in o.private['shed'].items() if v} }")
    print('    ',act)

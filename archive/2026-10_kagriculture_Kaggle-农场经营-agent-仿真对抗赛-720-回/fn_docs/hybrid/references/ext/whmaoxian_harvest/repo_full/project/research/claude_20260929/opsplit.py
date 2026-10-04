import sys,collections
from dbg import run
T0=int(sys.argv[4]) if len(sys.argv)>4 else 288
for name,(a,b) in (('A',(sys.argv[1],sys.argv[2])),('B',(sys.argv[2],sys.argv[2]))):
    env=run(a,b,int(sys.argv[3]))
    c=collections.Counter();hires=0
    for t in range(T0,719):
        act=env.steps[t+1][0].action or {}
        o=env.steps[t][0].observation
        if o.hour==23: hires+=o.farms[0]['hires_today']
        for cmd in [act.get('farmer')]+list(act.get('hands') or []):
            if not cmd: continue
            op=cmd[0]
            c['MOVE' if op in ('NORTH','SOUTH','EAST','WEST') else op]+=1
    tot=sum(c.values())
    print(name,'unit-turns',tot,'hand-days',hires,{k:v for k,v in sorted(c.items(),key=lambda x:-x[1])})

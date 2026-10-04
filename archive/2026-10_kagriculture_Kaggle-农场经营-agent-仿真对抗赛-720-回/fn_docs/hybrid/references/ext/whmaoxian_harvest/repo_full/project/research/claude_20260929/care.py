import sys,collections
from dbg import run
env=run(sys.argv[1],sys.argv[2],int(sys.argv[3]))
c=collections.Counter()
for t in range(len(env.steps)):
    o=env.steps[t][0].observation
    if o.hour!=23: continue
    for row in o.farms[0]['tiles']:
        for tl in row:
            if isinstance(tl,dict) and tl.get('animal'):
                a=tl['animal']; c[a+':days']+=1
                c[a+':fed']+=tl['fed_today']; c[a+':cared']+=tl['cared_today']; c[a+':fedcared']+=tl['fed_today'] and tl['cared_today']
                c[a+':fert_left']+=tl['fertilizer_available']
print(dict(sorted(c.items())))

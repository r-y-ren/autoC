import sys,collections
from dbg import run
for name,(a,b) in (('A',(sys.argv[1],sys.argv[2])),('B',(sys.argv[2],sys.argv[2]))):
    env=run(a,b,int(sys.argv[3]))
    c=collections.Counter();wheat_ages=collections.Counter()
    for t in range(288,len(env.steps)):
        o=env.steps[t][0].observation;f=o.farms[0]
        for y in range(10):
            for x in range(10):
                tl=f['tiles'][y][x]
                if tl is None: c['empty']+=1
                elif tl=='LOCKED': pass
                elif tl['kind']=='WEED': c['weed']+=1
                elif tl['kind']=='PLANT':
                    c[tl['crop']]+=1
                    if tl['crop']=='WHEAT' and o.hour==23: wheat_ages[o.day-tl['planted_day']]+=1
                else: c[tl.get('animal') or 'struct']+=1
    print(name,{k:round(v/24,1) for k,v in c.items()},'wheat ages at h23',sorted(wheat_ages.items()))

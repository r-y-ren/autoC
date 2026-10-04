import sys,collections
from dbg import run
for name,(a,b) in (('A',(sys.argv[1],sys.argv[2])),('B',(sys.argv[2],sys.argv[2]))):
    env=run(a,b,int(sys.argv[3]))
    for t in (696,708,718):
        o=env.steps[t][0].observation;f=o.farms[0]
        c=collections.Counter()
        for row in f['tiles']:
            for tl in row:
                if isinstance(tl,dict) and tl.get('yield_units',0)>0: c[tl.get('crop') or tl.get('animal')]+=tl['yield_units']
                if isinstance(tl,dict) and tl.get('kind')=='PLANT' and tl.get('yield_units',0)==0: c['zero:'+tl['crop']]+=1
        carried=sum(sum(i.values()) for i in o.private['inventories'])
        print(name,'t',t,'field yield',dict(c),'carried',carried,'shed',sum(o.private['shed'].values()))

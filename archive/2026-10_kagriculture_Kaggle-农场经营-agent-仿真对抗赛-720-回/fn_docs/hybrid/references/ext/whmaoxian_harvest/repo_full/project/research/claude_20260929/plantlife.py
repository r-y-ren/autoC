import sys,collections
from dbg import run
def life(env,crop='STRAWBERRY',seat=0):
    plants={}  # (x,y,planted_day)->harvested
    for t in range(len(env.steps)-1):
        o=env.steps[t][seat].observation;f=o.farms[seat]
        act=env.steps[t+1][seat].action or {}
        units=[tuple(f['farmer'])]+[tuple(h) for h in f['hands']]
        cmds=[act.get('farmer')]+list(act.get('hands') or [])
        for y in range(10):
            for x in range(10):
                tl=f['tiles'][y][x]
                if isinstance(tl,dict) and tl.get('crop')==crop: plants.setdefault((x,y,tl['planted_day']),[0,0])
        for pos,c in zip(units,cmds):
            if c and c[0]=='HARVEST':
                tl=f['tiles'][pos[1]][pos[0]]
                if isinstance(tl,dict) and tl.get('crop')==crop:
                    plants[(pos[0],pos[1],tl['planted_day'])][0]+=tl['yield_units']
            if c and c[0]=='FERTILIZE':
                tl=f['tiles'][pos[1]][pos[0]]
                if isinstance(tl,dict) and tl.get('crop')==crop:
                    plants[(pos[0],pos[1],tl['planted_day'])][1]+=1
    return plants
for name,(a,b) in (('A',(sys.argv[1],sys.argv[2])),('B',(sys.argv[2],sys.argv[2]))):
    env=run(a,b,int(sys.argv[3]))
    p=life(env)
    hist=collections.Counter(v[0] for v in p.values())
    print(name,'plants',len(p),'total',sum(v[0] for v in p.values()),'fert',sum(v[1] for v in p.values()),'hist',sorted(hist.items()))
    print('   by planted day',sorted(collections.Counter(k[2] for k in p).items()))

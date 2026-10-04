import sys,collections
from anal import load
def ops(eid):
    g=load(eid);names=g['info']['TeamNames']
    for p in range(2):
        c=collections.Counter();turns=0
        for t in range(719):
            o=g['steps'][t][p]['observation'];f=o['farms'][p]
            a=g['steps'][t+1][p]['action'] or {}
            units=[(a.get('farmer') or ['PASS'],f['farmer'])]+list(zip(a.get('hands') or [],f['hands']))
            for act,pos in units:
                turns+=1
                if not act: continue
                op=act[0]
                if op in ('NORTH','SOUTH','EAST','WEST'): c['MOVE']+=1;continue
                tile=f['tiles'][pos[1]][pos[0]] if pos else None
                what=''
                if isinstance(tile,dict): what=tile.get('crop') or tile.get('animal') or tile['kind']
                if op in('FERTILIZE','HARVEST','WATER','FEED','CARE','COLLECT_FERTILIZER','PLANT'): c[op+':'+str(what)[:5]]+=1
                else: c[op]+=1
        print(names[p][:20],'unit-turns',turns,'reward',g['rewards'][p])
        print('  ',sorted(c.items(),key=lambda x:-x[1]))
for e in sys.argv[1:]: ops(int(e))

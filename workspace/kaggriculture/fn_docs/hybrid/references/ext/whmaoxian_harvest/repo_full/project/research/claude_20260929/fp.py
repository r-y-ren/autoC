import json,gzip,sys,collections
from anal import load,tilecount
def fp(eid):
    g=load(eid);names=g['info']['TeamNames'];steps=g['steps']
    out=[]
    for p in range(2):
        money={};land={};hires=collections.Counter();tiles={};sold=collections.Counter()
        for t in range(len(steps)):
            o=steps[t][p]['observation'];f=o['farms'][p];d=o['day']
            if o['hour']==23: hires[d]=f['hires_today']
            if o['hour']==0: money[d]=int(f['money'])
            for q in f['unlocked_quadrants']: land.setdefault(q,d)
            if o['hour']==12 and d in (8,12,16,20,24): tiles[d]=tilecount(f['tiles'])
            if t+1<len(steps):
                for m in (steps[t+1][p]['action'] or {}).get('market',[]) or []:
                    if isinstance(m,list) and m and m[0]=='SELL': sold[m[1]]+= (m[2] if len(m)>2 else 1)
        out.append((names[p],g['rewards'][p],money,land,hires,tiles,sold))
    print('=== EP',eid,'shops',steps[-1][0]['observation']['town']['unlocked_shops'])
    for n,r,money,land,hires,tiles,sold in out:
        print(f'{n[:22]:22s} final={r:.0f} money d10={money.get(10)} d15={money.get(15)} d20={money.get(20)} d25={money.get(25)} d29={money.get(29)}')
        print('   land',{k:v for k,v in land.items() if k!='NW'},'hires/day',[hires[d] for d in range(0,30,3)])
        for d,tc in tiles.items(): print('   d',d,tc)
if __name__=='__main__':
    for e in sys.argv[1:]: fp(int(e))

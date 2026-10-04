import json,gzip,sys,collections
def load(eid): return json.loads(gzip.decompress(open(f'replays/{eid}.json.gz','rb').read()))
def tilecount(tiles):
    c=collections.Counter()
    for row in tiles:
        for t in row:
            if t is None: c['empty']+=1
            elif t=='LOCKED': pass
            elif t['kind']=='PLANT': c[t['crop'][:3]]+=1
            elif t['kind']=='WEED': c['weed']+=1
            else: c[(t.get('animal') or ('e'+t['kind']))[:5]]+=1
    return dict(c)
def summarize(eid,verbose=True):
    g=load(eid);names=g['info']['TeamNames'];steps=g['steps']
    print('EP',eid,names,'rewards',g['rewards'])
    for p in range(2):
        sold=collections.Counter();rev=collections.Counter();bought=collections.Counter();spent=collections.Counter()
        print(f'--- P{p} {names[p]}')
        for t in range(len(steps)-1):
            o=steps[t][p]['observation'];act=steps[t+1][p]['action'] or {}
            # action at steps[t+1] is taken given obs at steps[t]
            prices=o['market']['prices'] if 'market' in o and o['market'] else {}
            for m in act.get("market",[]) or []:
                if not isinstance(m,list) or not m: continue
                if m[0] in ("SELL","BUY_SEED","BUY_ANIMAL","BUY_PRODUCT") and len(m)<3: m=m+[1]
                if m[0]=='SELL': sold[m[1]]+=m[2]; rev[m[1]]+=m[2]*prices.get(m[1],0)
                elif m[0] in('BUY_SEED','BUY_ANIMAL','BUY_PRODUCT'): bought[m[0][4:8]+':'+m[1]]+=m[2]
                elif m[0] in ('HIRE','BUY_LAND'): bought[m[0]]+=1
            if verbose and o['hour']==0 and o['day']%2==0:
                f=o['farms'][p]
                print(f"d{o['day']:2d} ${f['money']:7.0f} hires={len(f['hands'])} q={''.join(q[0]+q[1] for q in f['unlocked_quadrants'])} {tilecount(f['tiles'])} shed={sum(o['private']['shed'].values()) if o.get('private') else '?'}")
        print(' SOLD',dict(sold));print(' approxREV',{k:int(v) for k,v in rev.items()},'sum',int(sum(rev.values())));print(' BOUGHT',dict(bought))
    o=steps[-1][0]['observation'];print('town',o['town'])
if __name__=='__main__':
    for e in sys.argv[1:]: summarize(int(e))

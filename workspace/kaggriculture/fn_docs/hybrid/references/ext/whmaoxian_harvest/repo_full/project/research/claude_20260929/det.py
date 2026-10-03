import json,gzip,glob,sys,itertools,collections
def load(sid):
    out=[]
    for p in glob.glob(f'tapes/*_{sid}.json.gz'):
        out.append(json.loads(gzip.decompress(open(p,'rb').read())))
    return out
def farm(a): return json.dumps([a.get('farmer'),a.get('hands')])
def mkt(a): return json.dumps(a.get('market'))
def prefix(a,b,f):
    for t in range(min(len(a),len(b))):
        if f(a[t])!=f(b[t]): return t
    return min(len(a),len(b))
def shopseq(c): return [s for t,s in c['shops']][-1]
if __name__=='__main__':
    sid=int(sys.argv[1]);cs=load(sid)
    print('n',len(cs))
    # opening agreement
    pf=[prefix(a['tape'],b['tape'],farm) for a,b in itertools.combinations(cs,2)]
    pm=[prefix(a['tape'],b['tape'],mkt) for a,b in itertools.combinations(cs,2)]
    print('farm prefix: min',min(pf),'median',sorted(pf)[len(pf)//2],'max',max(pf))
    print('market prefix: min',min(pm),'median',sorted(pm)[len(pm)//2],'max',max(pm))
    # same first shop pairs
    for a,b in itertools.combinations(cs,2):
        sa,sb=shopseq(a),shopseq(b)
        k=0
        while k<min(len(sa),len(sb)) and sa[k]==sb[k]: k+=1
        if k>=2: print('shared shops',k,sa[:k],'farm prefix',prefix(a['tape'],b['tape'],farm),'mkt',prefix(a['tape'],b['tape'],mkt), 'seats',a['seat'],b['seat'])

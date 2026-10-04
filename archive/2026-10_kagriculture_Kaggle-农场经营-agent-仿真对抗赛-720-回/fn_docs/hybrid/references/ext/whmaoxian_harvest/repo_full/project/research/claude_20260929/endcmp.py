import sys
from dbg import run
a=sys.argv[1];seed=int(sys.argv[2]);t0=int(sys.argv[3]) if len(sys.argv)>3 else 672
ea=run(a,'cand/r2.py',seed); eb=run('cand/r2.py','cand/r2.py',seed)
def fy(f): return sum(tl.get('yield_units',0) for row in f['tiles'] for tl in row if isinstance(tl,dict))
for t in range(t0,720,2):
    oa=ea.steps[t][0].observation; ob=eb.steps[t][0].observation
    fa,fb=oa.farms[0],ob.farms[0]
    print(f"d{oa.day}h{oa.hour:2d} A ${fa['money']:7.0f} h{len(fa['hands']):2d} fld{fy(fa):4d} car{sum(sum(i.values()) for i in oa.private['inventories']):4d} shd{sum(oa.private['shed'].values()):4d} | B ${fb['money']:7.0f} h{len(fb['hands']):2d} fld{fy(fb):4d} car{sum(sum(i.values()) for i in ob.private['inventories']):4d} shd{sum(ob.private['shed'].values()):4d}")
print('final A',ea.steps[-1][0].observation.farms[0]['money'],'B',eb.steps[-1][0].observation.farms[0]['money'])

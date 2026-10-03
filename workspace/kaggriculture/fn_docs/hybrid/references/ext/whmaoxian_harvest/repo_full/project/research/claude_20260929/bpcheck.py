import sys,io,contextlib,os,collections
from dbg import run
seed=int(sys.argv[1])
g={}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(open('cand/hyBP1.py',encoding='utf-8').read(),os.path.abspath('cand/hyBP1.py'),'exec'),g)
env=run('cand/r2.py','cand/r2.py',seed)
# actual R2 plantings
actual=collections.Counter();byday=collections.Counter()
for t in range(len(env.steps)-1):
    o=env.steps[t][0].observation;f=o.farms[0];n=env.steps[t+1][0].observation.farms[0]
    for y in range(10):
        for x in range(10):
            a,b=f['tiles'][y][x],n['tiles'][y][x]
            if (a is None or (isinstance(a,dict) and a.get('kind')=='WEED')) and isinstance(b,dict) and b.get('kind')=='PLANT':
                actual[((x,y),t//24,b['crop'])]+=1
# replay R2 in-process to get route: run its agent on the recorded observations
R2=g['_HY_R2']
for t in range(len(env.steps)-1):
    R2(env.steps[t][0].observation,env.configuration)
ch=g['_IMPL'].chassis
route=ch.players.get(0,{}).get('route')
print('route',route,'routes',len(ch.routes))
bp=g['_HY_ENG']['tape_plantings'](ch.routes[route],(648,ch.routes.get(2)))
pred=collections.Counter()
for p,ev in bp.items():
    for t,c in ev:
        if c in g['_HY_ENG']['CROPS']: pred[(p,t//24,c)]+=1
post=lambda C:{k:v for k,v in C.items() if k[1]>=12}
A,P=post(actual),post(pred)
match=sum(min(A[k],P.get(k,0)) for k in A)
print('actual post-d12 plantings',sum(A.values()),'blueprint',sum(P.values()),'exact tile/day/crop matches',match)
print('actual crops',collections.Counter(k[2] for k in A.elements()) if False else collections.Counter(k[2] for k in A),'bp crops',collections.Counter(k[2] for k in P))

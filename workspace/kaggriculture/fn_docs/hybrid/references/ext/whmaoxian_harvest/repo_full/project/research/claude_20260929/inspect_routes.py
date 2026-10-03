import sys,io,contextlib,collections,os
sys.argv=['x']
with contextlib.redirect_stdout(io.StringIO()):
    g={}
    exec(compile(open('cand/r2.py',encoding='utf-8').read(),'r2','exec'),g)
ch=g['_IMPL'].chassis
print('routes',len(ch.routes))
for rid,tape in sorted(ch.routes.items()):
    land=[t for t,a in enumerate(tape) if any(o and o[0]=='BUY_LAND' for o in (a.get('market') or []))]
    hires=collections.Counter()
    last_hire_hour=0
    for t,a in enumerate(tape):
        n=sum(1 for o in (a.get('market') or []) if o and o[0]=='HIRE')
        if n: hires[t//24]+=n; last_hire_hour=max(last_hire_hour,t%24)
    print(rid,'land',land,'maxhires',max(hires.values()) if hires else 0,'lasthirehour',last_hire_hour)

import sys,io,contextlib,os
from dbg import run
cand=sys.argv[1];seed=int(sys.argv[2]);T=int(sys.argv[3])
env=run(cand,'cand/r2.py',seed)
import collections
g={}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(open(cand,encoding='utf-8').read(),cand,'exec'),g)
E=g['_HY_ENG']
obs=env.steps[T][0].observation
st=E['new_state'](); st['cfg'].update(E['OVERRIDES'])
w=E['World'](obs)
E['assign_animal_roles'](w,st)
tasks=E['gen_tasks'](w,st)
f=obs.farms[0]
for y in range(10):
    for x in range(10):
        t=f['tiles'][y][x]
        if isinstance(t,dict) and t.get('kind')=='WEED': print('weed',(x,y),'tasks',tasks.get((x,y)),'role',st['roles'].get((x,y)))
print('n tasks',len(tasks),'crop choice',E['crop_choice'](w,st),'spendable',E['spendable'](w,st))

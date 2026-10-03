import sys,collections
from dbg import run
env=run(sys.argv[1],sys.argv[2],int(sys.argv[3]))
c=collections.Counter()
for t in range(len(env.steps)-1):
    o=env.steps[t][0].observation;f=o.farms[0]
    act=env.steps[t+1][0].action or {}
    units=[tuple(f['farmer'])]+[tuple(h) for h in f['hands']]
    cmds=[act.get('farmer')]+list(act.get('hands') or [])
    for pos,cmd in zip(units,cmds):
        if not cmd or cmd[0]!='PASS': continue
        c['PASS']+=1
        tl=f['tiles'][pos[1]][pos[0]]
        if isinstance(tl,dict) and tl.get('animal'):
            if not tl['cared_today']: c['on_animal_uncared']+=1
            if tl['fertilizer_available']: c['on_animal_fert']+=1
            if not tl['fed_today']: c['on_animal_unfed']+=1
        elif isinstance(tl,dict) and tl.get('kind')=='PLANT':
            if not tl['watered_today']: c['on_plant_unwatered']+=1
        elif isinstance(tl,dict) and tl.get('kind')=='WEED': c['on_weed']+=1
print(dict(c))

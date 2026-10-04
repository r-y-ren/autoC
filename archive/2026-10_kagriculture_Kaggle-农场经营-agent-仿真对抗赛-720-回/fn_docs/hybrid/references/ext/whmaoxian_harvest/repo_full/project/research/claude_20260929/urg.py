import sys
from dbg import run
env=run(sys.argv[1],sys.argv[2],int(sys.argv[3]))
for t in range(len(env.steps)-1):
    o=env.steps[t][0].observation
    if o.day<12 or o.hour not in (16,20,23): continue
    f=o.farms[0]
    urg=[(x,y) for y in range(10) for x in range(10) if isinstance(f['tiles'][y][x],dict) and f['tiles'][y][x].get('kind')=='PLANT' and f['tiles'][y][x]['consecutive_unwatered']>=1 and not f['tiles'][y][x]['watered_today']]
    fed=[(x,y) for y in range(10) for x in range(10) if isinstance(f['tiles'][y][x],dict) and f['tiles'][y][x].get('animal') and not f['tiles'][y][x]['fed_today']]
    act=env.steps[t+1][0].action
    cmds=[act.get('farmer')]+list(act.get('hands') or [])
    print(f"d{o.day}h{o.hour} urgent={len(urg)} unfed={len(fed)} units={len(cmds)} cmds={[c[0] for c in cmds]}")
    if o.day>15: break

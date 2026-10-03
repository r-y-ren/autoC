import sys
from dbg import run
env=run(sys.argv[1],sys.argv[2],int(sys.argv[3]));day=int(sys.argv[4])
for t in range(day*24+14,day*24+24):
    o=env.steps[t][0].observation;act=env.steps[t+1][0].action
    inv=o.private['inventories']
    print(f"h{o.hour} shed={ {k:v for k,v in o.private['shed'].items() if v} } carried={[sum(i.values()) for i in inv]} mkt={act.get('market')}")

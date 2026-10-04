import sys
from dbg import run
env=run(sys.argv[1],'cand/r2.py',int(sys.argv[2]));day=int(sys.argv[3])
rows={}
for t in range(day*24,day*24+24):
    o=env.steps[t][0].observation;f=o.farms[0];act=env.steps[t+1][0].action or {}
    units=[tuple(f['farmer'])]+[tuple(h) for h in f['hands']]
    cmds=[act.get('farmer')]+list(act.get('hands') or [])
    for i,(p,c) in enumerate(zip(units,cmds)):
        ab={'NORTH':'^','SOUTH':'v','EAST':'>','WEST':'<','PASS':'.','WATER':'W','HARVEST':'H','PICKUP':'P','PLACE':'L','DROP':'D','FEED':'F','CARE':'C','COLLECT_FERTILIZER':'c','FERTILIZE':'Z','PLANT':'T','DIG':'G'}.get(c[0] if c else '?','?')
        rows.setdefault(i,[]).append(ab)
for i,r in rows.items(): print(f'u{i:2d}',''.join(r))

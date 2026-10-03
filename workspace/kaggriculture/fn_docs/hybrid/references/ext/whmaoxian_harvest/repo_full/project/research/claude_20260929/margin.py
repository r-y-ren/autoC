import json,sys
from episodes import rows
for sid in map(int,sys.argv[1:]):
    rs=rows(sid,json.load(open(f'eplists/{sid}.json')))
    for lo,hi in [(0,2200),(2200,2500),(2500,2800),(2800,4000)]:
        g=[r for r in rs if r['oppr'] and lo<=r['oppr']<hi]
        if g: print(sid,f'{lo}-{hi} n={len(g)} W={sum(r["my"]>r["opp"] for r in g)} ratio={sum(r["my"] for r in g)/sum(r["opp"] for r in g):.3f}')

import json
from episodes import rows
sid=56581759
rs=rows(sid,json.load(open(f'eplists/{sid}.json')))
bins=[(0,2000),(2000,2200),(2200,2400),(2400,2600),(2600,2800),(2800,4000)]
for lo,hi in bins:
    g=[r for r in rs if r['oppr'] and lo<=r['oppr']<hi]
    if not g: continue
    w=sum(r['my']>r['opp'] for r in g)
    print(f'{lo}-{hi}: n={len(g)} W={w} meanmy={sum(r["my"] for r in g)/len(g):.0f} meanopp={sum(r["opp"] for r in g)/len(g):.0f}')
print('last 30:')
for r in rs[-30:]: print(r['ep'],r['end'][:16],r['seat'],r['my'],r['opp'],round(r['oppr'] or 0),round(r['myr'] or 0))

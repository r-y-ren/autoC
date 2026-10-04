import json,sys
from episodes import rows
sid=int(sys.argv[1]);n=int(sys.argv[2]); minr=float(sys.argv[3]) if len(sys.argv)>3 else 0
rs=[r for r in rows(sid,json.load(open(f'eplists/{sid}.json'))) if (r['oppr'] or 0)>=minr]
for r in rs[-n:]: print(r['ep'],r['seat'],r['my'],r['opp'],round(r['oppr'] or 0))

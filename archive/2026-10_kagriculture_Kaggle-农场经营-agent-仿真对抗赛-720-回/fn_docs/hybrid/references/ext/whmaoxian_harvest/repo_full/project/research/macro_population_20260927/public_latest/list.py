"""Snapshot public notebook metadata without authentication or execution."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
from datetime import datetime,timezone
import hashlib,json,requests
D=Path(__file__).resolve().parent
USERS=('yhay81','ahmedberatozer','hakdevelopment','aurax7','boatlee','salemali7')
def fetch(user):
    response=requests.get('https://www.kaggle.com/api/v1/kernels/list',params={'user':user,'page':1,'pageSize':100,'sortBy':'dateRun'},timeout=45)
    response.raise_for_status();data=response.json()
    path=D/(user+'_listing.json');raw=response.content
    path.write_bytes(raw)
    rows=[r for r in data if 'kaggricultur' in (r.get('title','')+' '+r.get('ref','')).lower()]
    return dict(user=user,captured_utc=datetime.now(timezone.utc).isoformat(),source=response.url,sha256=hashlib.sha256(raw).hexdigest(),notebooks=rows)
if __name__=='__main__':
    results=[]
    with ThreadPoolExecutor(max_workers=3) as pool:
        futures={pool.submit(fetch,u):u for u in USERS}
        for future in as_completed(futures):
            try:row=future.result()
            except Exception as exc:row=dict(user=futures[future],error=str(exc))
            results.append(row)
            print(json.dumps(dict(user=row['user'],error=row.get('error'),notebooks=[{k:v.get(k) for k in ('ref','title','lastRunTime','totalVotes')} for v in row.get('notebooks',[])])),flush=True)
    (D/'manifest.json').write_text(json.dumps(results,indent=2),encoding='utf-8')

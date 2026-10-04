"""Download named public notebook sources for review only; no notebook execution."""
from pathlib import Path
from datetime import datetime,timezone
from concurrent.futures import ThreadPoolExecutor
import hashlib,json,requests
D=Path(__file__).resolve().parent;O=D/'sources';O.mkdir(exist_ok=True)
SLUGS=('nathanjacob/kaggriculture-pipe16-idle-workers',
 'dmitriigluzdov/kaggriculture-more-wheat-smarter-sales',
 'thomastschinkel/the-metav4-farm-submission-v13')
def fetch(slug):
    url='https://www.kaggle.com/api/v1/kernels/pull/'+slug
    try:
        response=requests.get(url,timeout=(10,35));response.raise_for_status()
        raw=response.content;assert len(raw)<20000000
        data=json.loads(raw);meta=data.get('metadata',{})
        assert meta.get('isPrivate') is False,'Not a confirmed public notebook'
        p=O/(slug.replace('/','__')+'.json');p.write_bytes(raw)
        nb=json.loads(data['blob'].get('source') or data['blob']['sourceNullable'])
        cells=[]
        for i,c in enumerate(nb['cells']):
            s=''.join(c.get('source',[]));cells.append((i,c['cell_type'],len(s),s[:180]))
        return dict(slug=slug,url=url,path=p.name,sha256=hashlib.sha256(raw).hexdigest(),
                    metadata=meta,cells=cells,captured_utc=datetime.now(timezone.utc).isoformat())
    except Exception as e:return dict(slug=slug,url=url,error=str(e))
if __name__=='__main__':
    with ThreadPoolExecutor(max_workers=3) as pool:results=list(pool.map(fetch,SLUGS))
    (D/'public_receipts.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
    print(json.dumps(results),flush=True)

"""Fetch public notebook text for static review, never execute notebook cells."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,requests
D=Path(__file__).resolve().parent;O=D/'public_review_20260929';O.mkdir(exist_ok=True)
slugs=['ahmedberatozer/more-yield-smarter-labor','salemali7/kaggriculture-2900','jaxa623/2780-beyond-48-0-128-128-worlds-with-95-cis','georgymamarin/kaggriculture-daily-replays-the-live-meta-report']
receipts=[]
for slug in slugs:
    url='https://www.kaggle.com/api/v1/kernels/pull/'+slug
    try:
        response=requests.get(url,timeout=(10,30));response.raise_for_status();raw=response.content
        assert len(raw)<20000000
        obj=json.loads(raw);meta=obj['metadata'];assert meta.get('isPrivate') is False
        target=O/(slug.replace('/','__')+'.json')
        if target.exists():assert target.read_bytes()==raw
        else:target.write_bytes(raw)
        blob=obj['blob'];source=blob.get('source') or blob.get('sourceNullable');notebook=json.loads(source)
        overview=[dict(index=i,kind=c['cell_type'],characters=len(''.join(c.get('source',[]))),head=''.join(c.get('source',[]))[:400]) for i,c in enumerate(notebook['cells'])]
        receipt=dict(slug=slug,url=url,path=target.name,sha256=hashlib.sha256(raw).hexdigest(),metadata=meta,cells=overview,captured_utc=datetime.now(timezone.utc).isoformat())
    except Exception as error:receipt=dict(slug=slug,error=str(error))
    receipts.append(receipt);print(json.dumps(receipt),flush=True)
(O/'receipts.json').write_text(json.dumps(receipts,indent=2),encoding='utf-8')

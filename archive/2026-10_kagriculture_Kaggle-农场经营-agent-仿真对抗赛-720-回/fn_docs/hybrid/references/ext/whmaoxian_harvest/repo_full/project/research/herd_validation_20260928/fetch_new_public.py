"""Read newly located public notebook sources for inspection; do not execute them."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,requests
D=Path(__file__).resolve().parent;O=D/'new_public_sources';O.mkdir(exist_ok=True)
slugs=('salemali7/harvest-kaggriculture','prvsiyan/where-the-wheat-remembers-tomorrow-kaggriculture','georgymamarin/kaggriculture-what-2600-farms-do-differently')
receipts=[]
for slug in slugs:
    url='https://www.kaggle.com/api/v1/kernels/pull/'+slug
    try:
        r=requests.get(url,timeout=(10,40));r.raise_for_status();raw=r.content
        assert len(raw)<20000000
        obj=json.loads(raw);meta=obj.get('metadata',{})
        assert meta.get('isPrivate') is False
        p=O/(slug.replace('/','__')+'.json');p.write_bytes(raw)
        source=obj['blob'].get('source') or obj['blob']['sourceNullable']
        notebook=json.loads(source)
        cells=[dict(index=i,type=c['cell_type'],characters=len(''.join(c.get('source',[]))),preview=''.join(c.get('source',[]))[:450]) for i,c in enumerate(notebook['cells'])]
        record=dict(slug=slug,url=url,path=str(p),sha256=hashlib.sha256(raw).hexdigest(),metadata=meta,cells=cells,captured_utc=datetime.now(timezone.utc).isoformat())
        print(json.dumps(dict(slug=slug,metadata=meta,cells=cells)),flush=True)
    except Exception as exc:
        record=dict(slug=slug,error=str(exc));print(json.dumps(record),flush=True)
    receipts.append(record)
(O/'receipts.json').write_text(json.dumps(receipts,indent=2),encoding='utf-8')

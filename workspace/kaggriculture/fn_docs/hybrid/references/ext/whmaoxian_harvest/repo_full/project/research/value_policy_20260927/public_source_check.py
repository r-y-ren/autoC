"""Download only public Kaggle notebook sources for inspection; do not execute them."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,requests
D=Path(__file__).resolve().parent;out=D/'public_sources';out.mkdir(exist_ok=True)
slugs=('ahmedberatozer/kaggriculture-v35-reactive-sales-sheep-expansi','aurax7/kaggriculture-shop-router-reactive-v7','salemali7/kaggriculture-2900')
receipts=[]
for slug in slugs:
    url='https://www.kaggle.com/api/v1/kernels/pull/'+slug
    try:
        response=requests.get(url,timeout=40);response.raise_for_status();data=response.json()
        path=out/(slug.replace('/','__')+'.json')
        path.write_text(json.dumps(data),encoding='utf-8')
        meta=data.get('metadata',{})
        record=dict(slug=slug,path=path.name,sha256=hashlib.sha256(path.read_bytes()).hexdigest(),version=meta.get('currentVersionNumber'),last_run=meta.get('lastRunTime'),public=not meta.get('isPrivate',True),captured_utc=datetime.now(timezone.utc).isoformat(),source=url)
    except Exception as exc:record=dict(slug=slug,error=str(exc),source=url)
    receipts.append(record);print(json.dumps(record),flush=True)
(out/'receipts.json').write_text(json.dumps(receipts,indent=2))

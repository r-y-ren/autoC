"""Download public Kaggle notebook JSON for review; do not execute downloaded code."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,requests
P=Path(__file__).resolve().parent;out=P/'public_notebooks';out.mkdir(exist_ok=True)
slugs=['thomastschinkel/the-2945-farm-96-vs-the-top-10-public-bots','ahmedberatozer/more-yield-smarter-labor']
records=[]
for slug in slugs:
    url='https://www.kaggle.com/api/v1/kernels/pull/'+slug
    record={'slug':slug,'url':url,'captured_utc':datetime.now(timezone.utc).isoformat()}
    try:
        response=requests.get(url,timeout=45);response.raise_for_status()
        raw=response.content;assert len(raw)<30000000
        obj=json.loads(raw);path=out/(slug.replace('/','__')+'.json')
        if not path.exists():path.write_bytes(raw)
        else:assert path.read_bytes()==raw,'Preserve original download; use a new timestamp for updates.'
        record.update(path=str(path),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),keys=list(obj)[:20])
    except Exception as exc:record['error']=str(exc)
    records.append(record);print(json.dumps(record),flush=True)
(out/'download_receipts.json').write_text(json.dumps(records,indent=2))

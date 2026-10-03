"""Read public Kaggle notebook listings. No login, upload or account changes."""
from pathlib import Path
import json,requests
OUT=Path(__file__).resolve().parent
results={}
for user in ('boatlee','ahmedberatozer','hakdevelopment','raykkretzschmar'):
    response=requests.get('https://www.kaggle.com/api/v1/kernels/list',
        params={'user':user,'page':1,'pageSize':100,'sortBy':'dateRun'},timeout=45)
    print(user,response.status_code,response.headers.get('Content-Type'),flush=True)
    if response.status_code!=200:continue
    try:data=response.json()
    except ValueError:continue
    results[user]=data
    (OUT/('public_notebooks_'+user+'.json')).write_text(json.dumps(data),encoding='utf-8')
    if isinstance(data,list):
        print(json.dumps([{k:r.get(k) for k in ('ref','title','lastRunTime','totalVotes')} for r in data[:20]]),flush=True)
(OUT/'public_notebook_listing_manifest.json').write_text(json.dumps(list(results)),encoding='utf-8')

"""Collect additional public, non-uploading comparison sources."""
from pathlib import Path
import concurrent.futures,json
import fetch_notebooks as loader
OUT=Path(__file__).resolve().parent
SLUGS=['salemali7/kaggriculture-3000-socre','aurax7/kaggriculture-shop-router-reactive-v7',
       'yhay81/shop-router-0909','leoprovorov/a-song-of-ice-and-fire-fixed-flexible',
       'alperen5252525/turn-one-market-advantage',
       'ahmedberatozer/kaggriculture-v35-reactive-sales-sheep-expansi']
if __name__=='__main__':
    results=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        futures={pool.submit(loader.fetch,slug):slug for slug in SLUGS}
        for future in concurrent.futures.as_completed(futures):
            try: row=future.result()
            except Exception as exc: row=dict(slug=futures[future],error=str(exc))
            results.append(row);print(json.dumps(row),flush=True)
    (OUT/'additional_source_index.json').write_text(json.dumps(results,indent=2),encoding='utf-8')

"""Read public notebook sources without executing notebook cells."""
from pathlib import Path
import concurrent.futures, hashlib, json, requests
OUT = Path(__file__).resolve().parent/'notebooks'
OUT.mkdir(exist_ok=True)
SLUGS = [
 'raykkretzschmar/kaggriculture-rank-your-agent',
 'georgymamarin/kaggriculture-what-2600-farms-do-differently',
 'nathanjacob/kaggriculture-pipe-5-terminal-boost',
 'salemali7/kaggriculture-2900',
 'pilkwang/kaggriculture-structured-economic-policy',
 'leoprovorov/kaggricult-man-reverse-engineering',
 'tetsutani/market-smart-farming-kaggriculture',
 'hakdevelopment/kaggriculture-2887-score-fieldcraft-agent']
def fetch(slug):
    name = slug.replace('/','__')
    response = requests.get('https://www.kaggle.com/api/v1/kernels/pull/'+slug,timeout=60)
    response.raise_for_status()
    data = response.json()
    (OUT/(name+'.json')).write_text(json.dumps(data),encoding='utf-8')
    source = data['blob'].get('sourceNullable',data['blob'].get('source'))
    notebook = json.loads(source)
    cells = notebook.get('cells',[])
    notes = '\n\n'.join(''.join(c['source']) for c in cells if c['cell_type']=='markdown')
    (OUT/(name+'.md')).write_text(notes,encoding='utf-8')
    for index,cell in enumerate(cells):
        if cell['cell_type']=='code':
            (OUT/(name+f'_{index}.py.txt')).write_text(''.join(cell['source']),encoding='utf-8')
    return dict(slug=slug,cells=[(i,c['cell_type'],len(''.join(c['source']))) for i,c in enumerate(cells)])
if __name__ == '__main__':
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        futures = {pool.submit(fetch,slug):slug for slug in SLUGS}
        for future in concurrent.futures.as_completed(futures):
            try: row = future.result()
            except Exception as exc: row = dict(slug=futures[future],error=str(exc))
            results.append(row)
            print(json.dumps(row),flush=True)
    (OUT/'index.json').write_text(json.dumps(results,indent=2),encoding='utf-8')

"""Download public notebook data; do not execute any notebook cells."""
import json
from pathlib import Path
import requests

root=Path(__file__).parent
for name, slug in [('ahmed_v56','ahmedberatozer/kaggriculture-v56-smarter-seeds-and-fertilizer'),
                   ('orderbook','shiiin9/your-market-list-is-an-order-book')]:
    response=requests.get('https://www.kaggle.com/api/v1/kernels/pull/'+slug,timeout=40)
    response.raise_for_status()
    data=response.json()
    (root/f'external/{name}_response.json').write_text(json.dumps(data),encoding='utf-8')
    cells=json.loads(data['blob']['sourceNullable'])['cells']
    print(name,[(i,c['cell_type'],len(''.join(c.get('source',[])))) for i,c in enumerate(cells)])
    (root/f'research/round7/{name}_notes.md').write_text('\n\n'.join(''.join(c['source']) for c in cells if c['cell_type']=='markdown'),encoding='utf-8')

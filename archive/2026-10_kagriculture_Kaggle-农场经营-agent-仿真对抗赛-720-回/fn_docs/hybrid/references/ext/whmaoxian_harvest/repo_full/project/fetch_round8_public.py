"""Fetch public notebook source data without running notebook cells."""
import json
from pathlib import Path
import requests

r=Path(__file__).parent
out=r/'external/round8'
out.mkdir(exist_ok=True)
for name,slug in [('fieldcraft','hakdevelopment/kaggriculture-2887-score-fieldcraft-agent'),
                  ('master2965','haideptry/the-2965-master-hybrid-engine'),
                  ('icefire','leoprovorov/a-song-of-ice-and-fire-fixed-flexible')]:
    response=requests.get('https://www.kaggle.com/api/v1/kernels/pull/'+slug,timeout=45)
    response.raise_for_status()
    data=response.json()
    (out/f'{name}_response.json').write_text(json.dumps(data),encoding='utf-8')
    cells=json.loads(data['blob']['sourceNullable'])['cells']
    (out/f'{name}_notes.md').write_text('\n\n'.join(''.join(c['source']) for c in cells if c['cell_type']=='markdown'),encoding='utf-8')
    print(name, [(i,c['cell_type'],len(''.join(c['source']))) for i,c in enumerate(cells)],flush=True)
    for i,c in enumerate(cells):
        if c['cell_type']=='code':
            (out/f'{name}_cell{i}.txt').write_text(''.join(c['source']),encoding='utf-8')
    (out/f'{name}_origin.json').write_text(json.dumps({'url':'https://www.kaggle.com/code/'+slug,'version':data['metadata'].get('currentVersionNumber')}),encoding='utf-8')

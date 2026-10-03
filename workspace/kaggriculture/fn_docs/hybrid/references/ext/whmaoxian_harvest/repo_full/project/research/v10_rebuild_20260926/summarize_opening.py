from pathlib import Path
import json
OUT=Path(__file__).resolve().parent
rows=[json.loads(line) for line in (OUT/'opening_results.jsonl').read_text(encoding='utf-8').splitlines()]
for source in ('release_v9','release_v10','open_5','open_10','open_30'):
    subset=[r for r in rows if source in r['candidate'] and r['panel']=='online_loss_probe']
    print(source,[(Path(r['opponent']).stem,r['margin']) for r in subset],flush=True)
control=[r for r in rows if 'open_20.py' in r['candidate']]
reference=[r for r in rows if 'release_v10/' in r['candidate']]
key=lambda r:(r['opponent'],r['seed'],r['seat'])
reference={key(r):r for r in reference}
print('sham-control coin parity',sum(r['money']==reference[key(r)]['money'] for r in control),'/',len(control),flush=True)

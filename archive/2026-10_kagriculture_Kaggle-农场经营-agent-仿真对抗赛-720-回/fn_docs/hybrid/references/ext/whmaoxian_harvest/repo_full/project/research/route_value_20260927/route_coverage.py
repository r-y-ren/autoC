"""Summarize candidate-menu coverage before deciding further simulation budgets."""
from pathlib import Path
import json,statistics
D=Path(__file__).resolve().parent
rows=[json.loads(s) for s in (D/'prefixes.jsonl').read_text().splitlines()]
routes=json.loads((D/'model.json').read_text())['routes']
point=lambda v:1 if v>0 else .5 if v==0 else 0
report=[]
for index,route in enumerate(routes):
    families={}
    for family in sorted({r['family'] for r in rows}):
        cases=[r for r in rows if r['family']==family]
        families[family]=dict(games=len(cases),points=sum(point(r['outcomes'][index]['margin']) for r in cases),
            mean_margin_gain=statistics.mean(r['outcomes'][index]['margin']-r['outcomes'][0]['margin'] for r in cases),
            flipped=sum(r['outcomes'][0]['margin']<=0<r['outcomes'][index]['margin'] for r in cases),
            lost=sum(r['outcomes'][index]['margin']<=0<r['outcomes'][0]['margin'] for r in cases))
    report.append(dict(route=route,families=families))
(D/'route_coverage.json').write_text(json.dumps(report,indent=2))
for r in report:print(json.dumps(r),flush=True)

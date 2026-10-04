"""Show complete candidate panels only; never mix references into public strength."""
from pathlib import Path
import collections,json,statistics
OUT=Path(__file__).resolve().parent
rows=[json.loads(line) for line in (OUT/'combination_results.jsonl').read_text(encoding='utf-8').splitlines()]
groups=collections.defaultdict(list)
for row in rows:groups[row['candidate']].append(row)
summary={}
for candidate,group in groups.items():
    if len(group)!=123:continue
    panels={}
    for panel in sorted({r['panel'] for r in group}):
        sub=[r for r in group if r['panel']==panel];good=[r for r in sub if r.get('valid')]
        panels[panel]=dict(games=len(sub),wins=sum(r['margin']>0 for r in good),
            ties=sum(r['margin']==0 for r in good),invalid=len(sub)-len(good),
            mean_margin=round(statistics.mean(r['margin'] for r in good),2))
    summary[candidate]=panels
    print(Path(candidate).name,panels,flush=True)
(OUT/'combination_complete_panels.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
print('Raw records',len(rows),'complete candidates',len(summary),flush=True)

"""Describe all finite Phase-C results, including losses and incomplete panels."""
from pathlib import Path
from statistics import mean
import json
C=Path(__file__).resolve().parent
raw=(C/'risk_results.jsonl').read_text(encoding='utf-8')
lines=raw.splitlines()
if raw and not raw.endswith('\n'):lines=lines[:-1]
rows=[json.loads(line) for line in lines]
jobs=json.loads((C/'risk_jobs.json').read_text())
assert len({r['id'] for r in rows})==len(rows)
def describe(group):
    return dict(games=len(group),invalid=sum(not r.get('valid') for r in group),
      wins=sum(r.get('margin',0)>0 for r in group),ties=sum(r.get('margin',1)==0 for r in group),
      losses=sum(r.get('margin',0)<0 for r in group),
      points=mean(1 if r['margin']>0 else .5 if r['margin']==0 else 0 for r in group),
      mean_margin=mean(r['margin'] for r in group),worst=min(r['margin'] for r in group))
summary={}
for candidate in sorted({j['candidate'] for j in jobs}):
    group=[r for r in rows if r['candidate']==candidate]
    item=dict(recorded=len(group),expected=sum(j['candidate']==candidate for j in jobs))
    item['complete']=item['recorded']==item['expected']
    item['panels']={p:describe([r for r in group if r['panel']==p]) for p in sorted({r['panel'] for r in group})}
    item['families']={p:describe([r for r in group if r['family']==p and r['panel'] in ('public_program','counter_population','direct_reference')]) for p in sorted({r['family'] for r in group if r['panel'] in ('public_program','counter_population','direct_reference')})}
    summary[candidate]=item
    print(Path(candidate).stem,item['recorded'],{p:(d['wins'],d['ties'],d['losses'],round(d['mean_margin'])) for p,d in item['panels'].items()},flush=True)
(C/'risk_summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')

"""Aggregate completed development ledgers without counting cached controls anew."""
from pathlib import Path
import json,runpy
D=Path(__file__).resolve().parent;R=D.parents[1]
lib=runpy.run_path(str(D/'summarize_herd.py'));load=lib['load'];key=lib['key'];summarize=lib['summarize'];BASE=lib['BASE']
controls=load(R/'research/meta_rebuild_20260927/midgame_herd_results.jsonl')+load(D/'herd_extended_results.jsonl')
base={key(r):r for r in controls if r['candidate']==BASE}
repeated=load(D/'repeated_results.jsonl')+load(D/'repeated_extended_results.jsonl')
archived=load(D/'archived_panel_results.jsonl');expected=load(D/'expected_repeated_results.jsonl')
archive_base={key(r):r for r in archived if r['candidate']==BASE}
reports={'repeated':summarize(repeated,base),'archived':summarize(archived,archive_base),'expected':summarize(expected,base)}
counts={name:dict(completed=len(rows),invalid=sum(not r.get('valid') for r in rows)) for name,rows in [('repeated',repeated),('archived',archived),('expected',expected)]}
(D/'expanded_development_summary.json').write_text(json.dumps(dict(counts=counts,results=reports),indent=2))
print('COUNTS',json.dumps(counts),flush=True)
for batch,report in reports.items():
    for path,row in report.items():
        print(batch,Path(path).name,'N',row['cases'],'PANELS',json.dumps(row['panels']),'DECISIONS',json.dumps(row['decisions']),flush=True)

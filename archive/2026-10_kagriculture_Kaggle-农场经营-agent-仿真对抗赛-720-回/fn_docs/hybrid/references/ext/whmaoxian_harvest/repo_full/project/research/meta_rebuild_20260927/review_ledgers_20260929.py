"""Read-only experiment review with paired outcomes and duplicate-result checks."""
from pathlib import Path
from collections import defaultdict
import json,statistics,hashlib
D=Path(__file__).resolve().parent;R=D.parents[1]
BASE='b35b5b09fbec059ab7cbd2ba67a9fbb6d3e467ef5262f3e2ddba592b3e50c1c4'
folders=[D,R/'research/production_upgrade_20260928',R/'research/herd_search_20260929',R/'research/herd_validation_20260928']
ledgers={};references={};conflicts=[]
def key(row):
    return (row.get('seed'),row.get('seat'),row.get('opponent'),row.get('opponent_sha256'))
def points(row):
    m=row['margin'];return 1.0 if m>0 else 0.0 if m<0 else 0.5
for folder in folders:
    for path in sorted(folder.glob('*results*.jsonl')):
        rows=[]
        for text in path.read_text(encoding='utf-8').splitlines():
            try:row=json.loads(text)
            except json.JSONDecodeError:continue
            rows.append(row)
            if row.get('valid') and row.get('candidate_sha256')==BASE:
                k=key(row)
                if k in references and references[k]['money']!=row['money']:
                    conflicts.append(dict(context=k,first=references[k]['money'],second=row['money']))
                references[k]=row
        ledgers[path.relative_to(R).as_posix()]=rows
summary={'baseline_conflicts':conflicts,'baseline_contexts':len(references),'ledgers':{}}
for path,rows in ledgers.items():
    groups=defaultdict(list)
    for row in rows:groups[row.get('candidate','unknown')].append(row)
    result={}
    for candidate,group in groups.items():
        valid=[r for r in group if r.get('valid') and 'margin' in r]
        panels={}
        for panel in sorted({r.get('panel','unknown') for r in valid}):
            rr=[r for r in valid if r.get('panel','unknown')==panel]
            paired=[(r,references[key(r)]) for r in rr if key(r) in references]
            panels[panel]=dict(cases=len(rr),wins=sum(r['margin']>0 for r in rr),losses=sum(r['margin']<0 for r in rr),ties=sum(r['margin']==0 for r in rr),paired=len(paired),outcome_delta=sum(points(r)-points(b) for r,b in paired),mean_margin_delta=round(statistics.mean([r['margin']-b['margin'] for r,b in paired]),2) if paired else None)
        result[candidate]=dict(cases=len(group),invalid=len(group)-len(valid),panels=panels)
    summary['ledgers'][path]=dict(cases=len(rows),variants=result)
output=D/'ledger_review_20260929.json'
output.write_text(json.dumps(summary,indent=2),encoding='utf-8')
print('BASELINE_CONTEXTS',len(references),'CONFLICTS',len(conflicts),flush=True)
for path,section in summary['ledgers'].items():
    if any(t in path for t in ('herd_extended_results_20260929','fusion_results','husbandry_results','predictor_fixed','transport_results','funded_results')):
        print('LEDGER',path,'CASES',section['cases'],flush=True)
        for candidate,stats in section['variants'].items():
            print(Path(candidate).stem,stats,flush=True)
print('REVIEW_SAVED',str(output),flush=True)

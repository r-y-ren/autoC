"""Paired summaries; keep worlds, seats, real programs and proxies distinct."""
from pathlib import Path
from collections import defaultdict,Counter
import json,statistics
D=Path(__file__).resolve().parent;R=D.parents[1]
BASE='submissions/release_v10_r2/main.py'
def load(path):
    return [json.loads(s) for s in Path(path).read_text().splitlines() if s.strip()] if Path(path).exists() else []
def key(row):return (row['opponent_sha256'],row['seed'],row['seat'])
def score(row):return 1.0 if row['margin']>0 else (0.5 if row['margin']==0 else 0.0)
def summarize(rows,baseline):
    out={}
    for candidate in sorted({r['candidate'] for r in rows}):
        cr=[r for r in rows if r['candidate']==candidate];panels={}
        for panel in sorted({r['panel'] for r in cr}):
            data=[r for r in cr if r['panel']==panel];pairs=[(r,baseline[key(r)]) for r in data if key(r) in baseline and r.get('valid') and baseline[key(r)].get('valid')]
            deltas=[a['margin']-b['margin'] for a,b in pairs]
            panels[panel]=dict(cases=len(data),invalid=sum(not r.get('valid') for r in data),paired=len(pairs),wins=sum(r.get('margin',0)>0 for r in data if r.get('valid')),losses=sum(r.get('margin',0)<0 for r in data if r.get('valid')),base_wins=sum(b['margin']>0 for a,b in pairs),better_outcomes=sum(score(a)>score(b) for a,b in pairs),worse_outcomes=sum(score(a)<score(b) for a,b in pairs),mean_margin_delta=round(statistics.mean(deltas),2) if deltas else None,worst_margin_delta=min(deltas) if deltas else None)
        decisions=Counter(r.get('macro',{}).get('_CS_REPORT',{}).get('cs_decision','') for r in cr)
        out[candidate]=dict(cases=len(cr),worlds=len({r['seed'] for r in cr}),panels=panels,decisions=dict(decisions))
    return out
if __name__=='__main__':
    old=load(R/'research/meta_rebuild_20260927/midgame_herd_results.jsonl')
    extended=load(D/'herd_extended_results.jsonl');repeated=load(D/'repeated_results.jsonl')
    baseline={key(r):r for r in old+extended if r['candidate']==BASE}
    reports={name:summarize(rows,baseline) for name,rows in [('extended',extended),('repeated',repeated)]}
    (D/'development_summary.json').write_text(json.dumps(reports,indent=2))
    for batch,report in reports.items():
        for path,row in report.items():
            print(batch,Path(path).name,'N',row['cases'],'WORLD',row['worlds'],'PANELS',json.dumps(row['panels']),'DECISIONS',json.dumps(row['decisions']),flush=True)

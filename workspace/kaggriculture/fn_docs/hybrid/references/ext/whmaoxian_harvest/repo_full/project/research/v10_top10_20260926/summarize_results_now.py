"""Summarize only saved Kaggriculture study ledgers; no matches or uploads."""
from pathlib import Path
from collections import defaultdict
import hashlib,json,statistics,sys
D=Path(__file__).resolve().parent
for filename in sys.argv[1:]:
    path=D/filename
    assert path.parent==D and path.name.endswith('_results.jsonl')
    rows=[json.loads(s) for s in path.read_text(encoding='utf-8').splitlines() if s.strip()]
    groups=defaultdict(list)
    for row in rows: groups[(row['candidate'],row.get('panel',''))].append(row)
    baseline={(r['opponent'],r['seed'],r['seat']):r for r in rows if r['candidate']=='submissions/release_v10_r2/main.py' and r.get('valid')}
    summaries=[]
    for (candidate,panel),group in sorted(groups.items()):
        good=[r for r in group if r.get('valid')]
        pairs=[(r,baseline[(r['opponent'],r['seed'],r['seat'])]) for r in good if (r['opponent'],r['seed'],r['seat']) in baseline]
        point=lambda r:1.0 if r['margin']>0 else .5 if r['margin']==0 else 0.0
        result=dict(candidate=candidate,panel=panel,games=len(group),invalid=len(group)-len(good),wins=sum(r['margin']>0 for r in good),ties=sum(r['margin']==0 for r in good),losses=sum(r['margin']<0 for r in good),mean_margin=statistics.mean(r['margin'] for r in good) if good else None)
        result.update(pairs=len(pairs),paired_point_gain=statistics.mean(point(a)-point(b) for a,b in pairs) if pairs else None,paired_margin_gain=statistics.mean(a['margin']-b['margin'] for a,b in pairs) if pairs else None)
        summaries.append(result)
    out=dict(ledger=filename,rows=len(rows),invalid=sum(not r.get('valid') for r in rows),source_hashes=sorted({r.get('candidate_sha256','') for r in rows}),summaries=summaries)
    path.with_suffix('.current_summary.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps(out,ensure_ascii=False),flush=True)

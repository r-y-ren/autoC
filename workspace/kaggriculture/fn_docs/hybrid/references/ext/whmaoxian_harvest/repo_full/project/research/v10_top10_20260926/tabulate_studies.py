"""Compact readout of completed or explicitly partial local study results."""
from pathlib import Path
from collections import defaultdict
import json,statistics,sys
D=Path(__file__).resolve().parent
for filename in sys.argv[1:]:
    p=D/filename;assert p.parent==D and p.name.endswith('_results.jsonl')
    rows=[json.loads(s) for s in p.read_text(encoding='utf-8').splitlines() if s.strip()]
    groups=defaultdict(list)
    for r in rows:groups[(r['candidate'],r.get('panel',''))].append(r)
    print('LEDGER',filename,'ROWS',len(rows),'INVALID',sum(not r.get('valid') for r in rows),flush=True)
    baseline={(r['opponent'],r['seed'],r['seat']):r for r in rows if r['candidate']=='submissions/release_v10_r2/main.py' and r.get('valid')}
    output=[]
    for (candidate,panel),group in sorted(groups.items()):
        good=[r for r in group if r.get('valid')]
        pairs=[(r,baseline[(r['opponent'],r['seed'],r['seat'])]) for r in good if (r['opponent'],r['seed'],r['seat']) in baseline]
        point=lambda r:1 if r['margin']>0 else .5 if r['margin']==0 else 0
        row=dict(candidate=candidate,panel=panel,n=len(group),wins=sum(r['margin']>0 for r in good),ties=sum(r['margin']==0 for r in good),losses=sum(r['margin']<0 for r in good),mean_margin=round(statistics.mean(r['margin'] for r in good),2) if good else None)
        row.update(pairs=len(pairs),point_gain=round(statistics.mean(point(a)-point(b) for a,b in pairs),4) if pairs else None,margin_gain=round(statistics.mean(a['margin']-b['margin'] for a,b in pairs),2) if pairs else None)
        output.append(row)
        print(Path(candidate).parent.name+'/'+Path(candidate).stem,panel,f"{row['wins']}/{row['losses']}/{row['ties']}",'margin',row['mean_margin'],'paired_gain',row['point_gain'],row['margin_gain'],flush=True)
    p.with_suffix('.compact_summary.json').write_text(json.dumps(dict(ledger=filename,rows=len(rows),groups=output),indent=2),encoding='utf-8')

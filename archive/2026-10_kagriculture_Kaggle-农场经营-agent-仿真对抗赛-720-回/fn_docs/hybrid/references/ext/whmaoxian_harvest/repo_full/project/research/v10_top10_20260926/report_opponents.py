"""Keep per-opponent results visible instead of pooling unrelated strategies."""
from pathlib import Path
from collections import defaultdict
import json,statistics,sys
D=Path(__file__).resolve().parent
for name in sys.argv[1:]:
    path=D/name;assert path.parent==D and path.name.endswith('_results.jsonl')
    rows=[json.loads(s) for s in path.read_text(encoding='utf-8').splitlines() if s.strip()]
    groups=defaultdict(list)
    for r in rows:
        if r.get('valid'):groups[(r['candidate'],r['family'])].append(r)
    print('LEDGER',name,'COUNT',len(rows),'INVALID',sum(not r.get('valid') for r in rows),flush=True)
    report=[]
    for (candidate,family),group in sorted(groups.items()):
        row=dict(candidate=candidate,family=family,n=len(group),wins=sum(r['margin']>0 for r in group),ties=sum(r['margin']==0 for r in group),mean=round(statistics.mean(r['margin'] for r in group),2),worst=min(r['margin'] for r in group))
        report.append(row)
        print(Path(candidate).parent.name+'/'+Path(candidate).stem,family,row['n'],row['wins'],row['ties'],row['mean'],row['worst'],flush=True)
    path.with_suffix('.opponents.json').write_text(json.dumps(report,indent=2),encoding='utf-8')

"""Compact paired review for explicitly named experiment ledgers."""
from pathlib import Path
from collections import defaultdict
import json,sys,statistics
D=Path(__file__).resolve().parent
BASE='submissions/release_v10_r2/main.py'
def read(p):return [json.loads(s) for s in p.read_text().splitlines() if s.strip()]
def key(r):return r['seed'],r['seat'],r['opponent'],r.get('opponent_sha256')
def points(r):return 1 if r['margin']>0 else 0 if r['margin']<0 else .5
refs={key(r):r for f in ('midgame_herd_results.jsonl','herd_extended_results_20260929.jsonl') for r in read(D/f) if r['candidate']==BASE and r['valid']}
for name in sys.argv[1:]:
    path=D/name
    if not path.exists():print('MISSING',name);continue
    rows=read(path);groups=defaultdict(list)
    for r in rows:groups[r['candidate']].append(r)
    print('LEDGER',name,'CASES',len(rows),'INVALID',sum(not r.get('valid') for r in rows),flush=True)
    for candidate,group in groups.items():
        valid=[r for r in group if r.get('valid')];panels={}
        for panel in sorted({r['panel'] for r in valid}):
            rr=[r for r in valid if r['panel']==panel];paired=[(r,refs[key(r)]) for r in rr if key(r) in refs]
            panels[panel]=dict(n=len(rr),w=sum(r['margin']>0 for r in rr),l=sum(r['margin']<0 for r in rr),t=sum(r['margin']==0 for r in rr),paired=len(paired),point_gain=sum(points(r)-points(b) for r,b in paired),margin_gain=round(statistics.mean([r['margin']-b['margin'] for r,b in paired]),1) if paired else None)
        counters=defaultdict(float)
        for r in valid:
            for k,v in r.get('macro',{}).get('_MP_REPORT',{}).items():
                if isinstance(v,(int,float)):counters[k]+=v
        print(Path(candidate).stem,json.dumps(dict(panels=panels,counters=dict(counters))),flush=True)

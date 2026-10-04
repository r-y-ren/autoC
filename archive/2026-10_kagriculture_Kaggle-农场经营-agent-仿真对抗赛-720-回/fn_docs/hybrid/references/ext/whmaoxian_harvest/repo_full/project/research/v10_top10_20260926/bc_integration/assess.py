"""Separate public agents, reconstructed proxies, and direct-reference results."""
from pathlib import Path
from collections import defaultdict
import hashlib,json,statistics,sys
B=Path(__file__).resolve().parent;BASE='submissions/release_v10_r2/main.py'
def load(path):return [json.loads(s) for s in Path(path).read_text(encoding='utf-8').splitlines() if s.strip()]
def point(row):return 1.0 if row['margin']>0 else .5 if row['margin']==0 else 0.0

def summarize(path):
    rows=load(path);groups=defaultdict(list)
    base={(r['opponent_sha256'],r['seed'],r['seat']):r for r in rows if r['candidate']==BASE}
    assert len({r['id'] for r in rows})==len(rows)
    for row in rows:groups[(row['candidate'],row['panel'])].append(row)
    reports=[]
    for (candidate,panel),group in sorted(groups.items()):
        valid=[r for r in group if r.get('valid')]
        paired=[(r,base[(r['opponent_sha256'],r['seed'],r['seat'])]) for r in valid if (r['opponent_sha256'],r['seed'],r['seat']) in base]
        counts={key:sum(r.get('bc_telemetry',{}).get(key,0) for r in valid) for key in ('predictions','proposed','changed','extra','held','errors')}
        report=dict(candidate=candidate,panel=panel,games=len(group),invalid=len(group)-len(valid),wins=sum(r['margin']>0 for r in valid),losses=sum(r['margin']<0 for r in valid),ties=sum(r['margin']==0 for r in valid),paired=len(paired),telemetry=counts)
        report['point_gain']=statistics.mean(point(a)-point(b) for a,b in paired) if paired else None
        report['margin_gain']=statistics.mean(a['margin']-b['margin'] for a,b in paired) if paired else None
        reports.append(report)
    result=dict(records=len(rows),invalid=sum(not r.get('valid') for r in rows),groups=reports,ledger_sha256=hashlib.sha256(Path(path).read_bytes()).hexdigest())
    Path(path).with_suffix('.summary.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    return result
if __name__=='__main__':
    result=summarize(B/sys.argv[1]); print(json.dumps(result),flush=True)

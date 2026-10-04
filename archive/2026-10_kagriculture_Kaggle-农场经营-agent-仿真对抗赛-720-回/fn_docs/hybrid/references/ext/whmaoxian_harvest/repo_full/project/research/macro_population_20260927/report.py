"""Paired developmental readout; keep opponent families and actual economics separate."""
from pathlib import Path
from collections import defaultdict
import hashlib,json,statistics,sys
D=Path(__file__).resolve().parent;BASE='submissions/release_v10_r2/main.py'
def load(name):return [json.loads(s) for s in (D/name).read_text().splitlines()]
def point(r):return 1 if r['margin']>0 else .5 if r['margin']==0 else 0
def summarize(name):
    rows=load(name);controls={(r['opponent'],r['seed'],r['seat']):r for r in rows if r['candidate']==BASE}
    groups=defaultdict(list)
    for r in rows:groups[r['candidate']].append(r)
    result=[]
    for candidate,group in groups.items():
        families={};changes=0;wage=0;harvest=0;cashgain=0
        for family in sorted({r['family'] for r in group}):
            items=[r for r in group if r['family']==family];pairs=[(r,controls[(r['opponent'],r['seed'],r['seat'])]) for r in items if (r['opponent'],r['seed'],r['seat']) in controls]
            good=[r for r in items if r.get('valid')]
            families[family]=dict(games=len(items),invalid=len(items)-len(good),wins=sum(r['margin']>0 for r in good),losses=sum(r['margin']<0 for r in good),ties=sum(r['margin']==0 for r in good),points=statistics.mean(point(r) for r in good) if good else 0,paired=len(pairs),gain=statistics.mean(point(a)-point(b) for a,b in pairs) if pairs else None,margin_gain=statistics.mean(a['margin']-b['margin'] for a,b in pairs) if pairs else None)
            for a,b in pairs:
                if not a.get('valid') or not b.get('valid'):continue
                ea,eb=a['economics'][0],b['economics'][0]
                changes+=ea!=eb;wage+=ea['wages']-eb['wages'];harvest+=sum(ea['harvest'].values())-sum(eb['harvest'].values());cashgain+=a['money'][0]-b['money'][0]
        external=[v for k,v in families.items() if k!='r2' and v['gain'] is not None]
        score=statistics.mean(v['gain'] for v in external) if external else None
        invalid=sum(not r.get('valid') for r in group)
        result.append(dict(candidate=candidate,games=len(group),invalid=invalid,families=families,external_gain=score,changed_economic_cases=changes,wage_delta_sum=wage,harvest_delta_sum=harvest,cash_delta_sum=cashgain))
    return dict(ledger=name,rows=len(rows),invalid=sum(not r.get('valid') for r in rows),groups=result,sha256=hashlib.sha256((D/name).read_bytes()).hexdigest())
if __name__=='__main__':
    for name in sys.argv[1:]:
        result=summarize(name);(D/name).with_suffix('.summary.json').write_text(json.dumps(result,indent=2))
        print(json.dumps(dict(ledger=name,rows=result['rows'],invalid=result['invalid'])),flush=True)
        for g in sorted(result['groups'],key=lambda g:g['external_gain'] if g['external_gain'] is not None else -9,reverse=True):
            print(json.dumps(dict(candidate=Path(g['candidate']).name,games=g['games'],external_gain=g['external_gain'],families={k:[v['wins'],v['losses'],v['ties']] for k,v in g['families'].items()},cash_delta=g['cash_delta_sum'],wage_delta=g['wage_delta_sum'],harvest_delta=g['harvest_delta_sum'])),flush=True)

"""Audit current finite development batches without promoting any candidate."""
from pathlib import Path
from collections import defaultdict
import hashlib,json,statistics
D=Path(__file__).resolve().parent;R=D.parents[1]
NAMES=('tomato_gate2','native_value','tomato_gate3','market_value','herd_allocation','market_value2','macro_transplant','slack_roundtrip')
BASE='submissions/release_v10_r2/main.py';report={}
for name in NAMES:
    manifest=D/(name+'_jobs.json');ledger=D/(name+'_results.jsonl')
    jobs=json.loads(manifest.read_text(encoding='utf-8'))
    rows=[json.loads(s) for s in ledger.read_text(encoding='utf-8').splitlines() if s.strip()] if ledger.exists() else []
    expected={j['id']:j for j in jobs};assert len(expected)==len(jobs)
    assert len({r['id'] for r in rows})==len(rows)
    for row in rows:
        assert row['id'] in expected
        assert all(row.get(k)==v for k,v in expected[row['id']].items())
    controls={(r['opponent_sha256'],r['seed'],r['seat']):r for r in rows if r['candidate']==BASE}
    group=defaultdict(list)
    for row in rows:group[(row['candidate'],row['panel'])].append(row)
    summaries=[]
    for (candidate,panel),members in sorted(group.items()):
        valid=[r for r in members if r.get('valid')]
        paired=[(r,controls[(r['opponent_sha256'],r['seed'],r['seat'])]) for r in valid if (r['opponent_sha256'],r['seed'],r['seat']) in controls]
        point=lambda r:1 if r['margin']>0 else .5 if r['margin']==0 else 0
        summaries.append(dict(candidate=candidate,panel=panel,recorded=len(members),valid=len(valid),wins=sum(r['margin']>0 for r in valid),ties=sum(r['margin']==0 for r in valid),mean_margin=statistics.mean(r['margin'] for r in valid) if valid else None,paired_cases=len(paired),point_gain=statistics.mean(point(a)-point(b) for a,b in paired) if paired else None,margin_gain=statistics.mean(a['margin']-b['margin'] for a,b in paired) if paired else None))
    invalid=[dict(candidate=r['candidate'],family=r['family'],seed=r['seed'],seat=r['seat'],errors=r.get('errors'),exception=r.get('exception'),output=r.get('stderr_stdout')) for r in rows if not r.get('valid')]
    row=dict(expected=len(jobs),recorded=len(rows),complete=len(rows)==len(jobs),invalid=len(invalid),completed_full_games=sum(r.get('statuses')==['DONE','DONE'] for r in rows),summaries=summaries,invalid_examples=invalid[:3],ledger_sha256=hashlib.sha256(ledger.read_bytes()).hexdigest() if ledger.exists() else None)
    report[name]=row
    print(name,row['recorded'],row['expected'],'invalid',row['invalid'],flush=True)
    for g in summaries:
        if g['candidate']!=BASE:print(Path(g['candidate']).name,g['panel'],g['wins'],g['ties'],g['valid'],'gain',g['point_gain'],'margin',None if g['mean_margin'] is None else round(g['mean_margin']),flush=True)
(D/'resume_review.json').write_text(json.dumps({'scope':'Development and implementation audits only; no ranking prediction or release approval.','studies':report},indent=2),encoding='utf-8')

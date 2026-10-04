"""Evaluate new-generation outcomes without pooling evolved rivals into public gains."""
from pathlib import Path
import hashlib,json,random,statistics
from report import summarize,load,point
D=Path(__file__).resolve().parent;BASE='submissions/release_v10_r2/main.py'
rows=load('g2_results.jsonl');jobs=json.loads((D/'g2_jobs.json').read_text())
assert len(rows)==len(jobs) and len({r['id'] for r in rows})==len(rows)
expected={j['id']:j for j in jobs}
for r in rows:assert all(r.get(k)==v for k,v in expected[r['id']].items())
report=summarize('g2_results.jsonl')
controls={(r['opponent'],r['seed'],r['seat']):r for r in rows if r['candidate']==BASE}
core=('aurax','fieldcraft','marketshock','top_style_02','top_style_03')
ranked=[]
for g in report['groups']:
    f=g['families'];core_gain=statistics.mean(f[k]['gain'] for k in core)
    gains={};pairs=[]
    for r in rows:
        if r['candidate']!=g['candidate'] or r['family'] not in core:continue
        b=controls[(r['opponent'],r['seed'],r['seat'])]
        gains.setdefault(r['seed'],[]).append(point(r)-point(b));pairs.append((r,b))
    values=[statistics.mean(v) for v in gains.values()];rng=random.Random(20260927)
    boot=sorted(statistics.mean(rng.choices(values,k=len(values))) for _ in range(4000))
    reasons=[]
    if g['invalid']:reasons.append('runtime_diagnostics')
    if core_gain<=0:reasons.append('no_core_win_gain')
    if min(f[k]['gain'] for k in core)<-.05:reasons.append('core_family_regression')
    if f['r2']['points']<.5:reasons.append('loses_to_reference')
    ranked.append(dict(candidate=g['candidate'],invalid=g['invalid'],core_gain=core_gain,development_interval=[boot[100],boot[3899]],families=f,advance_to_confirmation=not reasons,reasons=reasons))
ranked.sort(key=lambda g:(g['advance_to_confirmation'],g['core_gain']),reverse=True)
result=dict(total=len(rows),invalid=sum(not r.get('valid') for r in rows),worlds=len({r['seed'] for r in rows}),candidates=len(report['groups']),ranked=ranked,core_families=list(core),evolved_population_separate=True,source_ledger_sha256=report['sha256'],online_rating=None)
(D/'g2_assessment.json').write_text(json.dumps(result,indent=2))
print(json.dumps(dict(total=result['total'],invalid=result['invalid'],worlds=result['worlds'],candidates=result['candidates'])),flush=True)
for g in ranked:
    print(json.dumps(dict(candidate=Path(g['candidate']).name,core_gain=g['core_gain'],interval=g['development_interval'],advance=g['advance_to_confirmation'],reasons=g['reasons'],families={k:[v['wins'],v['losses'],v['ties']] for k,v in g['families'].items()})),flush=True)

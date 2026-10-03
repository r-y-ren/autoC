"""Summarize immutable game records with paired baselines and no rating conversion."""
from pathlib import Path
from collections import defaultdict,Counter
from datetime import datetime,timezone
import json,statistics,random
D=Path(__file__).resolve().parent;M=D.parent/'meta_rebuild_20260927'
BASE='submissions/release_v10_r2/main.py'
def rows(path):
    if not path.exists():return []
    return [json.loads(s) for s in path.read_text().splitlines() if s.strip()]
def key(r):return (r['opponent'],r['seed'],r['seat'])
def points(r):return float(r['margin']>0)+.5*float(r['margin']==0)
files=sorted(D.glob('*_results.jsonl'));all_rows=[];batches=[]
for f in files:
    batch=rows(f);all_rows.extend(batch)
    manifest=f.with_name(f.name.replace('_results.jsonl','_jobs.json'))
    expected=len(json.loads(manifest.read_text())) if manifest.exists() else None
    batches.append(dict(file=f.name,completed=len(batch),expected=expected,invalid=sum(not r.get('valid') for r in batch)))
valid=[r for r in all_rows if r.get('valid')]
prior=rows(M/'midgame_herd_results.jsonl')
baselines={key(r):r for r in prior+valid if r.get('valid') and r['candidate']==BASE}
groups=defaultdict(list)
for r in valid:groups[(r['candidate'],r['panel'])].append(r)
result=[]
for (candidate,panel),group in sorted(groups.items()):
    paired=[(r,baselines[key(r)]) for r in group if key(r) in baselines]
    rec=dict(candidate=candidate,panel=panel,n=len(group),wins=sum(r['margin']>0 for r in group),losses=sum(r['margin']<0 for r in group),ties=sum(r['margin']==0 for r in group),mean_margin=statistics.mean(r['margin'] for r in group),paired_n=len(paired))
    if paired:
        rec.update(wins_gained=sum(a['margin']>0 and b['margin']<=0 for a,b in paired),wins_lost=sum(a['margin']<=0 and b['margin']>0 for a,b in paired),point_gain=statistics.mean(points(a)-points(b) for a,b in paired),margin_gain=statistics.mean(a['margin']-b['margin'] for a,b in paired))
        by_seed=defaultdict(list)
        for a,b in paired:by_seed[a['seed']].append(points(a)-points(b))
        values=[statistics.mean(v) for v in by_seed.values()];rec['paired_worlds']=len(values)
        if len(values)>1:
            rng=random.Random(28);sample=sorted(statistics.mean(rng.choices(values,k=len(values))) for _ in range(2000))
            rec['development_world_bootstrap_95']=[sample[49],sample[1949]]
    rec['decisions']=dict(Counter(r.get('macro',{}).get('_CS_REPORT',{}).get('cs_decision','') for r in group))
    rec['max_action_seconds']=max(r.get('max_seconds',0) for r in group)
    rec['max_seconds_over_1']=sum(r.get('max_seconds',0)>1 for r in group)
    result.append(rec)
report=dict(captured_utc=datetime.now(timezone.utc).isoformat(),batches=batches,valid_records=len(valid),unique_valid_cases=len({r['id'] for r in valid}),groups=result,scope='Development comparisons; fixed replay opponents are not responsive programs. No online rating is inferred.')
report['invalid_samples']=[dict(candidate=r['candidate'],error=str(r.get('exception') or r.get('errors'))[-600:]) for r in all_rows if not r.get('valid')][:8]
(D/'SUMMARY_CURRENT.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(dict(batches=batches,unique_valid_cases=report['unique_valid_cases'])),flush=True)
for r in result:
    brief={k:v for k,v in r.items() if k not in ('decisions','candidate')}
    print(Path(r['candidate']).stem,json.dumps(brief),flush=True)

"""Deduplicated finite-league summary; cached preflight rows are counted once."""
from pathlib import Path
from collections import defaultdict
from datetime import datetime,timezone
import json,statistics,random
D=Path(__file__).resolve().parent;M=D.parent/'meta_rebuild_20260927'
BASE='submissions/release_v10_r2/main.py'
def load(path):return [json.loads(s) for s in path.read_text().splitlines() if s.strip()] if path.exists() else []
def key(r):return r['opponent'],r['seed'],r['seat']
def point(r):return float(r['margin']>0)+.5*float(r['margin']==0)
unique={};batches=[]
for path in sorted(D.glob('*_results.jsonl')):
    rows=load(path);manifest=path.with_name(path.name.replace('_results.jsonl','_jobs.json'))
    expected=len(json.loads(manifest.read_text())) if manifest.exists() else None
    batches.append(dict(file=path.name,rows=len(rows),expected=expected,invalid=sum(not r.get('valid') for r in rows)))
    for row in rows:
        if row['id'] in unique:assert row==unique[row['id']]
        else:unique[row['id']]=row
valid=[r for r in unique.values() if r.get('valid')]
base={key(r):r for r in load(M/'midgame_herd_results.jsonl')+valid if r.get('valid') and r['candidate']==BASE}
groups=defaultdict(list)
for row in valid:groups[(row['candidate'],row['panel'])].append(row)
summary=[]
for (candidate,panel),rows in sorted(groups.items()):
    pairs=[(r,base[key(r)]) for r in rows if key(r) in base]
    result=dict(candidate=candidate,panel=panel,n=len(rows),wins=sum(r['margin']>0 for r in rows),losses=sum(r['margin']<0 for r in rows),ties=sum(r['margin']==0 for r in rows),mean_margin=statistics.mean(r['margin'] for r in rows),paired=len(pairs))
    if pairs:
        result.update(wins_gained=sum(a['margin']>0 and b['margin']<=0 for a,b in pairs),wins_lost=sum(a['margin']<=0 and b['margin']>0 for a,b in pairs),point_gain=statistics.mean(point(a)-point(b) for a,b in pairs),margin_gain=statistics.mean(a['margin']-b['margin'] for a,b in pairs))

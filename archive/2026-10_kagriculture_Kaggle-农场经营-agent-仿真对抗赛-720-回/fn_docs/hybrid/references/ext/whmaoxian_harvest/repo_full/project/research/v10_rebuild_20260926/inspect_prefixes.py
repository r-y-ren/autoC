from pathlib import Path
import collections,json,statistics
OUT=Path(__file__).resolve().parent
rows=[json.loads(line) for line in (OUT/'generation3_prefix_results.jsonl').read_text(encoding='utf-8').splitlines()]
groups=collections.defaultdict(list)
for row in rows:groups[Path(row['candidate']).name].append(row)
for name,group in groups.items():
    good=[r for r in group if r.get('valid')]
    if not good:print(name,'INVALID',group[0].get('exception'));continue
    cash=[r['checkpoints'][0]['money'] for r in good]
    cows=[r['checkpoints'][2]['mix'].get('COW',0) for r in good]
    print(name,len(group),'invalid',len(group)-len(good),'day0 minimum',min(cash),
        'day0 below4',sum(c<4 for c in cash),'day3 cows',dict(collections.Counter(cows)),flush=True)
print('Complete prefixes',len(rows),'of799; not full games',flush=True)

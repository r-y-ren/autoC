"""Summarize only frozen study demonstrations and their exact executed trades."""
from collections import Counter
import gzip
import json
from pathlib import Path
import statistics

ROOT=Path(__file__).parent
OUT=ROOT/'research/round8/top2'
index=json.loads((OUT/'compiled_index.json').read_text())
production=json.loads((OUT/'study_production.json').read_text())
teams={}
for team in ('Vadim Vasilenko','DSM'):
    rows=[r for r in index if r['team']==team]
    snapshots=[r for r in production if r['team']==team]
    incompatible={}
    for step in (24,48,72,144,216):
        keys=Counter()
        for r in rows:
            demo=json.loads(gzip.decompress((OUT/f"compiled_{r['episode_id']}_{r['seat']}.json.gz").read_bytes()))
            farm=demo['dawn_states'][step//24]['farm']
            tiles=[[None if isinstance(t,dict) and t.get('kind')=='WEED' else t for t in line] for line in farm['tiles']]
            keys[json.dumps(tiles,sort_keys=True,separators=(',',':'))]+=1
        incompatible[str(step)]={'distinct_full_farm_states_ignoring_only_weeds':len(keys),'largest_compatible_groups':sorted(keys.values(),reverse=True)}
    teams[team]={
        'study_games':len(rows),'unique_world_seeds':len({r['seed'] for r in rows}),
        'reproduced_exactly':sum(r['original_reproduced_exactly'] for r in rows),
        'median_income_by_product':{k:statistics.median(r['sales_income'].get(k,0) for r in rows) for k in ('MILK','WOOL','STRAWBERRY','EGG','MELON','TOMATO','CARROT')},
        'unexecuted_purchase_requests':dict(sum((Counter(r['requested'])-Counter(r['successful']) for r in rows),Counter())),
        'noop_nonmovement_requests':dict(sum((Counter(r['noop_requests']) for r in rows),Counter())),
        'farm_compatibility':incompatible,
        'first_shop_coverage':dict(Counter(r['daily_snapshots'][3]['shops'][0] for r in snapshots)),
        'daily_medians':[{ 'day_zero_based':day,'hands':statistics.median(r['daily_snapshots'][day]['hands'] for r in snapshots),'counts':{k:statistics.median(r['daily_snapshots'][day]['counts'].get(k,0) for r in snapshots) for k in ('WHEAT','MELON','STRAWBERRY','COW','SHEEP','GOOSE','TOMATO','CARROT')}} for day in (2,5,9,14,19,24,29)],
    }
(OUT/'study_findings.json').write_text(json.dumps(teams,indent=2),encoding='utf-8')
for team,data in teams.items():
    print(team,'coverage',data['first_shop_coverage'],'compatibility',data['farm_compatibility'])

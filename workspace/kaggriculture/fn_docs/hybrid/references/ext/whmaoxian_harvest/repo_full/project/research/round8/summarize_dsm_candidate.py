"""Summarize the declared DSM-style proxy comparison by independent world."""
import json
import statistics
from collections import defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
path=ROOT/'results/round8_dsm_candidate_development8.jsonl'
rows=[json.loads(x) for x in path.read_text().splitlines()]
assert len(rows)==48
report={'games':len(rows),'worlds':len({r['seed'] for r in rows}),'valid':sum(r['valid'] for r in rows),'by_opponent':{},'by_world':[]}
for opponent in sorted({r['opponent'] for r in rows}):
    group=[r for r in rows if r['opponent']==opponent]
    worlds=defaultdict(list)
    for r in group:worlds[r['seed']].append(r)
    wd=[statistics.mean(r['delta'] for r in g) for g in worlds.values()]
    report['by_opponent'][opponent]={
        'games':len(group),'worlds':len(worlds),'wins':sum(r['delta']>0 for r in group),
        'ties':sum(r['delta']==0 for r in group),'losses':sum(r['delta']<0 for r in group),
        'world_mean_margin':statistics.mean(wd),'world_median_margin':statistics.median(wd),
        'world_min_margin':min(wd),'world_max_margin':max(wd),
        'positive_worlds':sum(x>0 for x in wd),'negative_worlds':sum(x<0 for x in wd),
        'mean_bank':statistics.mean(r['money'] for r in group),
        'max_action_seconds':max(r['max_action_seconds'] for r in group),
        'max_final_carried_units':max(r['final_carried'] for r in group),
        'mean_final_carried_units':statistics.mean(r['final_carried'] for r in group),
        'nonempty_final_shed_games':sum(any(r['final_shed'].values()) for r in group),
        'nonzero_candidate_error_games':sum(bool(r['telemetry'][0]['nonzero']) for r in group),
        'worlds_with_seat_difference':sum(len({r['delta'] for r in g})>1 for g in worlds.values())}
for seed in sorted({r['seed'] for r in rows}):
    group=[r for r in rows if r['seed']==seed]
    report['by_world'].append({'seed':seed,'by_opponent':{op:{'seat0_delta':next(r['delta'] for r in group if r['opponent']==op and r['seat']==0),
                              'seat1_delta':next(r['delta'] for r in group if r['opponent']==op and r['seat']==1)}
                              for op in report['by_opponent']}})
(ROOT/'research/round8/dsm_candidate_development_summary.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report))
